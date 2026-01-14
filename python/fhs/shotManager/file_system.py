import os
from fhs.shotManager.environment import FHS_PIPELINE_ROOT


def create_shot_structure(
    shot_name: str, seq_name: str, base_path: str = FHS_PIPELINE_ROOT
) -> str:
    """Create the directory structure for a new shot.

    Args:
        shot_name (str): _name of the shot
        seq_name (str): _name of the sequence
        base_path (str, optional): _base path where the shots directory will be created. Defaults to FHS_PIPELINE_ROOT.

    Raises:
        ValueError: _if shot_name or seq_name is empty

    Returns:
        str: _path to the created shot directory
    """
    if not shot_name or not seq_name:
        raise ValueError("Both sequence and shot names must be provided.")

    # create shot directory structure
    shot_directory = os.path.join(base_path, "shots")

    if not os.path.exists(shot_directory):
        os.makedirs(shot_directory)

    # sequence directory
    seq_directory = os.path.join(shot_directory, seq_name)
    if not os.path.exists(seq_directory):
        os.makedirs(seq_directory)

    # shot directory
    shot_directory = os.path.join(seq_directory, shot_name)
    if not os.path.exists(shot_directory):
        os.makedirs(shot_directory)
    else:
        raise ValueError(f"Shot '{seq_name}_{shot_name}' already exists.")

    # subdirectories
    subdirs = ["animation", "cache", "comp", "layout", "models", "plates", "renders", "usd"]
    for subdir in subdirs:
        os.makedirs(os.path.join(shot_directory, subdir))

    return shot_directory
