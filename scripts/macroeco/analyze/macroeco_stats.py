#!/usr/bin/python

'''
This module contains the statistical functions for analyzing macroeco
distributions

'''

from __future__ import division
import numpy as np
import scipy.stats as stats


__author__ = "Mark Wilber"
__copyright__ = "Copyright 2012, Regents of University of California"
__credits__ = "John Harte"
__license__ = None
__version__ = "0.1"
__maintainer__ = "Mark Wilber"
__email__ = "mqw@berkeley.edu"
__status__ = "Development"

def aic(neg_L, k, n, corrected=True):
    '''
    Calculates the AIC of a given model

    Parameters
    ----------
    neg_L : float
        The negative log likelihood of a model
    k : float
        The number of parameters of a model
    
    
   Returns
   -------
   : float
        AIC for a given model
    '''

    aic = (2 * neg_L) + (2 * k)
    return aic

def aicc(neg_LL, k, n):
    '''
    Calculates the corrected AIC of a given model

    Parameters
    ----------
    neg_LL : float
        The negative log likelihood of a model
    k : float
        The number of parameters of a model
    n : int
        Number of observations

    Returns
    -------
    : float
        AICc for a given model

    '''

    aic_value = aic(neg_LL, k)
    return aic_value + ((2 * k * (k + 1)) / (n - k - 1))

def aic_weights(aic_values):
    '''
    Calculates the aic_weights for a given set of models

    Parameters
    ----------
    aic_values : array-like object
        Array-like object containing AIC values from different models
    
    Returns
    -------
    : np.ndarray
        Array containing the relative AIC weights

    Notes
    -----
    AIC weights can be interpreted as the probability that a given model is the
    best model in comparison to the other models

    '''

    #NOTE: Check length of aic_values
    if type(aic_values) == float or type(aic_values) == int:
        raise ValueError("Parameter must be array-like object")
    aic_values = np.array(aic_values)
    minimum = np.min(aic_values) 
    delta = np.array([x - minimum for x in aic_values])
    values = np.exp(-delta / 2)
    weights = np.array([x / sum(values) for x in values])
    return weights

def ks_two_sample_test(data1, data2):
    '''Function uses the Kolomogrov-Smirnov two-sample test to determine if the
    two samples come from the same distribution.  Note that the KS-test is only
    valid for continuous distributions

    Parameters
    ----------
    data1 : array-like object
        Array-like object which contains a set of data to compare
    data2 : array-like object
        Array-like object which contains a set of data to compare

    Returns
    -------
    : tuple
        (D-statistic, two-sided p-value)

    '''
    
    data1 = np.array(data1)
    data2 = np.array(data2)
    return stats.ks_2samp(data1, data2)

def likelihood_ratio_test(neg_LL_null, neg_LL_alt, df):
    '''
    This functions compares of two nested models using the likelihood ratio
    test.

    Parameters
    ----------
    neg_LL_null : float
        The negative log-likelihood of the null model
    neg_LL_alt : float
        The negative log-likelihood of the alternative model
    df : int
        the degrees of freedom calulated as (number of free parameters in
        alternative model) - (number of free parameters in null model)
    
    Returns
    -------
    : tuple
        (test_statistic, p-value)

    Notes
    -----
    The LRT only applies to nested models.  
    '''

    test_stat = 2 * neg_LL_null - (2 * neg_LL_alt)
    return (test_stat, stats.chisqprob(test_stat, df))

