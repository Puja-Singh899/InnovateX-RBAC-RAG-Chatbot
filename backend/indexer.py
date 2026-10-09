
from pathlib import Path
import uuid

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


# Load the embedding model only when needed
embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return embedding_model


# Connect to ChromaDB only when needed
chroma_client = None
collection = None


def get_collection():
    global chroma_client, collection

    if collection is None:
        chroma_client = chromadb.PersistentClient(
            path="vectorstore"
        )

        collection = chroma_client.get_or_create_collection(
            name="company_documents"
        )

    return collection


# Keep the existing chunking configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


def extract_text_from_pdf(file_path: Path):
    reader = PdfReader(str(file_path))

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n\n".join(pages_text)


def index_document(
    file_path: str,
    department: str,
    source_name: str
):
    file_path = Path(file_path)

    # Read TXT or PDF
    if file_path.suffix.lower() == ".txt":
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

    elif file_path.suffix.lower() == ".pdf":
        text = extract_text_from_pdf(file_path)

    else:
        raise ValueError(
            "Only TXT and PDF files are supported."
        )

    if not text.strip():
        raise ValueError(
            "The document contains no extractable text."
        )

    # Split document into chunks
    chunks = text_splitter.split_text(text)

    if not chunks:
        raise ValueError(
            "No text chunks were generated."
        )

    # Load the model only when indexing is requested
    embeddings = get_embedding_model().encode(
        chunks
    ).tolist()

    # Generate unique document ID
    document_id = uuid.uuid4().hex

    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    # Connect to ChromaDB only when needed
    get_collection().add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "department": department,
                "source": source_name
            }
            for _ in chunks
        ]
    )

    return {
        "chunks": len(chunks),
        "department": department,
        "source": source_name
    }
