import os
from typing import List, Dict

from utils import configs
from llama_index.core.schema import Document
from llama_index.readers.file import PyMuPDFReader


class DocumentGetter:
    """A class to retrieve documents from PDF files."""
    _PDF_READERS: Dict[str, object] = {
        'pymupdf': PyMuPDFReader()
    }

    def __init__(self, pdf_reader: str = 'pymupdf'):
        """Initialize the DocumentGetter with a specified PDF reader."""
        if pdf_reader not in self._PDF_READERS:
            raise ValueError(f"Unsupported PDF reader: {pdf_reader}")
        self._pdf_reader = self._PDF_READERS[pdf_reader]

    def get_documents_from_pdf(self, filepath: str) -> List[Document]:
        """
        Retrieve documents from a PDF file.

        Args:
            filepath (str): The path to the PDF file.

        Returns:
            List[Document]: A list of Document objects extracted from the PDF.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file is not a PDF.
            Exception: For any other errors during PDF processing.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file {filepath} does not exist.")

        if not filepath.lower().endswith('.pdf'):
            raise ValueError(f"The file {filepath} is not a PDF.")

        try:
            return self._pdf_reader.load_data(file_path=filepath)
        except Exception as e:
            raise Exception(f"Error processing PDF file: {str(e)}")


def main():
    """Main function to demonstrate the usage of DocumentGetter."""
    document_getter = DocumentGetter()
    pdf_path = os.path.join(configs.pdf_dir, "handbook.pdf")

    try:
        documents = document_getter.get_documents_from_pdf(filepath=pdf_path)
        print(f"Successfully extracted {len(documents)} documents from {pdf_path}")
        for i, doc in enumerate(documents, 1):
            print(f"Document {i}: {doc.text[:100]}...")  # Print first 100 characters of each document
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
