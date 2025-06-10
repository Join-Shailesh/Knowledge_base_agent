import pdfplumber, docx, requests
from bs4 import BeautifulSoup

knowledge_base = []

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    # Extract visible text
    text = soup.get_text(separator=' ', strip=True)
    # Optionally, clean up extra whitespace
    text = ' '.join(text.split())
    return text

def add_knowledge(source, content):
    knowledge_base.append({"source": source, "content": content})

def search_knowledge(query):
    return [item for item in knowledge_base if query.lower() in item["content"].lower()]
