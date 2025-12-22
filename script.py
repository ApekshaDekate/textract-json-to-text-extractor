from textractor.entities.document import Document
from textractor.data.text_linearization_config import TextLinearizationConfig

# create config in a compact way
config = TextLinearizationConfig(
    # hide_header_layout=True,
    # hide_footer_layout=True,
    # hide_page_num_layout=True,
    # remove_new_lines_in_leaf_elements=False,  # IMPORTANT
    same_layout_element_separator="\n",       # keep line breaks
    same_paragraph_separator="\n",
    layout_element_separator="\n\n", 
    # remove_new_lines_in_leaf_elements=True
)

# load → convert → save (one-liner style)
output = Document.open("json1.bin").get_text(config=config)

with open("output2.txt", "w", encoding="utf-8") as out:
    out.write(output)

print("Text extracted.")