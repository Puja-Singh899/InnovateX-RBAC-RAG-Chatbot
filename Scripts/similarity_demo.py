from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model=SentenceTransformer("all-MiniLM-L6-v2")

chunks=[
     """INNOVATEX TECHNOLOGIES
    FINANCIAL REPORT — Q2 2026

    Company Overview

    InnovateX Technologies is a fictional technology company
    specializing in artificial intelligence, cloud computing,
    and enterprise software solutions.

    Q2 Revenue""",

    """Q2 Revenue

    The company generated a total revenue of ₹2.4 crore during
    the second quarter of 2026.

    Equipment Expenditure

    The company spent ₹5.2 lakh on laptops, development servers,
    network equipment, and other technical equipment during Q2 2026.

    Employee Reimbursements""",

    """Employee Reimbursements

    The company processed employee reimbursements totaling
    ₹1.8 lakh during Q2 2026.

    Marketing Expenditure

    The total marketing expenditure during Q2 2026 was ₹8.4 lakh.

    Operational Expenses

    The company incurred ₹12.6 lakh in operational expenses
    during Q2 2026.""",

    """Financial Summary

    Q2 revenue: ₹2.4 crore
    Equipment expenditure: ₹5.2 lakh
    Employee reimbursements: ₹1.8 lakh
    Marketing expenditure: ₹8.4 lakh
    Operational expenses: ₹12.6 lakh"""
]

# User question
question = "How much did the company spend on equipment?"

# Convert chunks and question into embeddings
chunk_embeddings = model.encode(chunks)
question_embedding = model.encode([question])

# Calculate similarity
similarities = cosine_similarity(
    question_embedding,
    chunk_embeddings
)[0]

# Display results
for i, score in enumerate(similarities):
    print(f"Chunk {i + 1}: {score:.4f}")
