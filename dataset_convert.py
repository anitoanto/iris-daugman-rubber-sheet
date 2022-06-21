import sys
import os
import subprocess

folders = os.listdir("./dataset/16")
out_loc = "./out/16/localized/"
out_rub = "./out/16/rubber_sheet/"
if not os.path.exists(out_loc):
    os.makedirs(out_loc)
if not os.path.exists(out_rub):
    os.makedirs(out_rub)
for folder in folders:
    files = os.listdir("./dataset/16/" + folder)
    print(files)
    if not os.path.exists(out_loc + folder):
        os.makedirs(out_loc + folder)
    if not os.path.exists(out_rub + folder):
        os.makedirs(out_rub + folder)
    for file in files:
        print(file)
        subprocess.call(
            [
                "python",
                "./iris_rubber_sheet.py",
                "./dataset/16/" + folder + "/" + file,
                out_loc + folder + "/" + file,
                out_rub + folder + "/" + file,
            ],
            stdout=sys.stdout,
        )
