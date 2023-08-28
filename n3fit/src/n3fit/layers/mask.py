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
        self.has_mask = bool_mask is not None
        if self.has_mask:
            self.mask_tensor = Mask.tensor_from_mask(bool_mask)
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
                input tensor of shape (batchsize, replicas, ndata)

        Returns
        -------
            tf.Tensor
                output tensor of shape (batchsize, replicas, ndata_filtered)
        """
        if self.has_mask:
            y = op.einsum('brn, rnm -> brm', y, self.mask_tensor)

        if self.c is not None:
            y = y * self.kernel

        return y

    @staticmethod
    def tensor_from_mask(bool_mask):
        """
        Create a rank 3 tensor that replicates the functionality of tf.boolean_mask
        with multiplication

        Args:
            mask: list of list of booleans of shape (replicas, ndata)

        Returns:
            rank 3 tensor with shape (replicas, ndata, ndata_masked)
            for each (r, n, m=i) matrix, there are exactly r ones, one for each n
        """
        mask = np.array(bool_mask, dtype=bool)
        r, n = mask.shape

        # This creates an array of shape (replicas, ndata, num_trues) that has a single
        # 1 in each (r, n) matrix at the position of the corresponding true in the mask
        mask_array = []
        for idx in np.argwhere(mask):
            temp_matrix = np.zeros((r, n))
            temp_matrix[tuple(idx)] = 1
            mask_array.append(temp_matrix)

        # It happens that there are no true values in the mask, in which case
        # the mask_array is empty and the stack operation fails
        if len(mask_array) > 0:
            mask_array = np.stack(mask_array, axis=-1)
        mask_tensor = op.numpy_to_tensor(mask_array)

        # split the last axis into a replica axis and a masked indices axis
        mask_tensor = op.reshape(mask_tensor, shape=(r, n, r, -1))
        # sum over the replica axis
        mask_tensor = tf.reduce_sum(mask_tensor, axis=2)
        return mask_tensor
