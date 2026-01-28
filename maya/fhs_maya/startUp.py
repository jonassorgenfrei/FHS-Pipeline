from maya import cmds, utils
from fhs.core.core import helloCore

shot_manager_window = None

def createSpheres(arg):
    for r in range(100):
        sphere = cmds.polySphere()
        cmds.move(r, 0, 0, sphere)
    helloCore()

def open_shot_manager(arg):
    global shot_manager_window
    from fhs_maya.shot_manager import Maya_ShotManager

    try:
        shot_manager_window.close()
        shot_manager_window.deleteLater()
    except:
        pass

    shot_manager_window = Maya_ShotManager()
    shot_manager_window.show()

def createMenu():
    menu_name = "fhsMenu"
    menu_label = "FHS Menu"

    if cmds.menu(menu_name, exists=True):
        cmds.deleteUI(menu_name)

    cmds.menu(menu_name, label=menu_label, parent="MayaWindow", tearOff=True)
    cmds.menuItem(label="Create 100 Spheres", command=createSpheres)
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Open Shot Manager", command=open_shot_manager)
    
def startup():
    utils.executeDeferred(createMenu)