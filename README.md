# VideoSubOCR
OCR automation for VideoSubFinder. 

## Installation and Update
```
pip install git+https://github.com/moi15moi/VideoSubOCR.git
```

## Dependencies
- [Python 3.7 or more](https://www.python.org/downloads)
- [ABBYY FineReader](https://pdf.abbyy.com) (or Tesseract)
- [Tesseract](https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D) (or ABBYY FineReader)
- [VapourSynth](https://github.com/vapoursynth/vapoursynth/releases/latest)  (Optional, but required to use cropbox argument)
- [VapourSynth-Editor](https://github.com/YomikoR/VapourSynth-Editor/releases/latest)  (Optional, but required to use VideoPreview.vpy)

### Setup for [ABBYY FineReader](https://pdf.abbyy.com)
You will need to have the same parameters has this image.
To change your parameters, open **ABBYY FineReader** and go to ``Tools -> Options -> Format Settings -> TXT``
![Alt text](https://github.com/moi15moi/VideoSubOCR/blob/main/ABBYY%20FineReader%20-%20OCR%20Parameters.png)

### Setup for [Tesseract](https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D)
To be able to select the language you want, you need to download tesseract tessdata.

- [tessdata](https://github.com/tesseract-ocr/tessdata)
- [tessdata_best](https://github.com/tesseract-ocr/tessdata_best)
- [tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast)

I recommand you to use **tessdata_best** traineddata.

You will need to download the language you need and move it in the right folder.
On Windows, it should be: ``C:\Users\YOUR_USERNAME\AppData\Local\Tesseract-OCR\tessdata``

## Usage
```console
usage: VideoSubOCR [-h] --input INPUT [--generalSettings GENERALSETTINGS]
                   [--cropBoxDimension Width_or_Height Width_or_Height] [--cropBoxHeight Height]
                   [--videosubfinderwxw VIDEOSUBFINDERWXW] [--tesseract [TESSERACT]] [--finereader [FINEREADER]]
                   [--lang LANG]

Video OCR automation.

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Video file needed to be OCR.
  --generalSettings GENERALSETTINGS
                        Path to general settings (*.cfg file). By default, VideoSubFinder use the file
                        settings/general.cfg
  --cropBoxDimension Width_or_Height Width_or_Height, -cpdh Width_or_Height Width_or_Height
                        CropBox dimension Width x Height. Ex: --cropBoxDimension 1920 1080
  --cropBoxHeight Height, -cph Height
                        CropBox height. It is the height between the video bottom and the cropbox bottom.
  --videosubfinderwxw VIDEOSUBFINDERWXW, -vsf VIDEOSUBFINDERWXW
                        Path to VideoSubFinderWXW.exe if not in variable environments.
  --tesseract [TESSERACT], -t [TESSERACT]
                        If tesseract.exe is in your variable environments, simply use --tesseract. If not, path to
                        FineCmd.exe
  --finereader [FINEREADER], -f [FINEREADER]
                        If FineCmd.exe is in your variable environments, simply use --finereader. If not, path to
                        FineCmd.exe
  --lang LANG, -l LANG  Language in which the hardsubbed subtitle is. It will be use by the ocr engine you choose.
                        Warning, ABBYY FineReader and Tesseract doesn't have the exact same input for the same
                        language. Tesseract support ISO 639-2 (t version):
                        https://www.loc.gov/standards/iso639-2/php/code_list.php ABBYY FineReader support the
                        fullname: https://help.abbyy.com/en-us/finereader/15/user_guide/commandline_lang/
```

### VideoSubFinder General Settings
I recommand you to always create a setting.
This will allow to have a better ocr
You can save the settings with ``File --> Save Settings As...``

For more information about VideoSubFinder, see their [website](https://sourceforge.net/projects/videosubfinder/)

### Alternative to VideoSubFinder General Settings

If you don't want to create a setting, I recommand you to use the file named **VideoPreview.vpy**. To use it, you will need to install [VapourSynth](https://github.com/vapoursynth/vapoursynth/releases/latest) and [VapourSynth-Editor](https://github.com/YomikoR/VapourSynth-Editor/releases/latest).

1. Open VideoPreview.vpy with VapourSynth-Editor.
2. Change ``inputVideo``, ``cropBoxDimension``, ``cropBoxHeight`` to the value you think you need.
3. Press **F5**
4. See if the cropbox is good for you. If not, repeat the step 2 and 3.