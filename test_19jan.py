#running code to get text 
#------- steps to run---
# 1. source venv/bin/activate
# 2. uvicorn test:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from textractor.entities.document import Document
from textractor.data.text_linearization_config import TextLinearizationConfig
from textractor.data.html_linearization_config import HTMLLinearizationConfig
import tempfile
import json
import re
from bs4 import BeautifulSoup   

app = FastAPI()


# config = TextLinearizationConfig(
#     remove_new_lines_in_leaf_elements=True,
#     same_paragraph_separator=" ",       # join lines inside one paragraph
#     same_layout_element_separator="\n\n",  # blank line between layout blocks
#     layout_element_separator="\n\n",       # between different layout types
#     hide_header_layout=False,
#     hide_footer_layout=False,
#     hide_page_num_layout=False,       # keep page numbers if you want same look
#     max_number_of_consecutive_new_lines=2,
# )

# Generate TinyMCE-ready HTML
html_config = HTMLLinearizationConfig(
    hide_header_layout=False,    # Keep headers
    hide_footer_layout=False,    # Keep footers  
    hide_page_num_layout=False,  # Keep page numbers
    # table_linearization_format="html",  # Tables as HTML
    # add_short_ids_to_html_tags=True,
    title_prefix="<h4>",
    title_suffix="</h4>",
    header_prefix="<h4>",
    header_suffix="</h4>",
)


def looks_like_new_point(text: str) -> bool:
    return bool(re.match(r"^\s*(\d+[\)\.]|\([a-z]\))", text, re.I))


def looks_like_heading(text: str) -> bool:
    return text.isupper() and len(text.split()) < 15


def should_merge(prev: str, curr: str) -> bool:
    if not prev or not curr:
        return False

    # ❌ sentence clearly ended
    if prev.rstrip().endswith((".", "?", "!", ":", ";")):
        return False

    # ❌ new numbered paragraph
    if looks_like_new_point(curr):
        return False

    # ❌ heading / CORAM / JUDGMENT
    if looks_like_heading(curr):
        return False


    # ✅ lowercase continuation
    if curr.lstrip()[0].islower():
        return True

    # ✅ uppercase continuation
    if curr.lstrip()[0].isupper():
        return True

    return False


def merge_broken_paragraphs(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")

    i = 0
    while i < len(paragraphs) - 1:
        p1 = paragraphs[i]
        p2 = paragraphs[i + 1]

        t1 = p1.get_text(strip=True)
        t2 = p2.get_text(strip=True)

        if should_merge(t1, t2):
            p1.string = f"{t1} {t2}"
            p2.decompose()
        else:
            i += 1

    return str(soup)

@app.post("/extract-text-file", response_class=PlainTextResponse)
async def extract_text_raw(request: Request):

    # Read JSON sent from Java
    try:
        raw_json = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    #  Write raw JSON to a real file (Textractor requires this)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        json.dump(raw_json, tmp)
        temp_path = tmp.name

    try:
        #  Now Textractor can load it normally
        doc = Document.open(temp_path)

        # # use your config
        # text = doc.get_text(config=config)
        #  html version
        html = doc.get_text(html_config)

        #  FIX cross-page paragraph breaks
        html = merge_broken_paragraphs(html)


        #  remove extra empty lines
        # text = "\n".join([line for line in text.splitlines() if line.strip()])


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Textract JSON: {e}")

    return PlainTextResponse(content=html)
