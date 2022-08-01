# Scrolling Note Stitcher
## What is it
The tool serves the purpose of stitching together images which are specifically from scrolling note sheets. Note that it is a Command Line Interface (CLI) tool and (mostly) has no GUI. Some applications or playback tools do not give you an opportunity to download the original notesheet or PDF and only gives you the option of a scrolling notesheet/MP4. This tool converts the notesheet video into a full length notesheet.

This tool uses your GPU for processing, as it takes quite a long time to extract many images from an MP4 file quickly, thus the processing time scales on your processing power.

## Why a custom solution?
Preferrably one would use OpenCV to stitch images, but sadly OPENCV isn't easily usable on notesheets. It often mixes "image anchors" (points of reference) since so many notes are identical. It has issues parsing the thin lines of the score and the numbering of the music staff. Even if you are building up the note sheet piece by piece and are constraining it to an area, OpenCV simlpy fails to find a similar stiching reference

## How to use
Before installing, make sure that the video has the correct name of the artist and songname. The video name is used for the final export name. After, continue with the following:

1. Add the MP4(s) to the main area in a folder named "import"
  a. The folder can be manually created if it is missing
2. Launch "create_images"
  a. This converts the MP4(s) to an image set
3. Select the MP4(s) to convert
  b. Note: All files can be converted in one launch
3. Launch "create_scores" after all your MP4(s) are converted
4. Select MP4(s) to convert to notesheets
5. The notesheet will pop-up in an editor, where different properties can be adjusted
6. Adjust the properties and scroll through the sheet so that it fits properly
7. Press "S" to save or "Q" to quit
  a. It might use some time after pressing S
  b. The tool/GUI needs to be selected when pressing S or Q

## Potential improvements
- Merge Create_images and create_scores as one launch
- Build as executable with pyfreeze
- Integrate with a python library that supports music score parsing. This way we can convert the long sheet into multiple clean sheets instead of one continious one.
- Add tool-tips for S and Q to quit or save
- Remove GUI once S or Q are pressed
