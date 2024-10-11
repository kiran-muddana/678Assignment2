# import requests
# from PyPDF2 import PdfReader
# from typing import Any
# from pydantic import BaseModel, Field
# from gentopia.tools.basetool import BaseTool

# class PDFAnalyzerArgs(BaseModel):
#     pdf_url: str = Field(..., description="URL of the PDF file")

# class PDFAnalyzer(BaseTool):
#     """Tool for analyzing PDF files using PyPDF2 integrated with Gentopia."""
    
#     name = "pdf_analyzer"
#     description = "Fetches and analyzes text from a PDF file using a URL."

#     args_schema: Any = PDFAnalyzerArgs

#     def _run(self, **kwargs) -> str:
#         try:
#             # Extract the pdf_url from kwargs
#             pdf_url = kwargs.get('pdf_url', None)
#             if not pdf_url:
#                 return "Error: 'pdf_url' is required."

#             # Log the received additional arguments for debugging
#             print(f"Received pdf_url: {pdf_url}")
#             print(f"Received additional arguments: {kwargs}")

#             # Fetch the PDF from the provided URL
#             response = requests.get(pdf_url)
#             response.raise_for_status()

#             # Save the PDF content temporarily
#             with open("temp.pdf", "wb") as f:
#                 f.write(response.content)

#             # Open and read the PDF file
#             reader = PdfReader("temp.pdf")
#             text_content = []
#             # Iterate through each page in the PDF and extract text
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     text_content.append(text)

#             # Combine the text from all pages
#             return "\n\n".join(text_content)

#         except Exception as e:
#             return f"An error occurred while analyzing the PDF: {e}"

#     async def _arun(self, *args: Any, **kwargs: Any) -> Any:
#         raise NotImplementedError("Async run is not implemented.")

# if __name__ == "__main__":
#     # Example usage
#     analyzer = PDFAnalyzer()
#     # Provide a valid PDF URL here for testing
#     pdf_text = analyzer._run(pdf_url="https://example.com/sample.pdf")
#     print(pdf_text)

# working chatgpt

# import requests
# from PyPDF2 import PdfReader
# from typing import Any
# from pydantic import BaseModel, Field
# from gentopia.tools.basetool import BaseTool

# class PDFAnalyzerArgs(BaseModel):
#     pdf_url: str = Field(..., description="URL of the PDF file")

# class PDFAnalyzer(BaseTool):
#     """Tool for analyzing PDF files using PyPDF2 integrated with Gentopia."""
    
#     name = "pdf_analyzer"
#     description = "Fetches and analyzes text from a PDF file using a URL."

#     args_schema: Any = PDFAnalyzerArgs

#     def _run(self, **kwargs) -> str:
#         try:
#             # Extract the pdf_url from kwargs
#             pdf_url = kwargs.get('pdf_url', None)
#             if not pdf_url:
#                 return "Error: 'pdf_url' is required."

#             # Log the received URL for debugging
#             print(f"Received pdf_url: {pdf_url}")

#             # Fetch the PDF from the provided URL
#             response = requests.get(pdf_url, stream=True)
#             response.raise_for_status()

#             # Check if the response content type is a PDF
#             if 'application/pdf' not in response.headers.get('Content-Type', ''):
#                 return "Error: The provided URL does not point to a valid PDF file."

#             # Save the PDF content temporarily
#             with open("temp.pdf", "wb") as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     f.write(chunk)

#             # Open and read the PDF file
#             reader = PdfReader("temp.pdf")
#             text_content = []
#             # Iterate through each page in the PDF and extract text
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     text_content.append(text)

#             # Combine the text from all pages
#             return "\n\n".join(text_content) if text_content else "No text content found in the PDF."

#         except Exception as e:
#             return f"An error occurred while analyzing the PDF: {e}"

#     async def _arun(self, *args: Any, **kwargs: Any) -> Any:
#         raise NotImplementedError("Async run is not implemented.")

# if __name__ == "__main__":
#     # Example usage
#     analyzer = PDFAnalyzer()
#     # Provide a valid PDF URL here for testing
#     pdf_text = analyzer._run(pdf_url="https://example.com/sample.pdf")
#     print(pdf_text)


import io
import requests
from typing import Any, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field

class PDFAnalyzerArgs(BaseModel):
    pdf_source: str = Field(..., description="Path or URL to the PDF file")

