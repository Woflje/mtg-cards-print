import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path):
    try:
        if not os.path.exists(input_pdf_path):
            print(f"Error: File '{input_pdf_path}' does not exist.")
            return

        pdf_reader = PdfReader(input_pdf_path)
        num_pages = len(pdf_reader.pages)
        print(f"Total pages in '{input_pdf_path}': {num_pages}")

        base_name = os.path.splitext(input_pdf_path)[0]
        for i, page in enumerate(pdf_reader.pages):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)

            output_file_name = f"{base_name}-p{i+1}.pdf"
            with open(output_file_name, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"Created: {output_file_name}")
        
        print("PDF split completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_pdf = "input.pdf"
    split_pdf(input_pdf)