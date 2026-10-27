from huggingface_hub import InferenceClient
import json
from parser import parse_document
data_path = r"C:\Users\DELL\Downloads\small_ds_resume.pdf"
resume_text = parse_document(data_path)
with open("C:\\Users\\DELL\\Skill-Assessment-Agent\\Schema\\Schema\\resume_schema.json", "r", encoding="utf-8") as f:
    resume_schema = json.load(f)

client = InferenceClient(api_key="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")

system_prompt = """
You are an expert information extraction engine.

You extract structured information from resumes.

Rules:
- Return ONLY valid JSON.
- Never hallucinate.
- If information is missing, use null.
- Do not wrap the output in markdown.
"""

user_prompt = f"""
Extract information from the following resume.

The output MUST exactly match the JSON schema below.

Rules:
- Do NOT rename any key.
- Do NOT remove any key.
- Do NOT add any key.
- Replace only the values.
- Keep the same nesting.
- Every skill mentioned in the resume should appear in the skills list.
- Every evidence entry must be copied directly from the resume.

JSON Schema:

{json.dumps(resume_schema, indent=2)}

Resume:

{resume_text}
"""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=messages,
    temperature=0,
    max_tokens = 4096
)


content = response.choices[0].message.content

print("Finish reason:", response.choices[0].finish_reason)
resume_data = json.loads(content)




