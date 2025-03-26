import os
from typing import List, Tuple
import PyPDF2

def read_pdf_contents(pdf_file_path):
    """
    Reads the contents of a PDF file and returns the text from each page.

    Args:
        pdf_file_path (str): The file path of the PDF file to be read.

    Returns:
        str: The concatenated text from all pages of the PDF file.
    """
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Extract the text from each page and concatenate it
        pdf_text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            pdf_text += text

    return pdf_text

def get_pdf_files(directory: str) -> List[str]:
    """
    Retrieves a list of all PDF file names in the specified directory.
    
    Args:
        directory (str): The path to the directory containing the PDF files.
    
    Returns:
        List[str]: A list of PDF file names.
    """
    # Create an empty list to store the file names
    pdf_files: List[str] = []

    # Loop through all the files in the directory
    for filename in os.listdir(directory):
        # Check if the file has the .pdf extension
        if filename.endswith('.pdf'):
            # Add the file name to the list
            pdf_files.append(filename)

    return pdf_files

def get_application_id(filename: str) -> str:
    """
    Extracts the application id from the given file name.
    
    Args:
        filename (str): The name of the PDF file.
    
    Returns:
        str: The second number sequence extracted from the file name.
    """
    # Split the file name by the underscore
    parts = filename.split('_')
    # Extract the second number sequence
    second_number = parts[1]
    return second_number

def get_application_name_and_surname(filename: str) -> Tuple[str, str]:
    """
    Extracts the name and surname from the given file name.
    
    Args:
        filename (str): The name of the PDF file.
    
    Returns:
        Tuple[str, str]: A tuple containing the name and surname extracted from the file name.
    """
    # Split the file name by the underscore
    parts = filename.split('_')
    
    # Extract the name and surname, removing the .pdf extension if it's present in the surname
    name = parts[2]
    surname = parts[3]
    if surname.endswith('.pdf'):
        surname = surname[:-4]
    
    return name, surname

def get_candidate_application_pdf_data(application_id: str, directory: str):
    candidate_pdf_files = []
    pdf_files = get_pdf_files(directory=directory)
    # print(f"PDF files found: {pdf_files}")
    for pdf_file in pdf_files:
        application_id_from_file = get_application_id(pdf_file)
        # print(f"Application ID from file: {application_id_from_file}")
        if application_id_from_file == application_id:
            candidate_pdf_files.append(pdf_file)
            # pdf_file_path = f"{directory}/{pdf_file}"
            # print(f"Reading PDF file: {pdf_file_path}")
            # pdf_content = read_pdf_contents(pdf_file_path=pdf_file_path)
            # if pdf_content:
            #     pdf_contents.append(pdf_content)
    bmw_file = get_bmw_file(candidate_pdf_files)
    candidate_pdf_files.remove(bmw_file)
    return bmw_file, candidate_pdf_files


    # print(pdf_contents)
    # return "\n".join(pdf_contents)

def get_bmw_file(candidate_pdf_files : list):
    filtered_list = [s for s in candidate_pdf_files.copy() if ' ' not in s]
    filtered_list = [s for s in filtered_list if '.pdf' in s]
    return min(filtered_list, key=len)