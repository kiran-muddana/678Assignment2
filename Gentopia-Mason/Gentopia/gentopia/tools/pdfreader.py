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
    arg1_result = analyzer._run(__arg1="https://example.com/sample.pdf")
    print(arg1_result)
