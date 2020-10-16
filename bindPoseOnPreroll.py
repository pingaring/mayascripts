"""
Maya script to set pre-roll on bind pose at frame 900
unwantedAttributes is a list of control attributes we don't want to set to its default value
"""

import pymel.core as pm
import maya.cmds as cmds

holdPoseFrame = 985
bindPoseFrame = 900
firstAnimationFrame = 1000

# list of attributes we don't want to set to default values
UNWANTED_ATTRIBUTES = [
    "switchIkFk",
    "Hair",
    "Head",
    "Chest",
    "Front_Legs",
    "Back_Legs",
    "Body",
    "C_characterNode_CTL"
    ]

def suspend_viewport(boolean):
    if boolean == "suspendTrue":
        print("Suspending viewport refresh...")
        cmds.refresh(suspend=True)
        print("Viewport refresh suspended.")

    elif boolean == "suspendFalse":
        print("Unsuspending viewport refresh...")
        cmds.refresh(suspend=False)
        print("Viewport refresh unsuspended.")


def select_all_controls_from_rig():
    selection = cmds.ls(selection=True)
    namespaces = []
    for sel in selection:
        namespacer = sel.rpartition(':')[0]
        if namespacer not in namespaces:
            namespaces.append(namespacer)

    cmds.select(clear=True)
    for i in namespaces:
        cmds.select(i + ":*_CTL", add=True)


def set_attributes_to_default_values():
    selection = cmds.ls(long=True, selection=True)
    for controller in selection:
        attributes = cmds.listAttr(controller, keyable=True, unlocked=True, visible=True, write=True)
        if attributes is not None:
            for attribute in attributes:
                defaultValue = cmds.attributeQuery(attribute, node=(controller + "." + attribute), listDefault=True)
                if cmds.getAttr(controller + "." + attribute) != defaultValue and \
                        attribute not in UNWANTED_ATTRIBUTES and defaultValue is not None:

                    # try/except used to avoid errors when keying attributes with connected attributes
                    try:
                        cmds.setAttr((controller + "." + attribute), defaultValue[0])
                    except:
                        pass
    cmds.setKeyframe()


def bind_pose_on_preroll():
    # Main function of the bindPoseOnPreroll tool.
    with pm.UndoChunk():
        # We want to suspend viewport refresh to reduce potential viewport lag while the tool is running
        suspend_viewport("suspendTrue")
        select_all_controls_from_rig()
        cmds.currentTime(firstAnimationFrame, edit=True)

        # insert=True so we don't change the tangent curves
        cmds.setKeyframe(insert=True)
        cmds.currentTime(holdPoseFrame, edit=True)

        # We want to use "auto" tangent curves so we don't see unwanted interpolation between keys
        cmds.setKeyframe(inTangentType="auto", outTangentType="auto")
        cmds.currentTime(bindPoseFrame, edit=True)
        set_attributes_to_default_values()

        # Unsuspending the viewport
        suspend_viewport("suspendFalse")
        cmds.currentTime(firstAnimationFrame, edit=True)
        cmds.select(deselect=True)


if __name__ == "__main__":
    bind_pose_on_preroll()
