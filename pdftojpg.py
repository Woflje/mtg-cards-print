from pdf2image import convert_from_path

input_pdf = "input.pdf"
output_image = "output.jpg"

def pdf_to_jpg(input_pdf, output_image):
    try:
        images = convert_from_path(input_pdf, first_page=1, last_page=1)
        
        if images:
            images[0].save(output_image, 'JPEG')
            print(f"Successfully converted the first page of {input_pdf} to {output_image}")
        else:
            print("No pages found in the PDF.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pdf_to_jpg(input_pdf, output_image)