"""
Maya script to select all available controls from a selected rig
"""

import maya.cmds as cmds


def select_all_from_rig():
    character_name_format = "_CTL"

    # Props are using a different controller name format
    prop_name_format = "_ctrl"
    selection = cmds.ls(selection=True)

    # Using dictionaries to help determine if a rig is a character or prop using the dict value
    namespaces = {}
    for controller in selection:
        namespacer = controller.rpartition(":")[0]
        if namespacer not in namespaces:
            namespaces[namespacer] = controller

    cmds.select(clear=True)

    for k, v in namespaces.items():
        if character_name_format in v:
            cmds.select(k + ":*" + character_name_format, add=True)
        elif prop_name_format in v:
            cmds.select(k + ":*" + prop_name_format, add=True)


if __name__ == "__main__":
    select_all_from_rig()
