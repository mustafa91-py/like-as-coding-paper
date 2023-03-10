import os

MAIN_FOLDER_NAME = M_F_N = "CodingPaper"
FOLDER_PATH = F_P = os.path.join(os.path.expanduser("~"), M_F_N)
SCREEN_SHOT_PATH = SS_SHOT = os.path.join(F_P, "SS_SHOT")
for __ in [F_P, SS_SHOT]:
    if not os.path.exists(__):
        os.mkdir(__)
        os.startfile(__)


def create_folder_to_sshot(name: str):
    dir_ = os.path.join(SS_SHOT, name)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    return dir_


if os.path.exists(os.path.join("letters")):
    letters_path = os.path.join("letters")
else:
    letters_path = os.path.join("../letters")
# try:
#     letters_path = os.path.join("letters")
#     print(os.path.exists(letters_path))
# except FileNotFoundError:
#     letters_path = os.path.join(f"letters")
print(letters_path)