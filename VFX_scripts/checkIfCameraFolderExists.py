"""
Script to iterate through sequences and shots and prints which shots don't have CAM folders.
"""


import os
import cProfile

# Directory containing all the sequence folders. We need to replace / with \\ when running on Windows
DEFAULT_FILEPATH = "/Users/Dylan/Documents/shots/"

# Sequences we want to ignore. Usually we're ignoring any test sequence as they wont contain correct CAM caches
IGNORED_SEQUENCES = []


def set_current_folder(filepath):
    return os.chdir(filepath)

def expected_sequence_folder(filepath, sequenceFolder):
    if not os.path.exists(os.path.join(filepath, sequenceFolder)):
        return False
    if not sequenceFolder[:2] == "sq":
        return False
    if sequenceFolder in IGNORED_SEQUENCES:
        return False
    else:
        return True


def expected_shot_folder(filepath, sequenceFolder, shotFolder):
    if not os.path.isdir(os.path.join(filepath, sequenceFolder, shotFolder)):
        return False
    if not shotFolder[:2] == "sq":
        return False
    if os.path.exists(os.path.join(filepath, sequenceFolder, shotFolder, "CAM")):
        return False
    if not os.path.exists(os.path.join(filepath, sequenceFolder, shotFolder, "ANI")):
        return False
    else:
        return True


def filter_folders(filepath):
    # Dictionary containing each sequence (key) and all shots (value) without a CAM folder.
    cameraNotExist = {}

    set_current_folder(filepath)
    sequenceFolders = os.listdir(".")

    # Start filtering through folders
    print("Filtering through folders in directory \"%s\"" % filepath)

    # Iterate through each sequence folder
    for sequenceFolder in sequenceFolders:

        # Don't iterate through non-folders, folders that don't start with "sq", and sequences found in ignoreSequences
        if expected_sequence_folder(filepath, sequenceFolder):
            shotFolders = os.listdir(filepath + sequenceFolder)

            # List of shots without CAM folders
            shotList = []

            # Iterate through each shot folder
            for shotFolder in shotFolders:
                if expected_shot_folder(filepath, sequenceFolder, shotFolder):
                    shotList.append(shotFolder)

            if shotList:
                cameraNotExist[sequenceFolder] = shotList

        print("%s complete" % sequenceFolder)

    for k, v in cameraNotExist.items():
        print("Sequence: %s, Shots: %s" % (k, v))


cProfile.run("filter_folders(DEFAULT_FILEPATH)")
