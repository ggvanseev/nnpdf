"""
A useful set of functions for implementation of datasets in commondata.

@author: Tanishq Sharma
"""

import numpy as np

from math import sqrt
from numpy.linalg import eig

def symmetrize_errors(delta_plus, delta_minus):
    r"""Compute the symmterized uncertainty and the shift in data point.

    Parameters
    ----------
    delta_plus : float
        The top/plus uncertainty with sign
    delta_minus : float
        The bottom/minus uncertainty with sign
    
    Returns
    -------
    se_delta : float
        The value to be added to the data point
    se_sigma : float
        The symmetrized uncertainty to be used in commondata

    """
    semi_diff = (delta_plus + delta_minus)/2
    average = (delta_plus - delta_minus)/2
    se_delta = semi_diff
    se_sigma = sqrt(average*average + 2*semi_diff*semi_diff)
    return se_delta, se_sigma

def percentage_to_absolute(percentage, value):
    r"""Compute the absolute value of uncertainty from percentage.

    Parameters
    ----------
    percentage : string
        Experimental datasets can provide the percentage 
        uncertainties with a % sign or without one. 
        In case a % sign is used, it will be automatically 
        stripped and the remaining string converted to a 
        float. If a % sign is not present, just input the 
        percentage uncertainty as a string, i.e. str(value).
        This is important as this functions uses replace()
        function which requires a string input.
    value : float
        The data point

    Returns
    -------
    absolute : float
        The absolute value of the uncertainty
    
    """
    percentage = float(percentage.replace("%", ""))
    absolute = percentage * value * 0.01
    return absolute 

def corMat_to_covMat(errList, corMatList):
    r"""Converts correlation matrix elements to covariance
    matrix elements.

    Parameters
    ----------
    errList : list
        A one dimensional list which contains the uncertainty
        associated to each data point in order.
    corMatList : list
        A one dimensional list which contains the elements of 
        the correlation matrix row by row. Since experimental
        datasets provide these matrices in a list form, this 
        simplifies the implementation for the user.

    Returns
    -------
    covMatList : list
        A one dimensional list which contains the elements of
        the covariance matrix row by row.
    
    """
    covMatList = []
    for i in range(len(corMatList)):
        a = i // len(errList)
        b = i % len(errList)
        covMatList.append(corMatList[i] * errList[a] * errList[b])
    return covMatList

def covMat_to_artUnc(ndata, covMatList, is_normalized):
    r"""Converts the covariance matrix to a matrix of 
    artificial uncertainties.

    Parameters
    ----------
    ndata : integer
        Number of data points
    covMatList : list
        A one dimensional list which contains the elements of
        the covariance matrix row by row. Since experimental
        datasets provide these matrices in a list form, this 
        simplifies the implementation for the user.
    is_normalized : boolean
        True if the dataset contains normalized values, False 
        if the dataset contains absolute values. Needed for 
        proper determination of whether the matrix is postive-
        semidefinite.

    Returns
    -------
    artUnc : numpy.ndarray
        A two dimensional matrix which contains artificial 
        uncertainties to be added to the commondata. 
        i^th row contains the artificial uncertainties of
        the i^th data point.
            
    """
    epsilon = -0.0000000001
    negEValCount = 0
    psdCheck = True
    covMat = np.zeros((ndata, ndata))
    artUnc = np.zeros((ndata, ndata))
    for i in range(len(covMatList)):
        a = i // ndata
        b = i % ndata
        covMat[a][b] = covMatList[i]
    eigVal, eigVec = eig(covMat)
    if is_normalized == False:
        for i in range(ndata):
            for j in range(ndata):
                if eigVal[j] <= 0:
                    raise ValueError('The covariance matrix is not positive-semidefinite')
                else:
                    artUnc[i][j] = eigVec[i][j] * sqrt(eigVal[j])
    elif is_normalized == True:
        for j in range(len(eigVal)):
            if eigVal[j] < epsilon:
                psdCheck = False
            elif eigVal[j] > epsilon and eigVal[j] <= 0:
                negEValCount = negEValCount + 1
                if negEValCount == 2:
                    psdCheck = False
            elif eigVal[j] > 0:
                continue
        if psdCheck == False:
            raise ValueError('The covariance matrix is not positive-semidefinite')
        else:
            for i in range(ndata):
                for j in range(ndata):
                    if eigVal[j] < 0:
                        continue
                    else:
                        artUnc[i][j] = eigVec[i][j] * sqrt(eigVal[j]) 
    return artUnc.tolist()

def cross_corMat_to_covMat(rowErrList, colErrList, corMatList):
    covMatList = []
    for i in range(len(corMatList)):
        a = i // len(colErrList)
        b = i % len(colErrList)
        covMatList.append(corMatList[i] * rowErrList[a] * colErrList[b])
    return covMatList

def matList_to_matrix(rows, columns, matList):
    if rows * columns == len(matList):
        matrix = np.zeros((rows, columns))
        for i in range(rows):
            for j in range(columns):
                matrix[i][j] = matList[j + i * columns]
        matrix = np.array(matrix)
        return matrix.tolist()
    else:
        raise Exception('rows * columns != len(matList)')
    
def concatMatrices(matInRows, matInColumns, listOfMatrices):
    for i in range(len(listOfMatrices)):
        listOfMatrices[i] = np.array(listOfMatrices[i])
    colList = []
    for i in range(matInRows):
        rowList = []
        for j in range(matInColumns):
            rowList.append(listOfMatrices[j + i * matInColumns])
        colList.append(np.concatenate(tuple(rowList), axis=1))
    finalMat = np.concatenate(tuple(colList), axis=0)
    finalMatList = []
    for i in range(len(finalMat)):
        for j in range(len(finalMat[i])):
            finalMatList.append(finalMat[i][j])
    return finalMatList

def triMat_to_fullMat(mode, triMatList):
    dim = int((np.sqrt(1 + 8*len(triMatList)) - 1)/2)
    matrix = np.zeros((dim, dim))
    if mode == 0:
        for i in range(dim):
            for j in range(i + 1):
                listEl = len(triMatList) - 1 - ((i*(i + 1))//2 + j)
                if i == j:
                    matrix[dim - 1 - i][dim - 1 - j] = triMatList[listEl]
                else:
                    matrix[dim - 1 - i][dim - 1 - j] = triMatList[listEl]
                    matrix[dim - 1 - j][dim - 1 - i] = triMatList[listEl]
    elif mode == 1:
        for i in range(dim):
            for j in range(i + 1):
                listEl = (i*(i + 1))//2 + j
                if i == j:
                    matrix[i][j] = triMatList[listEl]
                else:
                    matrix[i][j] = triMatList[listEl]
                    matrix[j][i] = triMatList[listEl]
    else:
        raise Exception('Mode should be 0 or 1, refer to the function for usage')
    matList = []
    for i in range(dim):
        for j in range(dim):
            matList.append(matrix[i][j])
    return matList
