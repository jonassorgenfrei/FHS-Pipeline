# FHS-Pipeline
Pipeline Repository for the FH Salzburg class Pipeline WS25


## Maya Installation Instruction
To install the toolset for maya create a userSetup.py file in 
Documents/maya/<version>/scripts and paste the follow code:

```python
import sys

sys.path.append("D:/Documents/Development/FH_Salzburg/pipeline/python") 
sys.path.append("D:/Documents/Development/FH_Salzburg/pipeline/maya")

from fhs_maya import startUp

startUp.startup()
```
NOTE replace the pathes to this directory.