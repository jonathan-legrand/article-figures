import numpy as np

def to_matrix(vec):
    n = int(np.sqrt(len(vec) * 2))
    mat = np.zeros((n, n))
    mat[np.triu_indices(n, k=0)] = vec
    mat += mat.T
    np.fill_diagonal(mat, np.diag(mat) / 2)
    return mat

def binarize(matrix):
    pos_matrix = np.zeros_like(matrix)
    neg_matrix = np.zeros_like(matrix)

    pos_matrix[matrix > 0] = 1
    neg_matrix[matrix < 0] = 1
    return pos_matrix, neg_matrix

def split_pos_neg(matrix):

    pos_matrix = np.where(matrix > 0, matrix, 0)
    neg_matrix = np.where(matrix < 0, matrix, 0)
    return pos_matrix, neg_matrix

def degree_centrality(matrix, weighted=False):
    if weighted:
        pos_matrix, neg_matrix = split_pos_neg(matrix)
    else:
        pos_matrix, neg_matrix = binarize(matrix)
        
    pos_degree = pos_matrix.sum(axis=0)
    neg_degree = neg_matrix.sum(axis=0)
    return pos_degree, neg_degree
