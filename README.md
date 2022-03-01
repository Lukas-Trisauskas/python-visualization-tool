### setup virtual environment

> to seperate packages for each project I would recommend creating a virtual environment

make sure you've cd into python-visualization-tool folder before executing this command
```
python -m venv venv-pvt
```
To actvitate the virtual environment
```
venv-pvt\Scripts\activate.bat
```
### installing requirements

make sure you've activated the virtual environment before installing the requirements
```
pip install -r requirements.txt
```
### folder structure
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
