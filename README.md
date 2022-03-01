#### Setup virtual environment (optional)

> I would recommend creating a virtual environment to seperate packages for each project

Make sure you cd to python-visualization-tool
```
python -m venv venv-pvt
```
Activate virtual environment
```
venv-pvt\Scripts\activate.bat
```
#### Installing requirements

Make sure you've activated the virtual environment before installing the requirements
```
pip install -r requirements.txt
```
#### Folder structure
```
python-visualization-tool/
├─ data/
│  ├─ anomaly_scores.npy
│  ├─ ground_truth.npy
├─ static/
│  ├─ images/
│  ├─ videos/
│  │  ├─ testset_3.mp4
│  ├─ gif/
│  │  ├─ selected/
├─ templates/
│  ├─ hover.html
├─ delete_frames.py
├─ extract_frames.py/
├─ main.py
```
