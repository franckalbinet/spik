# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_loading.ipynb.

# %% auto 0
__all__ = ['load_mir', 'load_nir']

# %% ../nbs/00_loading.ipynb 2
import pandas as pd
import fastcore.all as fc
from pathlib import Path
import re

# %% ../nbs/00_loading.ipynb 3
def load_mir(src_dir):
    """
    Load MIR spectra of K spiked soil samples.
    
    Parameters:
    src_dir (Path-like object): Directory containing the spectra files.
    
    Returns:
    tuple: Tuple containing the array of absorbance values, 
           array of wavenumbers (columns), and array of sample names (rows).
    """
    pattern = r'-\d-\d$'
    fnames = [f for f in src_dir.ls() if re.search(pattern, f.stem)]
    
    dfs = [pd.read_csv(fname, header=None, names=['wavenumber', 'absorbance'])
           .query('649 < wavenumber < 4000')
           .assign(name=fname.stem) for fname in fnames]
    
    df_combined = pd.concat(dfs).pivot_table(values='absorbance', index='name', columns='wavenumber')
    
    return df_combined.values, df_combined.columns.values, df_combined.index.values.astype('U')


# %% ../nbs/00_loading.ipynb 6
def load_nir(fname):
    """
    Load NIR spectra of K spiked soil samples.
    
    Parameters:
    fname (str or Path-like object): File name or path of the Excel file.
    
    Returns:
    tuple: Tuple containing the array of spectral values, 
           array of wavenumbers (columns), and array of sample names (rows).
    """
    df = pd.read_excel(fname, sheet_name='Results', index_col='Sample ID')
    df.index.name = 'name'
    df.columns.name = 'wavenumber'
    
    return df.values, df.columns.values, df.index.values.astype('U')
