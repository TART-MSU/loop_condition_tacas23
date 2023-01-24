#!/bin/sh

# Execute all experiments in paper #68 of TACAS 2023:
# "Efficient Loop Conditions for Bounded Model Checking Hyperproperties"



time python bit_protocol/abp_AE.py
time python bit_protocol/abp_buggy_AE.py

# time python matrix_mult/matrix_AE.py
# time python matrix_mult/matrix_buggy_AE.py

# time python secure_compilation/CBF_AE.py
# time python secure_compilation/CBF_buggy_AE.py

# time python robust_path/rp_EA.py
# time python robust_path/rp_nosol_EA.py

# time python gcw/ss_EA.py
# time python gcw/ss_nosol_EA.py
