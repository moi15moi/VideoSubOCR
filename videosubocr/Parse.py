import shutil
import sys
from argparse import ArgumentParser
from .Helpers import verifyIfFileExist
from .OCREngine import FineReader, OCREngine, Tesseract
from pathlib import Path
from rich.console import Console
from typing import Tuple
from .VideoSubOCR import CropBox, VideoSubFinder


def parseArguments() -> Tuple[VideoSubFinder, OCREngine]:
    parser = ArgumentParser(prog="VideoSubOCR", description="Video OCR automation.")

    # VideoSubFinder arguments
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="""
    Video file needed to be OCR.
    """,
    )

    parser.add_argument(
        "--generalSettings",
        type=Path,
        help="""
    Path to general settings (*.cfg file). By default, VideoSubFinder use the file settings/general.cfg
    """,
    )

    parser.add_argument(
        "--cropBoxDimension",
        "-cpdh",
        type=float,
        nargs=2,
        metavar="Width_or_Height",
        help="""
    CropBox dimension Width x Height. Ex: --cropBoxDimension 1920 1080
    """,
    )

    parser.add_argument(
        "--cropBoxHeight",
        "-cph",
        type=float,
        metavar="Height",
        help="""
    CropBox height. It is the height between the video bottom and the cropbox bottom.
    """,
    )
    parser.add_argument(
        "--videosubfinderwxw",
        "-vsf",
        type=Path,
        help="""
    Path to VideoSubFinderWXW.exe if not in variable environments.
    """,
    )
    # End VideoSubFinder arguments

    parser.add_argument(
        "--tesseract",
        "-t",
        type=Path,
        nargs="?",
        const=shutil.which("tesseract"),
        help="""
    If tesseract.exe is in your variable environments, simply use --tesseract.
    If not, path to FineCmd.exe

    """,
    )

    parser.add_argument(
        "--finereader",
        "-f",
        type=Path,
        nargs="?",
        const=shutil.which("FineCmd"),
        help="""
    If FineCmd.exe is in your variable environments, simply use --finereader.
    If not, path to FineCmd.exe
    """,
    )

    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        help="""
    Language in which the hardsubbed subtitle is. 
    It will be use by the ocr engine you choose.
    Warning, ABBYY FineReader and Tesseract doesn't have the exact same input for the same language.
        Tesseract support ISO 639-2 (t version): https://www.loc.gov/standards/iso639-2/php/code_list.php
        ABBYY FineReader support the fullname: https://help.abbyy.com/en-us/finereader/15/user_guide/commandline_lang/
    """,
    )

    args = parser.parse_args()
    cropBox = None

    if args.cropBoxDimension is not None and args.cropBoxHeight is not None:
        import vapoursynth as vs

        video = vs.core.ffms2.Source(verifyIfFileExist(args.input))

        cropBox = CropBox.from_vsf_param(
            video.width,
            video.height,
            args.cropBoxDimension[0],
            args.cropBoxDimension[1],
            args.cropBoxHeight,
        )

    ocrEngine = None
    if args.finereader is not None:
        ocrEngine = FineReader(args.finereader, args.lang)

    if args.tesseract is not None:
        ocrEngine = Tesseract(args.tesseract, args.lang)

    if ocrEngine is None:
        sys.exit(
            Console().print(
                f"Error: There is no OCR engine in your variable environments or you need to precize the OCR engine you wanna use (ABBYY FineReader or Tesseract)",
                style="red1",
            )
        )

    return (
        VideoSubFinder(
            args.videosubfinderwxw, args.input, cropBox, args.generalSettings
        ),
        ocrEngine,
    )
