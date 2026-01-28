# usd utility functions for shot manager
# Make sure to have the USD python libs in your PYTHONPATH
# e.g. via pip install usd-core
import os
from pxr import Usd, Kind, UsdGeom

def create_shot_usd_structure(shot_usd_folder: str, shot_name: str, start_frame: int, end_frame: int) -> str:
    """Create a basic USD structure for a shot.

    Args:
        shot_usd_folder (str): Path to the shot's USD folder.
        shot_name (str): Name of the shot.
        start_frame (int): Start frame of the shot.
        end_frame (int): End frame of the shot.
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
    
    # add shot prim
    shot = stage.DefinePrim("/shot", "Scope")

    shot.SetCustomDataByKey("startFrame", start_frame)
    shot.SetCustomDataByKey("endFrame", end_frame)
    shot.SetCustomDataByKey("fps", 24)
    shot.SetCustomDataByKey("shotName", shot_name)

    stage.GetRootLayer().Save()
    return usd_file