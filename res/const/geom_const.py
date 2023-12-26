import numpy as np

R_REACTOR = 0.25
H_REACTOR = 0.325
X_NORM = [1.0,0,0]
Y_NORM = [0,1.0,0]
Z_NORM = [0,0,1.0]

R_DN0 = 0.197
H_DNO = 0.038

R_WAFER = 0.15
H_WAFER = 0.001

R_INLET = 0.00215
L_INLET = 0.01
DELTA_PHI = np.pi*0.25
R_LOC_INLET = 0.2245
H_LOC_INLET = 0.3367
Z_PHI = 0.585

R_CON_DOWN = R_REACTOR - 0.0179
R_CON_UP = 0.2207
H_CON = 0.01985

ALPHA = np.arctan((1.0 * H_CON) / (1.0 * (R_CON_DOWN - R_CON_UP)))
SIN_ALPHA = np.sin(ALPHA)
COS_ALPHA = np.cos(ALPHA)


TEST_H = 0.5
TEST_W = 0.8
ALPHA_OUT = 0.8
ALPHA_IN = 0.4

