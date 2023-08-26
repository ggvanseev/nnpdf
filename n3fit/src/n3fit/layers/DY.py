from itertools import zip_longest

import numpy as np

from n3fit.backends import operations as op

from .observable import Observable


class DY(Observable):
    """
    Computes the convolution of two PDFs (the same one twice) and one fktable
    """

    def mask_fktable(self, basis, fktable):
        """
        Mask the fktable according to the mask

        Parameters
        ----------
            basis: list(int)
                list of active flavours
            fktable: backend tensor
                rank 4 tensor (ndata, masked_flavors, xgrid, xgrid)

        Returns
        -------
            masked_fktable: backend tensor
                rank 5 tensor (ndata, xgrid, flavours, xgrid, flavours)
        """
        if basis is None:
            basis_mask = np.ones((self.nfl, self.nfl), dtype=bool)
        else:
            basis_mask = np.zeros((self.nfl, self.nfl), dtype=bool)
            for i, j in basis.reshape(-1, 2):
                basis_mask[i, j] = True
        basis_mask = op.numpy_to_tensor(basis_mask, dtype=bool)
        mask_tensor = self.tensor_from_mask(basis_mask)
        masked_fk = op.einsum('fgF, nFxy -> nxfyg', mask_tensor, fktable)
        return masked_fk

    def call(self, pdf):
        """
        This function perform the fktable \otimes pdf \otimes pdf convolution.

        First uses the basis of active combinations to generate a luminosity tensor
        with only some flavours active.

        The concatenate function returns a rank-3 tensor (combination_index, xgrid, xgrid)
        which can in turn be contracted with the rank-4 fktable.

        Parameters
        ----------
            pdf_in: tensor
                rank 4 tensor (batchsize, replicas, xgrid, flavours)

        Returns
        -------
            results: tensor
                rank 3 tensor (batchsize, replicas, ndata)
        """
        # Hadronic observables might need splitting of the input pdf in the x dimension
        # so we have 3 different paths for this layer
        pdfs = op.split(pdf, self.splitting, axis=2) if self.splitting else [pdf]

        results = []
        for pdf in pdfs:
            intermediate = op.einsum('nxfyg, bryg -> brnxf', masked_fk, pdf)
            results.append(op.einsum('brnxf, brxf -> brn', intermediate, pdf))

        return self.operation(results)
