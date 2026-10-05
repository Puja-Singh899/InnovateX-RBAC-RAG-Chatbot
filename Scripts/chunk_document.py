from langchain_text_splitters import RecursiveCharacterTextSplitter
file_path = "data/finance/Financial_Report_Q2_2026.txt"
with open(file_path,"r",encoding="utf-8") as file :
    text=file.read()
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 300,
  chunk_overlap = 50
)

chunks = text_splitter.split_text(text)
print("Number of chunks")

for i,chunk in enumerate(chunks) :
    print(f"\n--- Chunk {i+1} ---")
    print(chunk)