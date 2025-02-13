#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
from pyrfu import mms, pyrf

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__license__ = "MIT"

# Initialize MMS client
mms.db_init(default="local", local="../data/")


def main():
    r"""Compute 1D reduced ion velocity distribution function."""
    tint = ["2015-12-28T03:57:10", "2015-12-28T03:59:00"]
    mms_id = 2

    # Load data
    # Load magnetic field
    b_dmpa = mms.get_data("b_dmpa_fgm_brst_l2", tint, mms_id)

    # Load defatt (spacecraft attitude)
    defatt = mms.load_ancillary("defatt", tint, mms_id)

    # Load ion velocity distribution function
    vdf_i = mms.get_data("pdi_fpi_brst_l2", tint, mms_id)
    vdf_i_err = mms.get_data("pderri_fpi_brst_l2", tint, mms_id)
    vdf_i.data.data[vdf_i.data.data < 1.1 * vdf_i_err.data.data] = 0.0

    # Define coordinate system
    n_vec = np.array([0.9580, -0.2708, -0.0938])  # Shock normal
    n_vec /= np.linalg.norm(n_vec)
    b_u = [-1.0948, -2.6270, 1.6478]  # Upstream magnetic field
    t2_vec = np.cross(n_vec, b_u) / np.linalg.norm(
        np.cross(n_vec, b_u)
    )  # Tangent to the shock
    t1_vec = np.cross(t2_vec, n_vec)

    # To time series
    n_t = len(b_dmpa.time.data)
    n_gse = pyrf.ts_vec_xyz(b_dmpa.time.data, np.tile(n_vec[np.newaxis, :], [n_t, 1]))
    t1_gse = pyrf.ts_vec_xyz(b_dmpa.time.data, np.tile(t1_vec[np.newaxis, :], [n_t, 1]))
    t2_gse = pyrf.ts_vec_xyz(b_dmpa.time.data, np.tile(t2_vec[np.newaxis, :], [n_t, 1]))

    # Rotate vectors from GSE to DMPA
    n_dmpa = mms.dsl2gse(n_gse, defatt)
    t1_dmpa = mms.dsl2gse(t1_gse, defatt)
    t2_dmpa = mms.dsl2gse(t2_gse, defatt)

    # Prepare for the projection
    # Create rotation matrices
    nt1t2 = np.transpose(np.stack([n_dmpa.data, t1_dmpa.data, t2_dmpa.data]), [1, 2, 0])
    nt1t2 = pyrf.ts_tensor_xyz(b_dmpa.time.data, nt1t2)

    # Define the velocity grid
    vn_lim = np.array([-800.0, 800.0], dtype=np.float64)
    vg_1d_n = 1e3 * np.linspace(vn_lim[0], vn_lim[1], 100)

    # Reduce the ion VDF to 1D (actual heavy part)
    n_mc = 200
    f1dn = mms.reduce(vdf_i, projection_dim="1d", xyz=nt1t2, n_mc=n_mc, vg=vg_1d_n)
    f1dn.to_netcdf("../data/output_reduce.nc")


if __name__ == "__main__":
    main()
