file_path ="data/finance/Financial_Report_Q2_2026.txt"
with open(file_path,"r",encoding="utf-8") as file :
 text = file.read()
print(text)