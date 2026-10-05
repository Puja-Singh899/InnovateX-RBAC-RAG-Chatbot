import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
import os

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to our existing Chroma database
client = chromadb.PersistentClient(
    path="vectorstore"
)
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

ROLE_PERMISSIONS = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "executive": ["finance", "marketing", "hr", "engineering", "general"],
    "employee": ["general"],
}

user_role = "finance"

allowed_departments = ROLE_PERMISSIONS[user_role]

print("User role:", user_role)
print("Allowed departments:", allowed_departments)

# Get our collection
collection = client.get_collection(
    name="company_documents"
)

# User's question
question = question = "How much did the company spend on equipment?"

# Convert question into an embedding
question_embedding = model.encode(question).tolist()

# Search Chroma
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2,
    where={
        "department": {
            "$in": allowed_departments
        }
    }
)

# Display results
for i, document in enumerate(results["documents"][0]):
    print(f"\n--- Result {i + 1} ---")
    print(document)

 # Combine retrieved documents into context
context = "\n\n".join(results["documents"][0])

# Create a prompt using the retrieved context
prompt = f"""
You are a company assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say that you do not have enough information.

Context:
{context}

Question:
{question}
"""

# Generate answer using Gemini
interaction = gemini_client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
)

print("\n--- Generated Answer ---")
print(interaction.output_text)

print("\n--- Sources ---")

unique_sources = set()

for metadata in results["metadatas"][0]:
    unique_sources.add(metadata["source"])

for source in unique_sources:
    print(f"- {source}")