import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create Chroma client
client = chromadb.PersistentClient(
    path="vectorstore"
)

collection = client.get_or_create_collection(
    name="company_documents"
)


# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


# Root data directory
DATA_DIR = "data"


# Process every department folder
for department in os.listdir(DATA_DIR):

    department_path = os.path.join(
        DATA_DIR,
        department
    )

    # Skip anything that isn't a folder
    if not os.path.isdir(department_path):
        continue

    # Process every text file
    for filename in os.listdir(department_path):

        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(
            department_path,
            filename
        )

        # Read document
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

        # Split into chunks
        chunks = text_splitter.split_text(text)

        print(
            f"{filename} → {len(chunks)} chunks"
        )

        # Create embeddings
        embeddings = model.encode(chunks).tolist()

        # Create unique IDs
        ids = [
            f"{department}_{filename}_{i}"
            for i in range(len(chunks))
        ]

        # Metadata
        metadatas = [
            {
                "department": department,
                "source": filename
            }
            for _ in chunks
        ]

        # Add to Chroma
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Added {filename} to Chroma."
        )


print("\nAll documents indexed successfully!")