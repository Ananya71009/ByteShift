from flask import Flask, render_template, Response

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

From recommendation systems and voice assistants to generative AI tools, intelligent software is becoming part of everyday life.

One of the biggest changes brought by AI is the ability to process enormous amounts of information and turn it into useful results.

However, the technology also raises important questions about privacy, misinformation, employment and responsible use.

The future of AI will not simply be about making machines more powerful. It will also be about deciding how humans use that power."""
    },

    {
        "id": 2,
        "title": "The technology race shaping the next decade",
        "category": "TECHNOLOGY",
        "date": "September 24, 2026",
        "read_time": "5 min read",
        "excerpt": "From powerful processors to intelligent software, technology is moving through a period of unusually rapid change.",
        "content": """Technology is developing faster than ever, with new advances appearing across computing, artificial intelligence, robotics and communication.

Modern devices are becoming more capable while also becoming smaller and more efficient.

At the same time, companies and researchers are exploring new ways to combine hardware and software to solve increasingly complex problems.

The next decade could bring major changes to how people interact with computers, information and digital services.

The interesting question is not simply what technology will exist, but how people will choose to use it."""
    },

    {
        "id": 3,
        "title": "Why cybersecurity matters more than ever",
        "category": "CYBERSECURITY",
        "date": "September 24, 2026",
        "read_time": "4 min read",
        "excerpt": "As more of everyday life moves online, protecting personal information and digital systems has become increasingly important.",
        "content": """Our lives are becoming increasingly connected to the internet.

Phones, computers, banking systems, social platforms and cloud services all depend on digital infrastructure.

This connectivity brings convenience, but it also creates security challenges.

Strong passwords, multi-factor authentication, software updates and cautious online behaviour are some of the basic steps people can take to improve their digital security.

Cybersecurity is no longer only an issue for large technology companies. It is becoming an important part of everyday digital life."""
    },

    {
        "id": 4,
        "title": "What happens when humans and AI work together?",
        "category": "FUTURE",
        "date": "September 25, 2026",
        "read_time": "5 min read",
        "excerpt": "The future of work may not be humans versus machines, but humans using intelligent systems as powerful tools.",
        "content": """The conversation around artificial intelligence often focuses on what machines might replace.

A different perspective is to consider what happens when humans and AI work together.

AI systems can process information quickly, recognise patterns and assist with repetitive tasks. Humans bring creativity, judgement, context and responsibility.

Combining those strengths could change how people approach education, engineering, design, research and many other fields.

The future may therefore be less about replacing humans and more about building better ways for humans and technology to collaborate."""
    },

    {
        "id": 5,
        "title": "The next generation of computing",
        "category": "INNOVATION",
        "date": "September 25, 2026",
        "read_time": "6 min read",
        "excerpt": "Computing is evolving beyond traditional performance metrics as researchers explore new approaches to processing information.",
        "content": """For decades, progress in computing was largely measured by faster processors and more powerful hardware.

Today, the picture is becoming more complicated.

Researchers are exploring specialised chips, advanced architectures, edge computing and other approaches designed for specific types of workloads.

Artificial intelligence is also changing what modern computing systems need to do efficiently.

The next generation of computing will likely involve a combination of different technologies rather than one universal approach.

That shift could influence everything from personal devices to large-scale scientific research."""
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
# XML SITEMAP
# =========================

@app.route("/sitemap.xml")
def sitemap():

    urls = [
        "https://byteshift-w1bw.onrender.com/"
    ]

    for article in articles:
        urls.append(
            f"https://byteshift-w1bw.onrender.com/article/{article['id']}"
        )

    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

    for url in urls:
        xml += f"<url><loc>{url}</loc></url>"

    xml += "</urlset>"

    return Response(xml, mimetype="application/xml")


# =========================
# ROBOTS.TXT
# =========================

@app.route("/robots.txt")
def robots():

    robots_text = """User-agent: *
Allow: /

Sitemap: https://byteshift-w1bw.onrender.com/sitemap.xml
"""

    return Response(robots_text, mimetype="text/plain")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)