class PDFAnalyzer(BaseTool):
    """Tool for analyzing PDF documents from both local files and URLs."""

    name = "pdf_analyzer"
    description = "Analyzes and extracts text from PDF documents. Can handle both local files and URLs."
    args_schema: Type[BaseModel] = PDFAnalyzerArgs

    def __init__(self):
        super().__init__()

    def _run(self, pdf_source: str = None, **kwargs) -> str:
        """
        Analyzes the specified PDF document, which can be either a local file or a URL.

        Args:
            pdf_source (str): The path to the PDF file or the URL of the PDF.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The extracted text and analysis from the PDF.
        """
        if pdf_source is None:
            pdf_source = kwargs.get('__arg1')
        if not pdf_source:
            return "Error: No PDF source provided"

        try:
            # Determine if the source is a URL or local file
            if pdf_source.startswith(('http://', 'https://')):
                response = requests.get(pdf_source)
                response.raise_for_status()
                pdf_file = io.BytesIO(response.content)
            else:
                pdf_file = open(pdf_source, 'rb')

            # Create a PDF reader object
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)

            analysis = f"PDF Analysis for {pdf_source}:\n\n"
            analysis += f"Total pages: {num_pages}\n\n"

            # Extract metadata
            metadata = reader.metadata
            if metadata:
                analysis += "Metadata:\n"
                for key, value in metadata.items():
                    analysis += f"{key}: {value}\n"
                analysis += "\n"

            # Extract text from all pages
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                analysis += f"Text from page {page_num + 1}:\n{text}\n\n"

            # Close the file if it's a local file
            if not pdf_source.startswith(('http://', 'https://')):
                pdf_file.close()

            return analysis

        except Exception as e:
            return f"Error analyzing PDF: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """
        Asynchronous version of the run method.
        """
        # This method is not implemented for asynchronous operation.
        raise NotImplementedError("Asynchronous operation is not supported for this tool.")

# Example usage (if running the script directly)
if __name__ == "__main__":
    analyzer = PDFAnalyzer()
    
    # Example with a local file
    local_result = analyzer._run(pdf_source="path/to/local/file.pdf")
    print(local_result)
    
    # Example with an online PDF
    online_result = analyzer._run(pdf_source="https://example.com/sample.pdf")
    print(online_result)
    
    # Example with argument passed as __arg1
    arg1_result = analyzer._run(__arg1="https://example.com/another_sample.pdf")
    print(arg1_result)


# from typing import AnyStr
# from PyPDF2 import PdfReader
# from gentopia.tools.basetool import *

# class PDFAnalyzerArgs(BaseModel):
#     pdf_path: str = Field(..., description="Path to the PDF file")
#     page_range: str = Field("all", description="Page range to analyze (e.g., '1-5', 'all')")

# class PDFAnalyzer(BaseTool):
#     """Tool that adds the capability to analyze PDF files using PyPDF2."""

#     name = "pdf_analyzer"
#     description = ("A PDF analysis tool that extracts text and metadata from PDF files. "
#                    "Input should be a path to a PDF file and optionally a page range.")

#     args_schema: Optional[Type[BaseModel]] = PDFAnalyzerArgs

#     def _run(self, pdf_path: AnyStr, page_range: str = "all") -> str:
#         try:
#             with open(pdf_path, 'rb') as file:
#                 reader = PdfReader(file)
#                 num_pages = len(reader.pages)
                
#                 if page_range == "all":
#                     pages_to_analyze = range(num_pages)
#                 else:
#                     start, end = map(int, page_range.split('-'))
#                     pages_to_analyze = range(start - 1, min(end, num_pages))
                
#                 analysis = f"PDF Analysis for {pdf_path}:\n\n"
#                 analysis += f"Total pages: {num_pages}\n\n"
                
#                 # Extract metadata
#                 metadata = reader.metadata
#                 analysis += "Metadata:\n"
#                 for key, value in metadata.items():
#                     analysis += f"{key}: {value}\n"
#                 analysis += "\n"
                
#                 # Extract text from specified pages
#                 for page_num in pages_to_analyze:
#                     page = reader.pages[page_num]
#                     text = page.extract_text()
#                     analysis += f"Text from page {page_num + 1}:\n{text}\n\n"
                
#                 return analysis
#         except Exception as e:
#             return f"Error analyzing PDF: {str(e)}"

#     async def _arun(self, *args: Any, **kwargs: Any) -> Any:
#         raise NotImplementedError

# if __name__ == "__main__":
#     analyzer = PDFAnalyzer()
#     result = analyzer._run("sample.pdf", "1-3")
#     print(result)