#running code to get text 
#------- steps to run---
# 1. source venv/bin/activate
# 2.  uvicorn test2:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from textractor.entities.document import Document
from textractor.data.text_linearization_config import TextLinearizationConfig
import tempfile
import json

app = FastAPI()

config = TextLinearizationConfig(
    # hide_header_layout=True,
    # hide_footer_layout=True,
     remove_new_lines_in_leaf_elements=True,
     same_layout_element_separator=" ",
    # hide_page_num_layout=True
    )



@app.post("/extract-text-file", response_class=PlainTextResponse)
async def extract_text_raw(request: Request):

    # Read JSON sent from Java
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

        # 🔥 use your config
        text = doc.get_text(config=config)


        # 🔥 remove extra empty lines
        # text = "\n".join([line for line in text.splitlines() if line.strip()])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Textract JSON: {e}")

    return PlainTextResponse(content=text)
