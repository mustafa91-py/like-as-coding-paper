import os

MAIN_FOLDER_NAME = M_F_N = "CodingPaper"
FOLDER_PATH = F_P = os.path.join(os.path.expanduser("~"), M_F_N)
if not os.path.exists(F_P):
    os.mkdir(F_P)
    os.startfile(F_P)