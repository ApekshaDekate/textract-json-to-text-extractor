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
    title_prefix="<h2>",
    title_suffix="</h2>",
    header_prefix="<h2>",
    header_suffix="</h2>",
)

@app.post("/extract-text-file", response_class=PlainTextResponse)
async def extract_text_raw(request: Request):

    # Read JSON sent from Javaw
    try:
        raw_json = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # 🔥 Write raw JSON to a real file (Textractor requires this)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
        json.dump(raw_json, tmp)
        temp_path = tmp.name

    try:
        # 🔥 Now Textractor can load it normally
        doc = Document.open(temp_path)

        # # 🔥 use your config
        # text = doc.get_text(config=config)
        #  html version
        html = doc.get_text(html_config)


        # 🔥 remove extra empty lines
        # text = "\n".join([line for line in text.splitlines() if line.strip()])


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Textract JSON: {e}")

    return PlainTextResponse(content=html)
