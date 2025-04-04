# MTG Card Print
This amature repository is designed as a tool to prepare Magic The Gathering card images (single cards) for printing.

## Usage `makepdf.py`

Simply put your single card images in a directory, match the directory name with `CARD_DIR`, and run the script.

### Parameters

The base script is made for A4 usage and cards of 63x88mm. You can change this in the Parameters section. You can also create a gap between the cards, to suit your own post process preferences.

### Cropping and Padding

You may prefer your cards to be somewhat consistent in their border. Some cards come with a very thick border, which you may want to crop. Put them in a subdirectory called `crop-4` where `4` means it will crop 4%. `crop-5` will crop 5% etc.
Similarly, you can put cards in a subdirectory called `pad-4` to add 4% padding, for cards that have no border at all.

## Extra tools

`pdftojpg.py` can be used to convert a PDF file to a JPG. Useful to reduce filesize (not for printing)

`splitpdf.py` can be used to split multi-page PDFs into single page PDFs.