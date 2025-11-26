import hou
from fhs.core import core


def core_function():
    """Debug Function to check if the core module is getting loaded."""
    core.helloCore("Called from Houdini core")


def create_outs():
    """Create Out Nodes"""
    sel_nodes = hou.selectedNodes()
    for sel_node in sel_nodes:
        geo_container = sel_node.parent()
        new_null = geo_container.createNode("null", "OUT")
        # make black
        new_null.setColor(hou.Color(0, 0, 0))
        # make bulge shape
        new_null.setUserData("nodeshape", "bulge")
        new_null.setInput(0, sel_node)
        new_null.moveToGoodPosition()
