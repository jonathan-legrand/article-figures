import numpy as np
from scipy.stats import norm
from sklearn.utils import Bunch

def signed_stouffer(pvalues, original_stat):
    Zi = norm.isf(pvalues / 2) # Divide by 2 for two-tailed test
    k = len(pvalues)
    sign_mask = np.where(original_stat < 0, -1, 1)
    Z = np.sum(Zi * sign_mask) / np.sqrt(k)
    p_global = norm.sf(np.abs(Z)) * 2  # Convert to p-value
    res = Bunch(pvalue=p_global, statistic=Z)
    return res


def nonparametric_p_value(empirical_matrix, null_matrices, alternative='two-sided'):
    """
    Calculate the p-value for the empirical matrix against the null distribution.
    
    Parameters:
    - empirical_matrix: The observed difference matrix.
    - null_matrix: The null distribution of differences.
    - alternative: 'two-sided', 'greater', or 'less'.
    
    Returns:
    - p-value as a numpy array.
    """
    if alternative == 'two-sided':
        N = null_matrices.shape[0]
        pvalues_more = (np.sum(empirical_matrix > null_matrices, axis=0) + 1) / (N + 1)
        pvalues_less = (np.sum(empirical_matrix <  null_matrices, axis=0) + 1) / (N + 1)
        pvalues = np.minimum(pvalues_less, pvalues_more) * 2
        return np.clip(pvalues, 0, .9999) # Sometimes p-values can be slightly above 1 due to the *2 factor above
    else:
        raise ValueError("Alternative must be 'two-sided'")