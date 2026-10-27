from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
from parser import parse_document

data_path = r"C:\Users\DELL\Downloads\small_ds_resume.pdf"
data = parse_document(data_path)

with open("Schema/Schema/resume_schema.json", "r", encoding="utf-8") as f:
    resume_schema = json.load(f)

llm = ChatOllama(model="qwen2.5:3b", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    (
       
        "system",
        """
You are an expert resume information extractor.

Your task is to extract structured information from the given resume.

Rules:
1. Return ONLY valid JSON.
2. Do NOT include markdown.
3. Do NOT explain your reasoning.
4. Do NOT invent information.
5. If a field is missing, use null.
6. Evidence must come directly from the resume.
7. Follow the JSON schema exactly.

JSON Schema:

{resume_schema}
"""
    ),
    (
        "human",
        """
Resume Text:

{resume_text}
""")
])

chain = prompt | llm
response = chain.invoke({
    "resume_schema": json.dumps(resume_schema, indent=2), 
    "resume_text": data["text"]
})


print(response.content)