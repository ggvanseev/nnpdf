"""
    DIS layer

    This layer produces a DIS observable, which can consists of one or more fktables.
    The rationale behind this layer is to keep all required operation in one single place
    such that is easier to optimize or modify.
"""

import numpy as np

from n3fit.backends import operations as op

from .observable import Observable


class DIS(Observable):
    """
    The DIS class receives a list of active flavours and a fktable
    and prepares a layer that performs the convolution of said fktable with
    the incoming pdf.

    The fktable is expected to be rank 3 (ndata, xgrid, flavours)
    while the input pdf is rank 4 where the first dimension is the batch dimension
    and the last dimension the number of replicas being fitted (1, xgrid, flavours, replicas)
    """

    def mask_fktable(self, basis, fktable):
        """
        Mask the fktable to the active flavours

        Parameters
        ----------
            basis: list(int)
                list of active flavours
            fktable: backend tensor
                rank 3 tensor (ndata, masked_flavors, xgrid)

        Returns
        -------
            masked_fktable: backend tensor
                rank 3 tensor (ndata, xgrid, flavours)
        """
        if basis is None:
            basis_mask = np.ones(self.nfl, dtype=bool)
        else:
            basis_mask = np.zeros(self.nfl, dtype=bool)
            for i in basis:
                basis_mask[i] = True
        basis_mask = op.numpy_to_tensor(basis_mask, dtype=bool)
        mask_tensor = self.tensor_from_mask(basis_mask)
        masked_fk = op.einsum('fF, nFx -> nxf', mask_tensor, fktable)
        return masked_fk

    def call(self, pdf):
        """
        This function perform the fktable \otimes pdf convolution.

        First pass the input PDF through a mask to remove the unactive flavors,
        then a tensor_product between the PDF and each fktable is performed
        finally the defined operation is applied to all the results

        Parameters
        ----------
            pdf:  backend tensor
                rank 4 tensor (batch_size, xgrid, flavours, replicas)

        Returns
        -------
            result: backend tensor
                rank 3 tensor (batchsize, replicas, ndata)
        """
        # DIS never needs splitting
        if self.splitting is not None:
            raise ValueError("DIS layer call with a dataset that needs more than one xgrid?")

        results = [
            op.einsum('brxf, nxf -> brn', pdf, masked_fk) for masked_fk in self.masked_fk_tables
        ]

        return self.operation(results)
