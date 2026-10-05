from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain RAG in one sentence."
)

print(interaction.output_text)
