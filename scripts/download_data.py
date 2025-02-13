#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import os

# 3rd party imports
from pyrfu import mms

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__license__ = "MIT"


os.makedirs("../data/", exist_ok=True)
mms.db_init(default="local", local="../data/")

def main():
    # For wavelet and SVD examples
    tint = ["2015-10-30T05:15:20.000", "2015-10-30T05:16:20.000"]
    mms_id = 1

    mms.download_data("r_gse_mec_srvy_l2", tint, mms_id)
    mms.download_data("b_gse_fgm_brst_l2", tint, mms_id)
    mms.download_data("e_gse_edp_brst_l2", tint, mms_id)
    mms.download_data("b_gse_scm_brst_l2", tint, mms_id)

    # For reduce example
    tint = ["2015-12-28T03:57:10", "2015-12-28T03:59:00"]
    mms_id = 2
    mms.download_data("b_dmpa_fgm_brst_l2", tint, mms_id)
    mms.download_ancillary("defatt", tint, mms_id)
    mms.download_data("pdi_fpi_brst_l2", tint, mms_id)

if __name__ == "__main__":
    main()
    