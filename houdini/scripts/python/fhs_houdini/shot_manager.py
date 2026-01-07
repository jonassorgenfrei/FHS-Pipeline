import hou
import os
from fhs.shotManager.shotManager import ShotManager

class Houdini_ShotManager(ShotManager):
    def __init__(self):
        """Initialize the Houdini Shot Manager GUI."""
        # construct parent
        super().__init__()

    def create_workfile(self, shot_name:str, shot_directory:str, start_frame:int, end_frame:int) -> str:
        """Create a Houdini .hip workfile for the shot.
        
        Args:
            shot_name (str): _name of the shot
            shot_directory (str): _path to the shot directory
            start_frame (int): _start frame of the shot
            end_frame (int): _end frame of the shot
        Returns:
            str: _path to the created .hip file
            
        """
        # create hip file 
        hip_file_path=os.path.join(shot_directory, f"{shot_name}.v001.hip")
        hou.hipFile.save(file_name=hip_file_path)
        
        self.init_scene(shot_name)
        
        # set frame range
        hou.playbar.setFrameRange(start_frame, end_frame)
        hou.playbar.setPlaybackRange(start_frame, end_frame)
        hou.setFrame(start_frame)
        
        # set env variables
        hou.hscript(f"setenv {FHS_Shot}={shot_name}")
        
        # save hip file after manual changes
        hou.hipFile.save(file_name=hip_file_path)
        return hip_file_path
    
    def init_scene(self, shot_name:str):
        """Initialize the Houdini scene for the shot.   
        Args:
            shot_name (str): _name of the shot
        """

        # clear hip file to create an empty one
        hou.hipFile.clear()
        
        sublayer = hou.node("/stage").createNode("sublayer")
        sublayer.setName(shot_name)
        # set to created hip file
        sublayer.parm("filepath1").set("$HIP/usd/shot.usda")
        sublayer.parm("reload").pressButton()
        
