"""
Script to iterate through sequences and shot folders and prints which shots don't have the most up to date anim caches
"""

import os
import cProfile
import platform

BASE_PROJECT_PATH = "/Users/Dylan/Documents/dev_project/publish/sequences/"
IGNORE_SEQUENCES = []

if platform.system() == "Windows":
    ANIM_FOLDERS_STRUCTURE = "ANI\\Anim\\maya\\"
else:
    ANIM_FOLDERS_STRUCTURE = "ANI/Anim/maya/"


class BaseAnimCacheChecker(object):
    def __init__(self, base_path=None, ignored_sequences=None):
        self.base_path = base_path
        self.ignored_sequences = ignored_sequences

    def get_shot_status(self, shot):
        raise NotImplementedError


class CheckAnimCacheExists(BaseAnimCacheChecker):
    def expected_sequence_folder(self, sequence_folder):
        """
        We are only trying to return True on expected sequence folders
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
        We are only trying to return True on expected shot folders
        """

        if not shot_folder.startswith("sq"):
            return False
        if not os.path.exists(
            os.path.join(self.base_path, sequence_folder, shot_folder, "ANI")
        ):
            return False
        else:
            return True

    def check_cache_not_exists(self, sequence_folder, shot_folder):
        """
        Anim caches live in the below directory so we're filtering into a shot folder hierarchy to find at least
        one cache file.

        e.g. /dev_project/publish/sq1200/sq1200_sh0050/ANI/Anim/maya/v089/cache/"
        """

        path_to_publish = os.path.join(
            self.base_path, sequence_folder, shot_folder, ANIM_FOLDERS_STRUCTURE
        )

        # Checking if the given sequence name and shot number has an existing folder
        # e.g. /dev_project/publish/sq1200/sq1200_sh0050/ANI/Anim/maya/
        if os.path.exists(path_to_publish):

            # publish_folders is a list of all possible publish versions, e.g. ["v001", "v002", "v003"]
            publish_folders = os.listdir(path_to_publish)

            # Reverse publish_folders so the highest folder version number gets looped first.
            for publish_folder in sorted(publish_folders, reverse=True):

                # Sometimes there are random unrelated folders found here.
                if publish_folder.startswith("v"):

                    # v000 is always an empty folder.
                    if publish_folder == "v000":
                        return False
                    else:
                        latest_folder = publish_folder
                        break

            path_to_pre_cache = os.path.join(
                self.base_path,
                sequence_folder,
                shot_folder,
                ANIM_FOLDERS_STRUCTURE,
                latest_folder,
            )
            pre_cache_folder = os.listdir(path_to_pre_cache)

            # Check if there's at least one "cache" folder.
            if pre_cache_folder.count("cache"):
                path_to_cache = os.path.join(
                    self.base_path,
                    sequence_folder,
                    shot_folder,
                    ANIM_FOLDERS_STRUCTURE,
                    latest_folder,
                    "cache",
                )

                # List of what's inside the "cache" folder.
                cache_folder = os.listdir(path_to_cache)

                # If the latest publish version was published and cached correctly, there should be more than 1 file
                # inside the "cache" folder. The ".bat" file is used to create our caches, so if at least that file
                # exists and the length of cache_folder is <= 1 then we can assume the caching job has failed or still
                # on the farm queue.
                if len(cache_folder) <= 1 and os.path.exists(path_to_cache):
                    for i in pre_cache_folder:
                        if i.endswith(".bat"):
                            return True

    def run_filter_folders(self):
        # Dictionary that will contain our keys (each sequence name) and value (each shot number).
        anim_cache_not_exist = {}

        # int of how many shots don't have caches.
        num_shots_no_caches = 0

        sequence_folders = os.listdir(self.base_path)

        print('Filtering through folders in directory "%s"' % self.base_path)

        # Filter through each sequence folder from base_path.
        for sequence_folder in sequence_folders:

            # Check if sequence_folder is actually a sequence.
            if self.expected_sequence_folder(sequence_folder):
                shot_folders = os.listdir(self.base_path + sequence_folder)

                # List of shots without caches that will be used as the dict value for anim_cache_not_exist.
                shots_without_caches = []

                # Filter through each shot folder from shot_folders.
                for shot_folder in shot_folders:

                    # Check if shot_folder is actually a shot.
                    if self.expected_shot_folder(sequence_folder, shot_folder):

                        # Check if caches don't exist.
                        if self.check_cache_not_exists(sequence_folder, shot_folder):
                            shots_without_caches.append(shot_folder)
                            num_shots_no_caches += 1

                if shots_without_caches:
                    anim_cache_not_exist[sequence_folder] = shots_without_caches

            print("%s complete" % sequence_folder)

        for sequence, shot in anim_cache_not_exist.items():
            print("Sequence: %s, Shots: %s" % (sequence, shot))

        print("Number of shots without anim caches: %d" % num_shots_no_caches)


if __name__ == "__main__":
    check_anim_cache1 = CheckAnimCacheExists(
        base_path=BASE_PROJECT_PATH, ignored_sequences=IGNORE_SEQUENCES
    )
    cProfile.run("check_anim_cache1.run_filter_folders()")
    # check_anim_cache1.run_filter_folders()
