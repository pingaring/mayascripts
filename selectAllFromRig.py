"""
Maya script to select all available controls from a selected rig
"""

import maya.cmds as cmds


def select_all_from_rig():
    characterNameFormat = "_CTL"

    # Props are using a different controller name format
    propNameFormat = "_ctrl"
    selection = cmds.ls(selection=True)

    # Using dictionaries to help determine if a rig is a character or prop using the dict value
    namespaces = {}
    for controller in selection:
        namespacer = controller.rpartition(':')[0]
        if namespacer not in namespaces:
            namespaces[namespacer] = controller

    cmds.select(clear=True)
    for k, v in namespaces.items():
        if characterNameFormat in v:
            cmds.select(k + ":*" + characterNameFormat, add=True)
        elif propNameFormat in v:
            cmds.select(k + ":*" + propNameFormat, add=True)


if __name__ == "__main__":
    select_all_from_rig()
