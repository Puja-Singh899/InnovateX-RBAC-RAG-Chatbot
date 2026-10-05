import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Chroma
client = chromadb.PersistentClient(
    path="vectorstore"
)

collection = client.get_or_create_collection(
    name="company_documents"
)

# Read general document
file_path = "data/general/Company_FAQ.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

print("Number of chunks:", len(chunks))

# Generate embeddings
embeddings = model.encode(chunks).tolist()

# Store in Chroma
collection.add(
    ids=[f"general_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[
        {
            "department": "general",
            "source": "Company_FAQ.txt"
        }
        for _ in chunks
    ]
)

print("General documents added to Chroma!")