import numpy as np
from numpy import count_nonzero
import tensorflow as tf

from n3fit.backends import MetaLayer
from n3fit.backends import operations as op


class Mask(MetaLayer):
    """
    This layers applies a boolean mask to a rank-1 input tensor.
    The mask admit a multiplier for all outputs which will be internally
    saved as a weight so it can be updated during trainig.

    Typical usage is to apply training/validation split masks
    or applying a multiplier to a given layer


    Parameters
    ----------
        bool_mask: np.array
            numpy array with the boolean mask to be applied
        c: float
            constant multiplier for every output
    """

    def __init__(self, bool_mask=None, c=None, **kwargs):
        if bool_mask is None:
            self.mask = None
        else:
            self.mask = op.numpy_to_tensor(bool_mask, dtype=bool)
            self.nonzero_per_replica = count_nonzero(bool_mask[0, ...])
            self.mask_tensor = Mask.tensor_from_mask(self.mask)
        self.c = c
        super().__init__(**kwargs)

    def build(self, input_shape):
        if self.c is not None:
            initializer = MetaLayer.init_constant(value=self.c)
            self.kernel = self.builder_helper("mask", (1,), initializer, trainable=False)
        super(Mask, self).build(input_shape)

    def call(self, y):
        """
        Apply the mask to the input tensor

        Parameters
        ----------
            y: tf.Tensor
                input tensor of shape (1, replicas, ndata)

        Returns
        -------
            tf.Tensor
                output tensor of shape (1, replicas, ndata_filtered)
        """
        if self.mask is not None:
            y = op.einsum('brn, rnm -> brm', y, self.mask_tensor)

        if self.c is not None:
            y = y * self.kernel

        return y

    @staticmethod
    def tensor_from_mask(mask):
        """
        Create a rank 3 tensor that replicates the functionality of tf.boolean_mask
        with multiplication

        Args:
            mask: a rank 2 boolean tensor of shape (replicas, ndata)

        Returns:
            rank 3 tensor with shape (replicas, ndata, ndata_masked))
            for each (r, n, m=i) matrix, there are exactly r ones, one for each n
        """
        r, n = mask.shape
        M = np.sum(mask)

        mask_array = []
        for idx in np.argwhere(mask):
            temp_matrix = np.zeros((r, n))
            temp_matrix[tuple(idx)] = 1
            mask_array.append(temp_matrix)

        if len(mask_array) > 0:
            mask_array = np.stack(mask_array, axis=-1)

        mask_tensor = op.numpy_to_tensor(mask_array)
        # split the last axis into a replica axis and a masked indices axis
        mask_tensor = op.reshape(mask_tensor, shape=(r, n, r, -1))
        # sum over the replica axis
        mask_tensor = tf.reduce_sum(mask_tensor, axis=2)
        return mask_tensor
