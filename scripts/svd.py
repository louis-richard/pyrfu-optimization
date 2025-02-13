#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
from pyrfu import mms, pyrf


def main():
    # Define time interval and spacecraft index
    tint = ["2015-10-30T05:15:42.000", "2015-10-30T05:15:54.00"]
    tint_long = pyrf.extend_tint(tint, [-100, 100])
    mms_id = 1

    # Load data
    r_xyz = mms.get_data("r_gse_mec_srvy_l2", tint_long, mms_id)
    b_xyz = mms.get_data("b_gse_fgm_brst_l2", tint, mms_id)
    e_xyz = mms.get_data("e_gse_edp_brst_l2", tint, mms_id)
    b_scm = mms.get_data("b_gse_scm_brst_l2", tint, mms_id)

    # Perform the polarization analysis (this is the heavy part)
    polarization = pyrf.ebsp(
        e_xyz,
        b_scm,
        b_xyz,
        b_xyz,
        r_xyz,
        freq_int=[10, 4000],
        polarization=True,
        fac=True,
    )


if __name__ == "__main__":
    main()
