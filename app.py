from flask import Flask, render_template

app = Flask(__name__)

# =========================
# ARTICLES
# =========================

articles = [
    {
        "id": 1,
        "title": "How AI is changing the way we use technology",
        "category": "ARTIFICIAL INTELLIGENCE",
        "date": "September 23, 2026",
        "read_time": "4 min read",
        "excerpt": "Artificial intelligence is moving from a futuristic concept into an everyday technology that is changing how we work, learn and create.",
        "content": """Artificial intelligence has quickly become one of the most important technologies of the modern era.

From recommendation systems and voice assistants to generative AI tools, intelligent software is becoming part of everyday life. What once seemed like science fiction is now being integrated into smartphones, computers, businesses and educational platforms.

One of the biggest changes brought by AI is the ability to process enormous amounts of information and turn it into useful results. AI can help people analyse data, generate ideas, automate repetitive tasks and solve complex problems.

However, the technology also raises important questions about privacy, misinformation, employment and the responsible use of automated systems.

The future of AI will not simply be about making machines more powerful. It will also be about deciding how humans use that power.

The most interesting part of the AI revolution may therefore not be the technology itself, but the new possibilities it creates for people."""
    }
]


# =========================
# HOMEPAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html", articles=articles)


# =========================
# ARTICLE PAGE
# =========================

@app.route("/article/<int:article_id>")
def article_page(article_id):

    article = next(
        (article for article in articles if article["id"] == article_id),
        None
    )

    if article is None:
        return "Article not found", 404

    return render_template("article.html", article=article)


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)