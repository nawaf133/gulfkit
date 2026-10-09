import re
from pathlib import Path

WEB = {
    "index.html": """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__NAME__</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <h1>__NAME__</h1>
    <p>المشروع جاهز، ابدأ من هنا.</p>
    <p id="today"></p>
  </main>
  <script src="script.js"></script>
</body>
</html>
""",
    "style.css": """:root {
  --bg: #0b1220;
  --fg: #e6edf7;
  --accent: #3b82f6;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--bg);
  color: var(--fg);
  font-family: "Tajawal", system-ui, sans-serif;
  line-height: 1.8;
}

main {
  padding: 2rem;
  text-align: center;
}

h1 {
  color: var(--accent);
  font-size: 2.5rem;
  margin: 0 0 .5rem;
}
""",
    "script.js": """const sar = new Intl.NumberFormat("ar-SA", { style: "currency", currency: "SAR" });
const hijri = new Intl.DateTimeFormat("ar-SA-u-ca-islamic-umalqura", { dateStyle: "full" });

document.querySelector("#today").textContent = hijri.format(new Date());
console.log(sar.format(1234.5));
""",
}

FLASK = {
    "app.py": """from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="__NAME__")


if __name__ == "__main__":
    app.run(debug=True)
""",
    "requirements.txt": "flask>=3.0\n",
    "templates/base.html": """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
""",
    "templates/index.html": """{% extends "base.html" %}
{% block content %}
<main>
  <h1>{{ title }}</h1>
  <p>المشروع جاهز، ابدأ من هنا.</p>
</main>
{% endblock %}
""",
    "static/style.css": WEB["style.css"],
}

TEMPLATES = {"web": WEB, "flask": FLASK}


def create(name, template="web", force=False):
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", name):
        raise ValueError("اسم المشروع لازم يكون حروف إنجليزية وأرقام و - أو _ بس")
    if template not in TEMPLATES:
        raise ValueError("القالب غير موجود: " + template)
    root = Path(name)
    if root.exists() and any(root.iterdir()) and not force:
        raise ValueError("المجلد موجود وفيه ملفات، استخدم --force لو تبي تكمل")
    created = []
    for rel, content in TEMPLATES[template].items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.replace("__NAME__", name), encoding="utf-8")
        created.append(str(path))
    return created
