# usd utility functions for shot manager
# Make sure to have the USD python libs in your PYTHONPATH
# e.g. via pip install usd-core
import os
from pxr import Usd, Kind, UsdGeom

def create_shot_usd_structure(shot_usd_folder: str) -> str:
    """Create a basic USD structure for a shot.

    Args:
        shot_usd_folder (str): Path to the shot's USD folder.
        
    Returns:
        str: Path to the created shot USD file.
    """
    usd_file = os.path.join(f"{shot_usd_folder}", "shot.usda")
    
    stage = Usd.Stage.CreateNew(usd_file)

    prims = []
    
    for group in ["cameras", "characters", "fx", "props", "sets"]:
        prim = stage.DefinePrim(f"/{group}", "Xform")
        prim.SetKind(Kind.Tokens.group)
        prims.append(prim)

    UsdGeom.Camera.Define(stage, "/cameras/shot_cam")

    stage.GetRootLayer().Save()
    return usd_file