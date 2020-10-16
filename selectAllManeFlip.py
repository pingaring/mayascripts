""" Maya script to select all available mane controls from a selected rig. Script derived from selectAllFromRig"""

import maya.cmds as cmds
import pymel.core as pm

INVERSE_ATTRIBUTES = [
    "translateY",
    "rotateX",
    "rotateZ"
    ]
MANE_CONTROL_SUFFIX = ":R_mane*_CTL"


def select_all_mane_controls():
    selection = cmds.ls(selection=True)
    namespaces = []
    for sel in selection:
        namespacer = sel.rpartition(':')[0]
        if namespacer not in namespaces:
            namespaces.append(namespacer)

    cmds.select(clear=True)
    for i in namespaces:
        cmds.select(i + MANE_CONTROL_SUFFIX, add=True)


def inverse_value(controllerName, attributeName):
    currentValue = cmds.getAttr(controllerName + "." + attributeName)
    inverseValue = float((currentValue - (currentValue * 2)))
    cmds.setAttr((controllerName + "." + attributeName), inverseValue)


def mane_flip():
    select_all_mane_controls()
    selection = cmds.ls(selection=True)
    with pm.UndoChunk():
        for controller in selection:
            attributes = cmds.listAttr(controller, keyable=True, unlocked=True, visible=True, write=True)
            for attribute in attributes:
                if attribute in INVERSE_ATTRIBUTES and cmds.getAttr(controller + "." + attribute) != 0:
                    inverse_value(controller, attribute)

    cmds.select(clear=True)


if __name__ == "__main__":
    mane_flip()
