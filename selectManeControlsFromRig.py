"""
Maya script to select specified groom controls from a character.
"""

import maya.cmds as cmds

GROOM_CONTROL_SUFFIX = {
    "mane": ":R_mane*_CTL",
    "fringe": ":C_fringe*_CTL",
    "tail": ":C_tail*_CTL"
    }


def select_groom_controls(control):
    selection = cmds.ls(selection=True)
    namespaces = {}
    for i in selection:
        namespacer = i.rpartition(':')[0]
        if namespacer not in namespaces:
            namespaces[namespacer] = i

    cmds.select(clear=True)
    for k, v in namespaces.items():
        if ":R_mane" in v:
            cmds.select(k + control["mane"], add=True)
        elif ":C_fringe" in v:
            cmds.select(k + control["fringe"], add=True)
        elif ":C_tail" in v:
            cmds.select(k + control["tail"], add=True)


if __name__ == "__main__":
    select_groom_controls(GROOM_CONTROL_SUFFIX)
