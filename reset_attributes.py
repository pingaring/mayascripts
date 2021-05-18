"""
Maya script to reset selected controls to their default values
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
    "Body",
]


def reset_attributes():
    with pm.UndoChunk():
        selection = cmds.ls(long=True, selection=True)

        # We are filtering through each controller and then filtering through each attribute from the above selection.
        for controller in selection:
            attributes = cmds.listAttr(
                controller, keyable=True, unlocked=True, visible=True, write=True
            )
            # Skipping over controllers that don't have any attributes.
            if attributes is not None:
                for attribute in attributes:

                    # Finding the default value of the attribute.
                    defaultValue = cmds.attributeQuery(
                        attribute, node=(controller + "." + attribute), listDefault=True
                    )

                    # We don't want to key attributes found in UNWANTED_ATTRIBUTES or if the value is already
                    # at the default value.
                    if (
                        cmds.getAttr(controller + "." + attribute) != defaultValue
                        and attribute not in UNWANTED_ATTRIBUTES
                        and defaultValue is not None
                    ):

                        # try/except used to avoid errors when keying attributes with connected attributes
                        # todo try to remove the try/except with better code
                        try:
                            cmds.setAttr(
                                (controller + "." + attribute), defaultValue[0]
                            )
                        except:
                            pass


if __name__ == "__main__":
    reset_attributes()
