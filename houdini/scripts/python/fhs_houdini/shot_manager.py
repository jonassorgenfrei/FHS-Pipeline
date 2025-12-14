import hou
import os
from fhs.shotManager.shotManager import ShotManager

class Houdini_ShotManager(ShotManager):
    def __init__(self):
        # construct parent
        super().__init__()

    def create_workfile(self, shot_name:str, shot_directory:str) -> str:
        self.init_scene(shot_name)
        hip_file_path=os.path.join(shot_directory, f"{shot_name}.hip")
        hou.hipFile().save(hip_file_path)
        return hip_file_path
    
    def init_scene(self, shot_name:str):
        sublayer = hou.node("/stage").createNode("sublayer")
        sublayer.setName(shot_name)
