from flask import Flask, render_template_string, request
from detector import detect_fake_news

app = Flask(__name__)

# Load index.html content
with open("index.html", "r", encoding="utf-8") as f:
    html_template = f.read()

@app.route("/", methods=["GET", "POST"])
def home():
    verdict, sources = None, []
    if request.method == "POST":
        headline = request.form.get("headline")
        if headline:
            verdict, sources = detect_fake_news(headline)
    return render_template_string(html_template, verdict=verdict, sources=sources)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






