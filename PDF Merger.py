import sys
import os
from PyPDF2 import PdfMerger, PdfReader


def extract_text_from_pdf(pdf_file, txt_file):
    #initialize pdf reader object passing in the pdf file
    reader = PdfReader(pdf_file)

    #opens text file
    with open(txt_file, "w", encoding="utf-8") as f:
        #passing in the pdf file to the object lets us get the pages in the pdf. then extract text from pages and write it to the text file
        for page in reader.pages:
            text = page.extract_text()
            if text:
                f.write(text + "\n")


def main():
    #read output filename from command line
    if len(sys.argv) < 2:
        print("Error: Merge file name not specified.")
        print("Usage: python pdfmerger.py filename [--extract]")
        sys.exit(1)

    output_name = sys.argv[1]
    extract_flag = "--extract" in sys.argv

    output_file = f"{output_name}.pdf"

    #initialize merger object
    merger = PdfMerger()

    #get cwd files
    files = os.listdir(".")

    #gets pdf files in cwd
    pdf_files = []
    
    for f in files:
        if f.endswith('.pdf'):
            pdf_files.append(f)
    
    #filters out the output file by going through the list and checking each index to see if its the same as the output file
    new_list = []

    for file in pdf_files:
        if file != output_file:
            new_list.append(file)

    pdf_files = new_list

    #sort alphabetically
    pdf_files.sort()

    #print files found
    print(f"PDF files found: {len(pdf_files)}")
    print("List:")
    for file in pdf_files:
        print(file)

    #if there are no pfs stop program
    if len(pdf_files) == 0:
        print("No PDF files to merge.")
        sys.exit()

    #prompt user takes user input as lower loops until user picks 'y' or 'n' if 'y' move on if 'n' stop program
    while True:
        choice = input("Continue (y/n): ").lower()

        if choice == "n":
            print("Operation cancelled.")
            sys.exit()
        elif choice == 'y':
            break
        else:
            print("Please choose 'y' or 'n'")

    #append PDFs to merger
    for pdf in pdf_files:
        merger.append(pdf)

    # export merged file
    merger.write(output_file)
    merger.close()

    print(f"Merged file saved as: {output_file}")

    #if extract flag then extract text
    if extract_flag:
        txt_file = f"{output_name}.txt"
        extract_text_from_pdf(output_file, txt_file)
        print(f"Text extracted to: {txt_file}")


if __name__ == "__main__":
    main()
