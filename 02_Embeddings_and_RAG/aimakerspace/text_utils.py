import os
from typing import List
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


class PDFFileLoader:
    def __init__(self, path: str):
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 is required for PDF loading. Install it with: pip install PyPDF2")
        self.documents = []
        self.path = path

    def load_file(self):
        """Extract text from a single PDF file."""
        try:
            with open(self.path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                self.documents.append(text.strip())
        except Exception as e:
            raise ValueError(f"Error reading PDF file {self.path}: {str(e)}")

    def load_directory(self):
        """Load all PDF files from a directory."""
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as pdf_file:
                            pdf_reader = PyPDF2.PdfReader(pdf_file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text() + "\n"
                            self.documents.append(text.strip())
                    except Exception as e:
                        print(f"Warning: Could not read PDF file {file_path}: {str(e)}")

    def load(self):
        """Load PDF file(s) from the specified path."""
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.lower().endswith(".pdf"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .pdf file."
            )

    def load_documents(self):
        """Load and return all documents."""
        self.load()
        return self.documents


class UniversalDocumentLoader:
    """A unified loader that can handle both text and PDF files."""
    
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        """Load documents from the specified path, supporting both text and PDF files."""
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.lower().endswith(".txt"):
                text_loader = TextFileLoader(self.path, self.encoding)
                self.documents.extend(text_loader.load_documents())
            elif self.path.lower().endswith(".pdf"):
                if not PDF_AVAILABLE:
                    raise ImportError("PyPDF2 is required for PDF loading. Install it with: pip install PyPDF2")
                pdf_loader = PDFFileLoader(self.path)
                self.documents.extend(pdf_loader.load_documents())
            else:
                raise ValueError(f"Unsupported file type: {self.path}")
        else:
            raise ValueError("Provided path is neither a valid directory nor a supported file.")

    def load_directory(self):
        """Load all supported files from a directory."""
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.lower().endswith(".txt"):
                        text_loader = TextFileLoader(file_path, self.encoding)
                        self.documents.extend(text_loader.load_documents())
                    elif file.lower().endswith(".pdf"):
                        if PDF_AVAILABLE:
                            pdf_loader = PDFFileLoader(file_path)
                            self.documents.extend(pdf_loader.load_documents())
                        else:
                            print(f"Warning: Skipping PDF file {file_path} - PyPDF2 not available")
                except Exception as e:
                    print(f"Warning: Could not load file {file_path}: {str(e)}")

    def load_documents(self):
        """Load and return all documents."""
        self.load()
        return self.documents


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
