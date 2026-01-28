from maya import cmds
import os
from fhs.shotManager.shotManager import ShotManager
try:
    from PySide6 import QtWidgets
except ModuleNotFoundError:
    from PySide2 import QtWidgets
    

class Maya_ShotManager(ShotManager):
    def __init__(self):
        """Initialize the Maya Shot Manager GUI."""
        # construct parent
        super().__init__()

    def create_workfile(self, shot_name:str, shot_directory:str, start_frame:int, end_frame:int) -> str:
        """Create a Maya .ma workfile for the shot.
        
        Args:
            shot_name (str): _name of the shot
            shot_directory (str): _path to the shot directory
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        Returns:
            str: _path to the created .ma file
            
        """
        # create ma file 
        ma_file_path=os.path.join(shot_directory, f"{shot_name}.v001.ma")
        
        cmds.file(rename=ma_file_path)
        cmds.file(save=True, type="mayaAscii")  
        
        self.init_scene(shot_directory, shot_name, start_frame, end_frame)
        
        # save ma file after manual changes
        cmds.file(save=True, type="mayaAscii")

        return ma_file_path
    
    def open_workfile(self, item: QtWidgets.QListWidgetItem) -> None:
        """Open the selected workfile in the DCC application."""
        workfile_path = item.text()
        
        if workfile_path.endswith(".ma"):
            cmds.file(workfile_path, open=True, force=True)
            self.close()
        else:
            super().open_workfile(item)

    def init_scene(self, shot_directory:str, shot_name:str, start_frame:int, end_frame:int):
        """Initialize the Maya scene for the shot.   
        Args:
            shot_directory (str): _path to the shot directory
            shot_name (str): _name of the shot
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        """
        # set frame range
        cmds.playbackOptions(min=start_frame, max=end_frame)
        cmds.currentTime(start_frame)
        
        # create USD stage
        stage = cmds.createNode("mayaUsdProxyShape", name="usdStageShape")
        usd_path=os.path.join(shot_directory, "usd", "shot.usda").replace("\\", "/")
        cmds.setAttr(stage + ".filePath", usd_path, type="string")

