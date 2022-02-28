from timeit import default_timer as timer
import cv2
import pandas as pd
import numpy as np
import click

start = timer()
score = np.load("../python-visualization-tool/data/anomaly_scores.npy").tolist()
round_score = [round(value, 3) for value in score]
ground_truth = np.load("../python-visualization-tool/data/ground_truth.npy").tolist()

data = { 'frame': [], 'image': [], 'score': round_score, 'ground_truth': ground_truth}

source = "../python-visualization-tool/static/videos/testset_3.mp4"
cap = cv2.VideoCapture(source)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

copy = frame_count
count = 0

with click.progressbar(length=frame_count, show_pos=True, label="Extracting frames", show_percent=True) as bar:
    for i in bar:
        ret, frame = cap.read()
        if ret:
            path = "../python-visualization-tool/static/images/"
            name = f"frame{count}.jpg"
            data['frame'].append(f"frame{count}")
            data['image'].append('python-visualization-tool/static/images/' + name)
            cv2.imwrite(path + name, frame)
        else:
            cap.release()
            break
        count += 1

df = pd.DataFrame(data, columns = ['frame', 'image', 'score', 'ground_truth'], dtype=float)
print(df)
df.to_csv('../python-visualization-tool/data/data.csv')


end = timer()
print(f"Frames extracted: {count}")
print(f"Elapsed time: {int(end - start)} seconds")

f = open("log.txt", "a")
f.write(f"Frames extracted: {count}\n")
f.write(f"Elapsed time: {int(end - start)}\n")
f.close()