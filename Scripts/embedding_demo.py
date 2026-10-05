from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences =[ "The company spent ₹5.2 lakh on equipment.",
    "The organization invested money in laptops and servers.",
    "Employees receive annual leave."]

embeddings = model.encode(sentences)

print("Number of embeddings:",len(embeddings))
print("Embedding dimensions:",len(embeddings[0]))