from fastapi.responses import HTMLResponse

@app.get("/editor", response_class=HTMLResponse)
def editor_ui():
    return """
<html>
<head>
<style>
.box { border: 1px solid #ccc; padding:10px; margin:5px; cursor:grab; }
#source, #target { width:45%; float:left; min-height:300px; border:1px solid #000; padding:10px; }
</style>
</head>
<body>
<h2>Drag paragraphs</h2>
<div id="source"></div>
<div id="target"></div>

<script>
async function loadData() {
    const response = await fetch("/temp-data");  // endpoint providing extracted paragraphs
    const data = await response.json();

    const container = document.getElementById("source");
    data.paragraphs.forEach(p => {
        let div = document.createElement("div");
        div.className = "box";
        div.draggable = true;
        div.innerText = p;

        div.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text/plain", p);
        });

        container.appendChild(div);
    });
}

document.getElementById("target").addEventListener("dragover", e => e.preventDefault());
document.getElementById("target").addEventListener("drop", e => {
    e.preventDefault();
    const p = e.dataTransfer.getData("text/plain");

    let div = document.createElement("div");
    div.className = "box";
    div.innerText = p;

    document.getElementById("target").appendChild(div);
});

loadData();
</script>
</body>
</html>
    """
