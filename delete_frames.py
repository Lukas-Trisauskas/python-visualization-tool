import os
import glob

def empty_dir():
    os.remove("../python-visualization-tool/data/data.csv")
    count = 0
    my_dir = glob.glob("../python-visualization-tool/static/images/*.jpg")
    file_count = len(my_dir)

    for file in my_dir:
        os.remove(file)
empty_dir()