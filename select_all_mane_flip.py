"""
Maya script to select all available horse mane controls from a selected rig.
"""

import maya.cmds as cmds
import pymel.core as pm

INVERSE_ATTRIBUTES = ["translateY", "rotateX", "rotateZ"]
MANE_CONTROL_SUFFIX = ":R_mane*_CTL"


def select_all_mane_controls():
    selection = cmds.ls(selection=True)

    # We want to create a list of unique character names so we can run the tool on more than one character at a time
    namespaces = []
    for sel in selection:
        namespacer = sel.rpartition(":")[0]
        if namespacer not in namespaces:
            namespaces.append(namespacer)

    cmds.select(clear=True)

    for namespace in namespaces:
        cmds.select(namespace + MANE_CONTROL_SUFFIX, add=True)


def inverse_value(controllerName, attributeName):
    """
    Because of the rig setup, we can flip the mane by inverting Translate Y, Rotate X, and Rotate Z values.
    """

    currentValue = cmds.getAttr(controllerName + "." + attributeName)
    inverseValue = float((currentValue - (currentValue * 2)))
    cmds.setAttr((controllerName + "." + attributeName), inverseValue)


def mane_flip():
    select_all_mane_controls()
    selection = cmds.ls(selection=True)
    with pm.UndoChunk():
        for controller in selection:
            attributes = cmds.listAttr(
                controller, keyable=True, unlocked=True, visible=True, write=True
            )
            for attribute in attributes:

                # Only invert attributes that are in INVERSE_ATTRIBUTES.
                if (
                    attribute in INVERSE_ATTRIBUTES
                    and cmds.getAttr(controller + "." + attribute) != 0
                ):
                    inverse_value(controller, attribute)

    cmds.select(clear=True)


if __name__ == "__main__":
    mane_flip()
