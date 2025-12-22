from textractor.entities.document import Document

doc = Document.open("json.bin")

lines = []

for page in doc.pages:
    for line in page.lines:
        lines.append(line.text)
    lines.append("")  # page separator

output = "\n".join(lines)

with open("output3.txt", "w", encoding="utf-8") as out:
    out.write(output)

print("Text extracted – every line on a new line")
