from PIL import Image, ImageOps
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

### Parameters ###

# Directory containing card images
CARD_DIR = "single_cards"
OUTPUT_PDF = "mtgcards_output.pdf"

CARD_WIDTH = 63 * mm
CARD_HEIGHT = 88 * mm

PAGE_WIDTH, PAGE_HEIGHT = A4

ROWS = 3
COLUMNS = 3

# Gap between cards
GAP_X = 0 * mm
GAP_Y = 0 * mm

##################

GRID_WIDTH = COLUMNS * CARD_WIDTH + (COLUMNS - 1) * GAP_X
GRID_HEIGHT = ROWS * CARD_HEIGHT + (ROWS - 1) * GAP_Y

if GRID_WIDTH > PAGE_WIDTH or GRID_HEIGHT > PAGE_HEIGHT:
    raise ValueError("Card grid dimensions with gaps exceed page size.")

MARGIN_X = (PAGE_WIDTH - GRID_WIDTH) / 2
MARGIN_Y = (PAGE_HEIGHT - GRID_HEIGHT) / 2

def process_image(img_path, crop_percentage=0, pad_percentage=0):
    """Process an image by cropping or adding padding."""
    img = Image.open(img_path)
    img = img.convert("RGB")

    if crop_percentage > 0:
        width, height = img.size
        crop_x = int(width * crop_percentage / 100)
        crop_y = crop_x
        img = img.crop((crop_x, crop_y, width - crop_x, height - crop_y))

    if pad_percentage > 0:
        width, height = img.size
        pad_x = int(width * pad_percentage / 100)
        pad_y = pad_x
        img = ImageOps.expand(img, border=(pad_x, pad_y), fill="black")

    return img

def get_image_files():
    """Retrieve all image files and their processing instructions."""
    image_files = []
    for root, dirs, files in os.walk(CARD_DIR):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                crop_percentage = 0
                pad_percentage = 0

                if "crop-" in root:
                    try:
                        crop_percentage = float(root.split("crop-")[-1])
                    except ValueError:
                        pass
                elif "pad-" in root:
                    try:
                        pad_percentage = float(root.split("pad-")[-1])
                    except ValueError:
                        pass

                image_files.append((os.path.join(root, file), crop_percentage, pad_percentage))

    return image_files

def create_pdf():
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    images = get_image_files()

    if not images:
        print("No card images found in the specified directory.")
        return

    x_offset = MARGIN_X
    y_offset = PAGE_HEIGHT - MARGIN_Y - CARD_HEIGHT

    for i, (img_path, crop_percentage, pad_percentage) in enumerate(images):
        print(f"Processing card ({i+1}/{len(images)}) '{img_path}' (Crop: {crop_percentage}%, Pad: {pad_percentage}%)")

        img = process_image(img_path, crop_percentage, pad_percentage)

        temp_img_path = f"temp_{i}.jpg"
        img.save(temp_img_path, "JPEG")

        c.drawImage(temp_img_path, x_offset, y_offset, width=CARD_WIDTH, height=CARD_HEIGHT)

        x_offset += CARD_WIDTH + GAP_X
        if (i + 1) % COLUMNS == 0:
            x_offset = MARGIN_X
            y_offset -= CARD_HEIGHT + GAP_Y

        if (i + 1) % (ROWS * COLUMNS) == 0:
            c.showPage()
            x_offset = MARGIN_X
            y_offset = PAGE_HEIGHT - MARGIN_Y - CARD_HEIGHT

        os.remove(temp_img_path)

    c.save()

    print(f"PDF created successfully: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_pdf()
