#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from pyrfu import mms, pyrf

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__license__ = "MIT"

# Initialize MMS client
mms.db_init(default="local", local="../data/")


def main():
    # Define time interval and spacecraft index
    tint = ["2015-10-30T05:15:20.000", "2015-10-30T05:16:20.000"]
    mms_id = 1

    # Load data
    # Load magnetic field FGM
    b_xyz = mms.get_data("b_gse_fgm_brst_l2", tint, mms_id)

    # Load electric field
    e_xyz = mms.get_data("e_gse_edp_brst_l2", tint, mms_id)

    # Some pre-processing
    # Rotate E and B into field-aligned coordinates
    e_fac = pyrf.convert_fac(e_xyz, b_xyz, [1, 0, 0])

    # Bandpass filter E and B waveforms
    fmin, fmax = [0.5, 1000]  # Hz

    # Compute wavelet transform (this is the heavy part)
    nf = 100
    e_cwt = pyrf.wavelet(e_fac, f=[fmin, fmax], n_freqs=nf)


if __name__ == "__main__":
    main()
