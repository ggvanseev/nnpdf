from abc import ABC, abstractmethod

import numpy as np

from n3fit.backends import MetaLayer
from n3fit.backends import operations as op


def is_unique(list_of_arrays):
    """Check whether the list of arrays more than one different arrays"""
    the_first = list_of_arrays[0]
    for i in list_of_arrays[1:]:
        if not np.array_equal(the_first, i):
            return False
    return True


class Observable(MetaLayer, ABC):
    """
    This class is the parent of the DIS and DY convolutions.
    All backend-dependent code necessary for the convolutions
                                is (must be) concentrated here

    The methods gen_mask and call must be overriden by the observables
    where
        - gen_mask: it is called by the initializer and generates the mask between
                    fktables and pdfs
        - call: this is what does the actual operation


    Parameters
    ----------
        fktable_data: list[validphys.coredata.FKTableData]
            list of FK which define basis and xgrid for the fktables in the list
        fktable_arr: list
            list of fktables for this observable
        operation_name: str
            string defining the name of the operation to be applied to the fktables
        nfl: int
            number of flavours in the pdf (default:14)
    """

    def __init__(self, fktable_data, fktable_arr, operation_name, nfl=14, **kwargs):
        super(MetaLayer, self).__init__(**kwargs)

        self.nfl = nfl

        all_bases = []
        xgrids = []
        fktables = []
        for fkdata, fk in zip(fktable_data, fktable_arr):
            xgrids.append(fkdata.xgrid.reshape(1, -1))
            all_bases.append(fkdata.luminosity_mapping)
            fktables.append(op.numpy_to_tensor(fk))

        # check how many xgrids this dataset needs
        if is_unique(xgrids):
            self.splitting = None
        else:
            self.splitting = [i.shape[1] for i in xgrids]

        self.operation = op.c_to_py_fun(operation_name)
        self.output_dim = fktables[0].shape[0]

        self.masked_fk_tables = [
            self.mask_fktable(basis, fk) for basis, fk in zip_copies(all_bases, fktables)
        ]

    def compute_output_shape(self, input_shape):
        return (self.output_dim, None)

    # Overridables
    @abstractmethod
    def mask_fktable(self, basis, fktable):
        pass

    @staticmethod
    def tensor_from_mask(mask):
        """
        Create a rank 3 tensor that replicates the functionality of tf.boolean_mask

        Args:
            mask: a rank 2 boolean tensor

        Returns:
            rank 3 tensor with shape (mask.shape[0], mask.shape[1], tf.reduce_sum(mask))
            of zeros and ones such that
            tf.boolean_mask(tensor, mask, axis=1) == tf.einsum('fg..., fgF -> F...', tensor, tensor_from_mask(mask))
        """
        mask_array = []
        for i in range(mask.shape[0]):
            if len(mask.shape) == 1:
                if mask[i] == True:
                    temp_matrix = np.zeros(mask.shape)
                    temp_matrix[i] = 1
                    mask_array.append(temp_matrix)
            else:  # rank 2
                for j in range(mask.shape[1]):
                    if mask[i, j] == True:
                        temp_matrix = np.zeros(mask.shape)
                        temp_matrix[i, j] = 1
                        mask_array.append(temp_matrix)
        mask = np.stack(mask_array, axis=-1)
        mask_tensor = op.numpy_to_tensor(mask)
        return mask_tensor


def zip_copies(list_a, list_b):
    """
    Zip two lists of different lengths by repeating the elements of the shorter one
    """
    if len(list_a) > len(list_b):
        return zip(list_a, list_b * len(list_a))
    else:
        return zip(list_a * len(list_b), list_b)
