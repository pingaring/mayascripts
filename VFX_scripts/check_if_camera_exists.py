"""
Script to iterate through sequences and shots and prints which shots don't have CAM folders.
"""

import os
import cProfile

BASE_PROJECT_PATH = "/Users/Dylan/Documents/dev_project/publish/sequences/"
IGNORE_SEQUENCES = []


class BaseCameraChecker(object):
    def __init__(self, camera_name="CAM", base_path=None, ignored_sequences=None):
        self.camera_name = camera_name
        self.base_path = base_path
        self.ignored_sequences = ignored_sequences

    def get_shot_status(self, shot):
        raise NotImplementedError


class CheckCameraFolderExists(BaseCameraChecker):
    def expected_sequence_folder(self, sequence_folder):
        """
        We are only trying to return True on expected sequence folders.
        """

        if sequence_folder in self.ignored_sequences:
            return False
        if not sequence_folder.startswith("sq"):
            return False
        if not os.path.exists(os.path.join(self.base_path, sequence_folder)):
            return False
        else:
            return True

    def expected_shot_folder(self, sequence_folder, shot_folder):
        """
        We are only trying to return True if the "CAM" folder doesn't exist and "ANI" folder does exist. The "CAM" folder
        only gets created once the camera is published, and we check if "ANI" exists so we know the animation department
        has started the shot.
        """

        if not shot_folder.startswith("sq"):
            return False
        if os.path.exists(
            os.path.join(self.base_path, sequence_folder, shot_folder, self.camera_name)
        ):
            return False
        if not os.path.exists(
            os.path.join(self.base_path, sequence_folder, shot_folder, "ANI")
        ):
            return False
        else:
            return True

    def run_filter_folders(self):
        # Dictionary that will contain our keys (each sequence name) and value (each shot number).
        camera_not_exist = {}

        # int of how many shots don't have caches.
        num_shots_no_camera = 0

        sequence_folders = os.listdir(self.base_path)

        print('Filtering through folders in directory "%s"' % self.base_path)

        # Filter through each sequence folder from base_path.
        for sequence_folder in sequence_folders:

            # Check if sequence_folder is actually a sequence.
            if self.expected_sequence_folder(sequence_folder):
                shot_folders = os.listdir(self.base_path + sequence_folder)

                # List of shots without caches that will be used as the dict value for anim_cache_not_exist.
                shots_without_cameras = []

                # Filter through each shot folder from shot_folders.
                for shot_folder in shot_folders:

                    # Check if shot_folder has a published camera.
                    if self.expected_shot_folder(sequence_folder, shot_folder):
                        shots_without_cameras.append(shot_folder)
                        num_shots_no_camera += 1

                if shots_without_cameras:
                    camera_not_exist[sequence_folder] = shots_without_cameras

            print("%s complete" % sequence_folder)

        for sequence, shot in camera_not_exist.items():
            print("Sequence: %s, Shots: %s" % (sequence, shot))

        print("Number of shots without cameras: %d" % num_shots_no_camera)


if __name__ == "__main__":
    check_camera1 = CheckCameraFolderExists(
        base_path=BASE_PROJECT_PATH, ignored_sequences=IGNORE_SEQUENCES
    )
    # cProfile.run("check_camera1.run_filter_folders()")
    check_camera1.run_filter_folders()
