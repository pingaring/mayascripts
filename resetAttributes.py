"""
Maya script to reset selected controls to their default values
unwantedAttributes is a list of control attributes we don't want to reset
"""

import pymel.core as pm
import maya.cmds as cmds

# list of attributes we don't want to reset
UNWANTED_ATTRIBUTES = [
    "switchIkFk",
    "Hair",
    "Head",
    "Chest",
    "Front_Legs",
    "Back_Legs",
    "Body"
    ]


def reset_attributes():
    with pm.UndoChunk():
        selection = cmds.ls(long=True, selection=True)
        for controller in selection:
            attributes = cmds.listAttr(controller, keyable=True, unlocked=True, visible=True, write=True)
            if attributes is not None:
                for attribute in attributes:
                    defaultValue = cmds.attributeQuery(attribute, node=(controller + "." + attribute), listDefault=True)
                    if cmds.getAttr(controller + "." + attribute) != defaultValue and \
                        attribute not in UNWANTED_ATTRIBUTES and defaultValue is not None:

                        # try/except used to avoid errors with attributes that contain connected values
                        try:
                            cmds.setAttr((controller + "." + attribute), defaultValue[0])
                        except:
                            pass


if __name__ == "__main__":
    reset_attributes()
