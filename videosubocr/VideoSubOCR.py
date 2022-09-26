import os
from .Helpers import parseDependency, runCommand, verifyIfFileExist
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from rich.console import Console
from typing import Dict, Tuple


class CropBox(object):
    def __init__(self, top: float, bottom: float, left: float, right: float):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    @classmethod
    def from_vsf_param(
        cls,
        videoWidth: int,
        videoHeight: int,
        cropBoxDimensionWidth: float,
        cropBoxDimensionHeight: float,
        cropBoxHeight: float,
    ):
        """
        Parameters:
            videoWidth (int): The video width in pixel
            videoHeight (int): The video height in pixel
            cropBoxDimensionWidth (float): The cropbox width dimension in pixel
            cropBoxDimensionHeight (float): The cropbox height dimension in pixel
            cropBoxHeight (float): The cropbox height in pixel

                                VideoWidth
            -----------------------------------------------------
            |                                                   |
            |                                                   |
            |                                                   |  V
            |                                                   |  i
            |                                                   |  d
            |                                                   |  e
            |                                                   |  o
            |                                                   |
            |                                                   |  h
            |               CropBoxDimensionWidth               |  e
            |                -----------------                  |  i
            |                |               | CropBox          |  g
            |                |               | DimensionHeight  |  t
            |                -----------------                  |  h
            |                         |                         |
            |                         |                         |
            |          CropBoxHeight  |                         |
            |                         |                         |
            |                         |                         |
            -----------------------------------------------------
        Returns:
            An instance of CropBox.
        """

        top = (cropBoxHeight + cropBoxDimensionHeight) / videoHeight
        bottom = cropBoxHeight / videoHeight
        left = (videoWidth - cropBoxDimensionWidth) / (2 * videoWidth)
        right = 1 - left

        return cls(top, bottom, left, right)


class VideoSubFinder(object):

    name = "VideoSubFinder"

    def __init__(
        self,
        videoSubFinderPath: Path,
        videoPath: Path,
        cropBox: CropBox = None,
        generalSettings: Path = None,
    ):
        self.videoSubFinderPath = videoSubFinderPath
        self.videoPath = videoPath
        self.cropBox = cropBox
        self.generalSettings = generalSettings

    @property
    def videoSubFinderPath(self):
        return self._videoSubFinderPath

    @videoSubFinderPath.setter
    def videoSubFinderPath(self, value):
        self._videoSubFinderPath = parseDependency(self.name, value)

    @property
    def txtImages(self) -> Dict[Path, Image.Image]:
        filesList = {}
        imagesDirectory = os.path.join(
            os.path.dirname(self.videoSubFinderPath), "TXTImages"
        )

        for filename in os.listdir(imagesDirectory):
            filePath = os.path.join(imagesDirectory, filename)
            try:
                image = Image.open(filePath)
            except UnidentifiedImageError:
                continue
            else:
                filesList[filePath] = image

        return filesList

    @property
    def videoPath(self):
        return self._videoPath

    @videoPath.setter
    def videoPath(self, value):
        self._videoPath = verifyIfFileExist(value)

    @property
    def generalSettings(self):
        return self._generalSettings

    @generalSettings.setter
    def generalSettings(self, value):
        self._generalSettings = verifyIfFileExist(value, True)

    @staticmethod
    def getTimeFromTxtImagesPath(txtImage: Path) -> Tuple[int, int]:
        """
        Parameters:
            txtImage (Path): An image path from the VideoSubFinder's TxtImages folder.
                Ex: "C:\..\0_00_04_713__0_00_08_882_0039400035005700048000640.jpeg"
        Returns:
            The start time and the end time in milliseconds.
        """

        imageFilename = os.path.basename(txtImage)

        try:
            startHour = int(imageFilename[0])
            startMin = int(imageFilename[2:4])
            startSec = int(imageFilename[5:7])
            startMsec = int(imageFilename[8:11])

            endHour = int(imageFilename[13])
            endMin = int(imageFilename[15:17])
            endSec = int(imageFilename[18:20])
            endMsec = int(imageFilename[21:24])
        except ValueError:
            Console().print(
                f'Error: the file "{imageFilename}" is not conform to this naming convention H_M_S_MS__H_M_S_MS.',
                style="red1",
            )

        startMs = startHour * 3600000 + startMin * 60000 + startSec * 1000 + startMsec
        endMs = endHour * 3600000 + endMin * 60000 + endSec * 1000 + endMsec

        return startMs, endMs

    def generateImages(self):
        """
        Run VideoSubFinder to generate the images that will be used to OCR.
        """
        args = []

        args.append(f'"{self.videoSubFinderPath}"')
        args.append("--clear_dirs")
        args.append("--run_search")
        args.append("--create_cleared_text_images")

        if self.cropBox is not None:
            args.append(f"--top_video_image_percent_end={self.cropBox.top}")
            args.append(f"--bottom_video_image_percent_end={self.cropBox.bottom}")
            args.append(f"--left_video_image_percent_end={self.cropBox.left}")
            args.append(f"--right_video_image_percent_end={self.cropBox.right}")
        if self.generalSettings is not None:
            args.append(f'--general_settings="{self.generalSettings}"')

        args.append(f'--input_video="{self.videoPath}"')

        runCommand(" ".join(args), f"{self.name}...")

        Console().print(
            f"{self.name}: Successfully created images", style="bright_green"
        )
