import chromadb

client = chromadb.PersistentClient(
    path="vectorstore"
)

collection = client.get_collection(
    name="company_documents"
)

results = collection.get(
    where={
        "source": "InnovateX_Finance_Q3_Report.pdf"
    },
    include=["metadatas"]
)

for doc_id, metadata in zip(
    results["ids"],
    results["metadatas"]
):
    print(doc_id, "->", metadata)