import pdfplumber, docx, requests, json, os
from bs4 import BeautifulSoup

KB_FILE = "knowledge_base.json"
knowledge_base = []

def load_kb_from_file():
    """Load the knowledge base from a JSON file at startup."""
    global knowledge_base
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, "r") as f:
                knowledge_base = json.load(f)
            print(f"Loaded {len(knowledge_base)} entries from {KB_FILE}")
        except Exception as e:
            print(f"Error loading KB: {e}")
            knowledge_base = []
    else:
        knowledge_base = []
        print(f"No existing KB file found. Starting with empty knowledge base.")

def save_kb_to_file():
    """Save the current knowledge base to a JSON file."""
    try:
        with open(KB_FILE, "w") as f:
            json.dump(knowledge_base, f)
        print(f"Saved {len(knowledge_base)} entries to {KB_FILE}")
    except Exception as e:
        print(f"Error saving KB: {e}")

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_url(url):
    """Extract visible text from a web page."""
    response = requests.get(str(url))  # Ensure url is a string
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return ' '.join(text.split())

def add_knowledge(source, content):
    """Add an entry to the knowledge base and persist it."""
    global knowledge_base
    knowledge_base.append({"source": str(source), "content": content})  # Ensure source is a string
    save_kb_to_file()

def search_knowledge(query):
    """Search the knowledge base for entries containing any query word."""
    q = query.lower()
    return [
        item for item in knowledge_base
        if any(word in item["content"].lower() for word in q.split())
    ]

def get_knowledge_base():
    global knowledge_base
    return knowledge_base