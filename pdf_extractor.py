from llama_parse import LlamaParse
import os

parser = LlamaParse(
    api_key=os.getenv("LLAMA_API_KEY"),
    result_type="markdown"
)

def extract_pdf_text(path: str) -> str:
    docs = parser.load_data(path)
    return docs[0].text