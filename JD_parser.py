import fitz

doc = fitz.open(r"C:\Users\DELL\Downloads\Jd.pdf")

jd_text = ""

for page in doc:
    jd_text += page.get_text()

print(jd_text)