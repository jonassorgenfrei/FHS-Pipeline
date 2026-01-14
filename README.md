# FHS-Pipeline
Pipeline Repository for the FH Salzburg class Pipeline WS25

![pipeline_concept](docs/fig/pipeline_concept.png)
## Maya Installation Instruction
To install the toolset for maya create a userSetup.py file in 
`Documents/maya/<version>/scripts` and paste the follow code:

```python
import sys

sys.path.append("D:/Documents/Development/FH_Salzburg/pipeline/python") 
sys.path.append("D:/Documents/Development/FH_Salzburg/pipeline/maya")

from fhs_maya import startUp

startUp.startup()
```
NOTE replace the paths to this directory in sys.path.

## Houdini Installation Instruction
Copy the file houdini/fhs_pipeline.json into the folder:
`Documents/Houdini<version>/packages`
and adjust in the file the line:
```json
  "FHS_PIPELINE": "D:/Documents/Development/FH_Salzburg/pipeline"
```
to the location where this folder is. 

## Dev
Powershell create and source devenv
```powershell
python -m venv .\venv
.\venv\Scripts\Activate.ps1
```
If you get a policy error in PowerShell, run:
```powershell 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Required Packages: 
PySide6 & usd-core

Install PySide6 (or PySide2 for older dccs e.g. houdini 20.5)
```
pip install PySide6
```

Install Usd Core Python libraries 
```
pip install usd-core
```

When running the standalone python you might have to append the python directory to the python path to being able to import the fhs module. 

In the powershell the following command can be used for it.
```
$env:PYTHONPATH += ";d:\Documents\Development\FH_Salzburg\pipeline\python"
```

### Reloading Modules
To reload a module inside of a dccs like houdini you can do
```python
from importlib import reload
from fhs_houdini import shot_manager
reload(shot_manager)
```

## Shot Manager
For the Shot manager the [environment.py](python/fhs/shotManager/environment.py) file has to be adjusted that the `FHS_PIPELINE_ROOT` points to the correct location on your machine.
