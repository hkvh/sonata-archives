import logging
import os
import subprocess
import tempfile
from shutil import rmtree, copyfile

from directories import ROOT_DIR, LILYPOND_DIR

log = logging.getLogger(__name__)

# A useful preamble to anly lilypond file that properly crops all images (but also creates a lot of junk files)
LILYPOND_BOOK_PREAMBLE = '\include "lilypond-book-preamble.ly"'

# Using a manual temp directory
# since issues with using NamedTemporaryFile have appeared between how Windows and Mac handle them
TEMP_DIRECTORY = os.path.join(ROOT_DIR, 'lilypond_temp')


def render_lilypond_png_into_app_directory(ly_file_full_path: str, remove_temp_dir: bool = True) -> None:
    """
    Given a full path to the file like ~/path/to/file.ly, uses the shell to run lilypond on it and renders it into a
    png file. If successful, moves the rendered png to app/static/lilypond/ overwriting anything that was there.
    Puts all junk created in the process of rendering in a temp direcvtory that is removed by default.

    If the rendering failed, will raise LilypondRenderError.

    :param ly_file_full_path: an absolute path to the lilypond file
    :param remove_temp_dir: an optional parameter that if False will remove the root-level lilypond_temp directory
    containing the extraneous files made by this rendering process. Defaults to True.
    """

    ly_file_path_name, ly_file_name = os.path.split(ly_file_full_path)

    if not ly_file_name.endswith(".ly"):
        raise Exception("File {} provided was not a lilypond file!".format(ly_file_name))

    ly_file_stem = ly_file_name.split('.ly')[0]

    # Open the raw lily file and append a preamble to it if necessary
    log.info("Reading {} and appending the \"lilypond-book-preamble\" to it (if necessary)".format(ly_file_name))
    with open(ly_file_full_path, 'r') as f:
        ly_file_contents = f.read()

        if LILYPOND_BOOK_PREAMBLE not in ly_file_contents:
            ly_file_contents = LILYPOND_BOOK_PREAMBLE + "\n" + ly_file_contents

    log.debug(ly_file_contents)

    # Create a temp dir that we will purge (assuming the remove_temp_dir
    if not os.path.exists(TEMP_DIRECTORY):
        os.mkdir(TEMP_DIRECTORY)

    # The NamedTemporaryFile I wanted to use works different on windows since you can't open it after creating it
    # in a with block, but since I'm making a directory that I'm going to purge anyway, I'll just make it in there
    temp_ly_file_path = os.path.join(TEMP_DIRECTORY, ly_file_name)

    log.info("Writing results to tempfile {}".format(temp_ly_file_path))

    with open(temp_ly_file_path, 'w') as f:
        f.write(ly_file_contents)

    shell_command = 'lilypond -fpng -dresolution=400 {temp_fn}'.format(temp_fn=temp_ly_file_path)

    log.debug(shell_command)
    subprocess.call(shell_command, shell=True, cwd=TEMP_DIRECTORY)

    # Alternate command that suppresses error about GenericResourceDir but it requires you to sleep because
    # python will advance unexpectedly:
    #
    # subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE, cwd=temp_dir).stdout.readline()

    created_png_file_name = "{}.png".format(ly_file_stem)

    source = os.path.join(TEMP_DIRECTORY, created_png_file_name)
    dest = os.path.join(LILYPOND_DIR, created_png_file_name)

    # The only way source won't exist is if the lilypond render failed
    if os.path.exists(source):
        # Now copy the file from our temp directory to the source direcotry
        log.info("Copying {} to {}".format(created_png_file_name, LILYPOND_DIR))

        # Must remove destination since copy won't overwrite by default
        if os.path.exists(dest):
            os.remove(dest)
        copyfile(src=source, dst=dest)
        log.info("Removing the temporary directory and all other files non-png files created")
        if remove_temp_dir:
            rmtree(TEMP_DIRECTORY)
    else:
        if remove_temp_dir:
            rmtree(TEMP_DIRECTORY)
        raise LilypondRenderError("Error in lilypond code in \"{}\", no png generated.".format(ly_file_full_path))


class LilypondRenderError(Exception):
    """
    An exception for when the Lilypond file could not render
    """
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')
    render_lilypond_png_into_app_directory(os.path.join(ROOT_DIR, 'data/beethoven/beethoven5_1.ly'))
