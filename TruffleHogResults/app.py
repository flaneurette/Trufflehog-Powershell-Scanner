from flask import Flask, jsonify, render_template_string
import os, json, re
import string

app = Flask(__name__)
RESULTS_DIR = "."  # same folder as JSON files
ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TruffleHog Dashboard</title>
<style>
body { font-family: Arial; margin: 20px; }
input { margin-bottom: 10px; padding: 5px; width: 300px; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 6px; vertical-align: top; }
th { background: #eee; }
tr:hover { background: #f9f9f9; }
pre { margin: 0; font-family: monospace; white-space: pre-wrap; word-break: break-word; cursor:pointer; }
.red { background-color: #f8a0a0; }
</style>
</head>
<body>
<h1>TruffleHog Full Log</h1>
<input type="text" id="search" placeholder="Search file, keyword...">
<table id="resultsTable">
<thead>
<tr><th>File</th><th>Line</th></tr>
</thead>
<tbody></tbody>
</table>

<script>
const tbody = document.querySelector("#resultsTable tbody");
const searchInput = document.getElementById("search");
let allData = [];

async function loadData() {
    const res = await fetch('/api/findings');
    allData = await res.json();
    displayRows(allData);
}

function displayRows(data) {
    tbody.innerHTML = "";
    data.forEach(item => {
        const tr = document.createElement('tr');
        const pre = document.createElement('pre');
        pre.textContent = item.raw;
        if(item.red) pre.classList.add('red');
        pre.addEventListener('click', () => {
            pre.style.maxHeight = pre.style.maxHeight === 'none' ? '50px' : 'none';
        });
        const tdFile = document.createElement('td');
        tdFile.textContent = item.file;
        const tdLine = document.createElement('td');
        tdLine.appendChild(pre);
        tr.appendChild(tdFile);
        tr.appendChild(tdLine);
        tbody.appendChild(tr);
    });
}

// Live search
searchInput.addEventListener("input", () => {
    const term = searchInput.value.toLowerCase();
    const filtered = allData.filter(item => 
        item.file.toLowerCase().includes(term) || 
        item.raw.toLowerCase().includes(term)
    );
    displayRows(filtered);
});

loadData();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/findings')
def get_findings():
    all_lines = []
    for fname in os.listdir(RESULTS_DIR):
        if fname.endswith(".json"):
            fpath = os.path.join(RESULTS_DIR, fname)
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    # Remove non-printable characters
                    line = ''.join(c for c in line if c in string.printable).strip()
                    if not line:
                        continue
                    # Strip ANSI escape codes
                    line_clean = ANSI_ESCAPE.sub('', line)
                    pretty = line_clean  # default
                    highlight = False
                    red = False
                    # Try JSON parsing for pretty-print
                    try:
                        data = json.loads(line_clean)
                        pretty = json.dumps(data, indent=2, ensure_ascii=False)
                        highlight = 'SourceMetadata' in data
                        red = highlight and data.get('Verified') is False
                    except json.JSONDecodeError:
                        pass
                    all_lines.append({
                        "file": fname,
                        "raw": pretty,
                        "highlight": highlight,
                        "red": red
                    })
    return jsonify(all_lines)


if __name__ == "__main__":
    app.run(debug=True)
