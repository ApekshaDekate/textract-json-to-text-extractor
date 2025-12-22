from textractor.entities.document import Document
from textractor.data.text_linearization_config import TextLinearizationConfig

doc = Document.open("json1.bin")

def try_config(name, config):
    text = doc.get_text(config=config)
    with open(f"{name}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ saved: {name}.txt")

# ---------- CONFIGS TO TEST ----------

configs = {
    "clean_basic": TextLinearizationConfig(
        hide_header_layout=True,
        hide_footer_layout=True,
        hide_page_num_layout=True
    ),

    "no_newlines": TextLinearizationConfig(
        remove_new_lines_in_leaf_elements=True,
        same_layout_element_separator=" "
    ),

    "tables_removed": TextLinearizationConfig(
        hide_table_layout=True
    ),

    "all_visible": TextLinearizationConfig(
        hide_header_layout=False,
        hide_footer_layout=False,
        hide_table_layout=False
    ),
}

# ---------- RUN TESTS ----------

for name, cfg in configs.items():
    try_config(name, cfg)
