#!/usr/bin/env python
"""
A module designed to render all lilypond files
"""
import glob
import logging
import os
from typing import List

from directories import DATA_DIR
from general_utils.lilypond_utils import render_lilypond_png_into_app_directory

log = logging.getLogger(__name__)


def render_all_lilypond(filenames_list: List[str] = None, remove_temp_dir: bool = True) -> None:
    """
    This function recursively iterates over and all lilypond files in the 'data' folder and renders them all into pngs
    that it moves to the app directory.

    Will throw an error if any single lilypond file does not render properly.

    If you provide a filename_list, will skip all files whose name (i.e. the filename itself, not the full path) are
    not in the filename list (this is to make it easier to focus on only the specific files you care about)

    :param filenames_list: an optional parameter that if provided will filter the files considered to those in the list
    (no need to include the .ly since all files have it)
    :param remove_temp_dir: an optional parameter that if False will not removes the root-level lilypond_temp directory
    containing the extraneous files made by this rendering process. Defaults to True.
    """

    # Get all lilypond files recursively under the data dir
    data_file_full_path_list = glob.glob(os.path.join(DATA_DIR, '**/*.ly'), recursive=True)

    log.info('#' * 40)
    log.info('#' * 40)
    log.info('#' * 40)
    log.info("RENDERING ALL LILYPOND FILES")
    log.info('#' * 40)
    log.info('#' * 40)
    log.info('#' * 40 + "\n")

    for data_file_full_path in data_file_full_path_list:

        path_name, file_name = os.path.split(data_file_full_path)

        # If no list provided, run everything, else check if the filename (minus .ly since we know all files have it)
        # is in the filename_list
        if filenames_list is None or file_name.split('.ly')[0] in filenames_list:
            log.info('\n' * 5)
            log.info('#' * 150)
            log.info('#' * 150)
            log.info("PROCESSING: {}".format(file_name))
            log.info('#' * 150)
            log.info('#' * 150)

            render_lilypond_png_into_app_directory(data_file_full_path, remove_temp_dir=remove_temp_dir)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')

    filenames_list = [
        'beethoven2_1',
    ]

    # Comment this out to use the filename_list
    # filenames_list = None

    render_all_lilypond(filenames_list=filenames_list, remove_temp_dir=True)


