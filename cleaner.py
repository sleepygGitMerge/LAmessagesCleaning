import json
import re

# Function to remove URLs from text
def clean_content(text: str) -> str:
    """Removes all URLs from the given text."""
    if not isinstance(text, str):
        return ""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text =  url_pattern.sub('', text)
    # Remove non-breaking spaces and newline characters
    text = text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ")

    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

with open("updated_messages.json", "r", encoding="utf-8") as file:
    data = json.load(file)["messages"]

for msg in data:
    msg["content"] = clean_content(msg["content"])

for msg in data:
    if msg["author"] == None:
        data.remove(msg)
i = 0
for msg in data:
    msg["id"] = i
    i += 1

with open("posted_messages.json", "w", encoding="utf-8") as file:
    json.dump({"messages": data}, file, ensure_ascii=False, indent=4)