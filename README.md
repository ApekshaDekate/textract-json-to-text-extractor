# Textract JSON to Text Extractor (Line-by-Line)

This project converts **AWS Textract JSON output** into **clean, readable text**
while preserving **one PDF line per output line**.

It is especially useful for:
- Court judgments
- Legal documents
- Government orders
- OCR-processed PDFs where line fidelity matters

---

## ❓ Why this project?

The default Textractor method (`get_text()`) merges lines and paragraphs.

❌ Not suitable for legal documents  
✅ This project extracts **Textract LINE blocks directly**

Result:
- No line merging
- No layout reflow
- Deterministic, PDF-like output

---

## 📂 Project Structure

```text
textract-json-to-text-extractor/
├── test2.py              # Main script (line-by-line extraction)
├── requirements.txt
├── README.md
├── .gitignore
