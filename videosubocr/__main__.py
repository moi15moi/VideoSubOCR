import sys
from .Helpers import createSubsFromOCRResults
from .Parse import parseArguments


def main():
    videoSubFinder, ocrEngine = parseArguments()

    videoSubFinder.generateImages()
    ocrText = ocrEngine.runOCR(videoSubFinder.txtImages)
    createSubsFromOCRResults(ocrText)


if __name__ == "__main__":
    sys.exit(main())
