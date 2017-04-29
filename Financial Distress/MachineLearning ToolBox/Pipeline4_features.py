# 4. Generate Features/Predictors: For this assignment, you should 
# write one function that can discretize a continuous variable and 
# one function that can take a categorical variable and create binary/dummy 
# variables from it. Apply them to at least one variable each in this data.
    
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import pylab as pl

def display_importance(df, label, features):
    '''
    Given dataframe, label, and list of features,
    plot a graph to rank variable importance
    '''
    clf = RandomForestClassifier()
    clf.fit(df[features], df[label])
    importances = clf.feature_importances_
    sorted_idx = np.argsort(importances)
    padding = np.arange(len(features)) + 0.5
    pl.barh(padding, importances[sorted_idx], align='center')
    pl.yticks(padding, np.asarray(features)[sorted_idx])
    pl.xlabel("Relative Importance")
    pl.title("Variable Importance")
    
def discretize(df, varname, nbins, method='quantile'):
    '''
    Discretizes given "varname" into "nbins".

    Inputs:
            - df: name of pandas DataFrame
            - varname: name of variable to be discretized
            - nbins: number of categories to create
            - method: can be 'quantile', 'uniform', 'linspace' or 'logspace'

    Returns: nothing. Modifies "df" in place
    '''
    assert varname in df.columns, "Column '{}' not found in DataFrame".format(varname)

    assert len(df[varname].value_counts()) > nbins, "Number of bins too large"

    if method == 'quantile':
        df[varname + '_cat'] = pd.qcut(df[varname], nbins)
    elif method == 'uniform':
        df[varname+'_cat'] = pd.cut(df[varname], nbins)
    elif method == 'linspace':
        minval = min(df[varname])
        maxval = max(df[varname])
        bins = np.linspace(minval, maxval, nbins+1)
        df[varname+'_cat'] = pd.cut(df[varname], bins, include_lowest=True)
    elif method == 'logspace':
        minval = min(df[varname])
        maxval = max(df[varname])
    else:
        raise ValueError('{} not currently avaliable'.format(method))
        
        assert maxval > 0, 'Column {} has only negative or zero numbers'.format(varname)

        if minval <= 0:
            print('Warning, {} has negative or zero values'.format(varname))
            minval = 0.0001

        bins = np.logspace(np.log10(minval), np.log10(maxval), num = nbins+1)
        df[varname+'_cat'] = pd.cut(df[varname], bins, include_lowest=True)


def gen_dummies(df, varnames, drop=True):
    '''
    Given a dataframe and certain column, returns a set of dummies
    '''
    for v in varnames:
        binary_cols = pd.get_dummies(df[v], v)
        df = pd.merge(df, 
                      binary_cols, 
                      left_index=True, 
                      right_index=True, 
                      how='inner')
        ## Carlos' method
        for i, value in enumerate(df[col].unique()):
            df[col + '_{}'.format(i)] = df[col] == value
        ##
    
    if drop:
        df.drop(cat_cols, inplace=True, axis=1)

def binarize_categories(df, cat_cols, drop=True):
    '''
    df: a pandas dataframe
    cat_cols: list of column names to generate indicator columns for
    drop: a bool. If true, drop the original category columns
    Returns: the modified dataframe
    '''
    for col in cat_cols:
        binary_cols = pd.get_dummies(df[col], col)
        df = pd.merge(df, 
                      binary_cols, 
                      left_index=True, 
                      right_index=True, 
                      how='inner')
    if drop:
        df.drop(cat_cols, inplace=True, axis=1)
    return df