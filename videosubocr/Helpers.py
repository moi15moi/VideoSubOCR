import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from pysubs2 import SSAEvent, SSAFile
from rich.console import Console
from rich.progress import Progress
from .Subs import ASS_DEFAULT
from typing import Dict

# Just to be safe, I floor 32767 https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa or https://stackoverflow.com/a/2381726/15835974
WINDOWS_CHARACTER_LIMIT = 32700


def verifyIfFileExist(path: Path, canBeNone: bool = False) -> Path:
    """
    Parameters:
        path (Path): File path.
        canBeNone (bool): If true and the path is None, it won't quit the program.
    Returns:
        If the file exist, it return the absolute path else, it quit the program.
    """
    if canBeNone and path is None:
        return path
    elif path is None or not path.is_file():
        sys.exit(
            Console().print(f'Error: the path "{path}" is not valid.', style="red1")
        )
    else:
        if not os.path.isabs(path):
            return os.path.abspath(path)
        return path


def parseDependency(dependencyName: str, possibleDependencyPath: Path = None):
    """
    Parameters:
        dependencyName (str): The name of the dependency program. Ex: VideoSubFinder.
        possibleDependencyPath (Path): The possible location of the program.
    Returns:
        If the program is found, it return the program absolute path, else it quit the program.
    """

    dependencyPath = ""

    if possibleDependencyPath is None:
        dependencyPath = shutil.which(dependencyName)
        if not dependencyPath:
            sys.exit(
                Console().print(
                    f"Error: {dependencyName} in not in your environnements variable, add it or specify the path with --{dependencyName}.",
                    style="red1",
                )
            )
    else:
        dependencyPath = verifyIfFileExist(possibleDependencyPath)

    return dependencyPath


def createSubsFromOCRResults(ocrText: Dict[Path, str]):
    """
    Parameters:
        ocrText (Dict[Path, str]): It is the ocr results from OCREngine.runOCR.
    """
    from .VideoSubOCR import VideoSubFinder

    subs = SSAFile.from_string(ASS_DEFAULT)

    for imagePath, text in ocrText.items():
        start, end = VideoSubFinder.getTimeFromTxtImagesPath(imagePath)
        line = SSAEvent(start=start, end=end)
        line.plaintext = text
        subs.events.append(line)

    subsPath = os.path.join(os.getcwd(), "Output.ass")
    subs.save(subsPath)
    Console().print(f"Subtitle saved at {subsPath}", style="bright_green")


def runCommand(args: str, processName: str):
    """
    Parameters:
        args (str): The command.
        processName (str): The name of the command that will be show in the cmd.
    """

    process = subprocess.Popen(args)

    with Progress() as progress:

        task = progress.add_task(processName, total=None)

        while not progress.finished:
            progress.update(task)

            if process.poll() is not None:
                progress.update(task, completed=1, total=1, refresh=True)

            time.sleep(0.5)
