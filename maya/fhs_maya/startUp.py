from maya import cmds, utils
from fhs.core.core import helloCore


def createSpheres(arg):
    for r in range(100):
        sphere = cmds.polySphere()
        cmds.move(r, 0, 0, sphere)
    helloCore()


def createMenu():
    menu_name = "fhsMenu"
    menu_label = "FHS Menu"

    if cmds.menu(menu_name, exists=True):
        cmds.deleteUI(menu_name)

    cmds.menu(menu_name, label=menu_label, parent="MayaWindow", tearOff=True)
    cmds.menuItem(label="Create 100 Spheres", command=createSpheres)
    
    
def startup():
    utils.executeDeferred(createMenu)