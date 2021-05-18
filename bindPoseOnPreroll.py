"""
Maya script to set pre-roll on bind pose at frame 900 assuming character controls are selected.
"""

import pymel.core as pm
import maya.cmds as cmds

HOLD_POSE_FRAME = 985
BIND_POSE_FRAME = 915
FIRST_ANIMATION_FRAME = 1000

# List of attributes we don't want to set to default values.
UNWANTED_ATTRIBUTES = [
    "switchIkFk",
    "Hair",
    "Head",
    "Chest",
    "Front_Legs",
    "Back_Legs",
    "Body",
    "C_characterNode_CTL",
]


class BindPoseOnPreroll:
    def __init__(self):
        pass

    def select_all_controls_from_rig(self):
        selection = cmds.ls(selection=True)

        # We want to create a list of unique character names so we can run the tool on more than one character at a time
        namespaces = []

        for sel in selection:
            namespacer = sel.rpartition(":")[0]
            if namespacer not in namespaces:
                namespaces.append(namespacer)

        cmds.select(clear=True)

        for namespace in namespaces:
            cmds.select(namespace + ":*_CTL", add=True)

    def set_attributes_to_default_values(self, key_tangent="linear"):
        selection = cmds.ls(long=True, selection=True)

        # We are filtering through each controller and then filtering through each attribute from the above selection
        for controller in selection:
            attributes = cmds.listAttr(
                controller, keyable=True, unlocked=True, visible=True, write=True
            )

            # Skipping over controllers that don't have any attributes
            if attributes is not None:
                for attribute in attributes:

                    # Finding the default value of the attribute
                    defaultValue = cmds.attributeQuery(
                        attribute, node=(controller + "." + attribute), listDefault=True
                    )

                    # We don't want to key attributes found in UNWANTED_ATTRIBUTES or if the value is already
                    # at the default value
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

        cmds.setKeyframe(outTangentType=key_tangent)

    def run_bind_pose_on_preroll(self):
        # Main function of the bindPoseOnPreroll tool.
        with pm.UndoChunk():

            # We want to suspend viewport refresh to reduce potential viewport lag while the tool is running
            cmds.refresh(suspend=True)

            # Select all available controls on the selected characters
            self.select_all_controls_from_rig()

            # Moving to and setting a key at the first animation frame
            cmds.currentTime(FIRST_ANIMATION_FRAME, edit=True)
            cmds.setKeyframe(insert=True, inTangentType="auto")

            # Moving to and setting a key at the hold pose frame
            cmds.currentTime(HOLD_POSE_FRAME, edit=True)
            cmds.setKeyframe(inTangentType="linear", outTangentType="auto")

            # Moving to and setting a key at the bind pose frame using default controller values
            cmds.currentTime(BIND_POSE_FRAME, edit=True)
            self.set_attributes_to_default_values()

            # Unsuspending the viewport
            cmds.refresh(suspend=False)

            cmds.currentTime(FIRST_ANIMATION_FRAME, edit=True)
            cmds.select(deselect=True)


if __name__ == "__main__":
    preroll = BindPoseOnPreroll()
    preroll.run_bind_pose_on_preroll()
