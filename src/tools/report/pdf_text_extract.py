from PyPDF2 import PdfReader
from crewai.tools import tool


class PDFExtractionTools:
    """Contains the PDf extraction tools"""

    @staticmethod
    @tool("Extracts text from the pdf file")
    def pdf_text_extraction(pdf_file_path: str) -> str:
        """
        This tool is used for extracting text from the pdf file

        Input:
        - pdf_file_path (str): contains the file path of the pdf

        Output:
        - extracted text from pdf
        """
        text = ""
        try:
            reader = PdfReader(pdf_file_path)
            for page in reader.pages:
                text += page.extract_text()
        except Exception as ex:
            raise Exception(f"Unable to extract text from PDF, error:{ex}")

        return text


def pdf_text_extract_tool():
    pdf_tool = PDFExtractionTools.pdf_text_extraction
    return pdf_tool