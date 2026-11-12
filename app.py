from flask import Flask, render_template_string, request
from parser import parser
from semantic import semantic_analysis
from intermediate import generate_tac
from interpreter import execute_tac
import io
import sys

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Mini Compiler IDE</title>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>

<style>
body {
    margin:0;
    background:#1e1e1e;
    color:white;
    font-family: Consolas;
}

header {
    background:#007acc;
    padding:10px;
    text-align:center;
    font-size:18px;
}

.container {
    display:flex;
    height:90vh;
}

.editor {
    width:50%;
    padding:10px;
}

.output {
    width:50%;
    padding:10px;
    background:#111;
    overflow:auto;
}

button {
    padding:10px;
    background:#007acc;
    color:white;
    border:none;
    margin-top:10px;
    cursor:pointer;
}

.section {
    margin-bottom:15px;
    padding:10px;
    border-radius:5px;
}

.success {
    background:#0f5132;
}

.error {
    background:#842029;
}

.tac {
    background:#1a1a1a;
}

h3 {
    margin:5px 0;
}

pre {
    white-space:pre-wrap;
}
</style>

</head>

<body>

<header>🚀 Mini Compiler IDE</header>

<div class="container">

<div class="editor">
<form method="post">
<textarea id="code" name="code">{{code}}</textarea>
<br>
<button type="submit">▶ Run Compiler</button>
</form>
</div>

<div class="output">

{% if error %}
<div class="section error">
<h3>❌ Error</h3>
<pre>{{error}}</pre>
</div>
{% endif %}

{% if ast %}
<div class="section">
<h3>🌳 AST</h3>
<pre>{{ast}}</pre>
</div>
{% endif %}

{% if semantic %}
<div class="section success">
<h3>🧠 Semantic Output</h3>
<pre>{{semantic}}</pre>
</div>
{% endif %}

{% if tac %}
<div class="section tac">
<h3>⚙️ TAC</h3>
<pre>{{tac}}</pre>
</div>
{% endif %}

{% if final %}
<div class="section success">
<h3>✅ Final Output</h3>
<pre>{{final}}</pre>
</div>
{% endif %}

</div>

</div>

<script>
var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    theme: "default",
    mode: "text/x-csrc"
});
</script>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    ast_out = ""
    semantic_out = ""
    tac_out = ""
    final_out = ""
    error = ""
    code = ""

    if request.method == "POST":
        code = request.form["code"]

        try:
            # Capture semantic output
            old_stdout = sys.stdout
            sys.stdout = sem_buffer = io.StringIO()

            ast = parser.parse(code)
            ast_out = str(ast)

            semantic_analysis(ast)

            semantic_out = sem_buffer.getvalue()
            sys.stdout = old_stdout

            # TAC
            tac = generate_tac(ast)
            tac_out = "\n".join(tac)

            # Final Execution
            sys.stdout = final_buffer = io.StringIO()
            execute_tac(tac)
            final_out = final_buffer.getvalue()
            sys.stdout = old_stdout

        except Exception as e:
            sys.stdout = old_stdout
            error = str(e)

    return render_template_string(
        HTML,
        ast=ast_out,
        semantic=semantic_out,
        tac=tac_out,
        final=final_out,
        error=error,
        code=code
    )

if __name__ == "__main__":
    app.run(debug=True)