from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Response
)
import sqlite3
import os
from functools import wraps

app = Flask(__name__)

# =========================================
# SETTINGS
# =========================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "byteshift-local-development-key"
)

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "admin"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "byteshift123"
)

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "byteshift.db"
)


# =========================================
# DATABASE
# =========================================

def get_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            read_time TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    existing_articles = connection.execute(
        "SELECT COUNT(*) AS count FROM articles"
    ).fetchone()["count"]

    if existing_articles == 0:

        starter_articles = [
            (
                "How AI is changing the way we use technology",
                "ARTIFICIAL INTELLIGENCE",
                "September 23, 2026",
                "4 min read",
                "Artificial intelligence is moving from a futuristic concept into an everyday technology that is changing how we work, learn and create.",
                """Artificial intelligence has quickly become one of the most important technologies of the modern era.

From recommendation systems and voice assistants to generative AI tools, intelligent software is becoming part of everyday life.

One of the biggest changes brought by AI is the ability to process enormous amounts of information and turn it into useful results.

However, the technology also raises important questions about privacy, misinformation, employment and responsible use.

The future of AI will not simply be about making machines more powerful. It will also be about deciding how humans use that power."""
            ),
            (
                "The technology race shaping the next decade",
                "TECHNOLOGY",
                "September 24, 2026",
                "5 min read",
                "From powerful processors to intelligent software, technology is moving through a period of rapid change.",
                """Technology is developing faster than ever, with new advances appearing across computing, artificial intelligence, robotics and communication.

Modern devices are becoming more capable while also becoming smaller and more efficient.

The next decade could bring major changes to how people interact with computers, information and digital services."""
            ),
            (
                "Why cybersecurity matters more than ever",
                "CYBERSECURITY",
                "September 24, 2026",
                "4 min read",
                "As more of everyday life moves online, protecting personal information and digital systems has become increasingly important.",
                """Our lives are becoming increasingly connected to the internet.

Phones, computers, banking systems, social platforms and cloud services all depend on digital infrastructure.

Strong passwords, multi-factor authentication, software updates and cautious online behaviour are some of the basic steps people can take to improve their digital security."""
            ),
            (
                "What happens when humans and AI work together?",
                "FUTURE",
                "September 25, 2026",
                "5 min read",
                "The future of work may not be humans versus machines, but humans using intelligent systems as powerful tools.",
                """The conversation around artificial intelligence often focuses on what machines might replace.

A different perspective is to consider what happens when humans and AI work together.

AI systems can process information quickly, recognise patterns and assist with repetitive tasks. Humans bring creativity, judgement, context and responsibility."""
            ),
            (
                "The next generation of computing",
                "INNOVATION",
                "September 25, 2026",
                "6 min read",
                "Computing is evolving beyond traditional performance metrics as researchers explore new approaches to processing information.",
                """For decades, progress in computing was largely measured by faster processors and more powerful hardware.

Today, the picture is becoming more complicated.

Researchers are exploring specialised chips, advanced architectures, edge computing and other approaches designed for specific types of workloads."""
            )
        ]

        connection.executemany("""
            INSERT INTO articles (
                title,
                category,
                date,
                read_time,
                excerpt,
                content
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, starter_articles)

    connection.commit()
    connection.close()


init_database()


# =========================================
# LOGIN PROTECTION
# =========================================

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return function(*args, **kwargs)

    return wrapper


# =========================================
# HOMEPAGE
# =========================================

@app.route("/")
def home():

    connection = get_db()

    articles = connection.execute(
        "SELECT * FROM articles ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        articles=articles
    )


# =========================================
# ARTICLE PAGE
# =========================================

@app.route("/article/<int:article_id>")
def article_page(article_id):

    connection = get_db()

    article = connection.execute(
        "SELECT * FROM articles WHERE id = ?",
        (article_id,)
    ).fetchone()

    connection.close()

    if article is None:
        return "Article not found", 404

    return render_template(
        "article.html",
        article=article
    )


# =========================================
# ADMIN LOGIN
# =========================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template(
        "admin_login.html"
    )


# =========================================
# ADMIN LOGOUT
# =========================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route("/admin")
@admin_required
def admin_dashboard():

    connection = get_db()

    articles = connection.execute(
        "SELECT * FROM articles ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        articles=articles
    )


# =========================================
# NEW ARTICLE
# =========================================

@app.route("/admin/new", methods=["GET", "POST"])
@admin_required
def admin_new_article():

    if request.method == "POST":

        title = request.form.get("title")
        category = request.form.get("category")
        date = request.form.get("date")
        read_time = request.form.get("read_time")
        excerpt = request.form.get("excerpt")
        content = request.form.get("content")

        connection = get_db()

        connection.execute("""
            INSERT INTO articles (
                title,
                category,
                date,
                read_time,
                excerpt,
                content
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            category,
            date,
            read_time,
            excerpt,
            content
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "admin_new.html"
    )


# =========================================
# EDIT ARTICLE
# =========================================

@app.route("/admin/edit/<int:article_id>", methods=["GET", "POST"])
@admin_required
def edit_article(article_id):

    connection = get_db()

    article = connection.execute(
        "SELECT * FROM articles WHERE id = ?",
        (article_id,)
    ).fetchone()

    if article is None:
        connection.close()
        return "Article not found", 404

    if request.method == "POST":

        title = request.form.get("title")
        category = request.form.get("category")
        date = request.form.get("date")
        read_time = request.form.get("read_time")
        excerpt = request.form.get("excerpt")
        content = request.form.get("content")

        connection.execute("""
            UPDATE articles
            SET
                title = ?,
                category = ?,
                date = ?,
                read_time = ?,
                excerpt = ?,
                content = ?
            WHERE id = ?
        """, (
            title,
            category,
            date,
            read_time,
            excerpt,
            content,
            article_id
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("admin_dashboard")
        )

    connection.close()

    return render_template(
        "admin_edit.html",
        article=article
    )


# =========================================
# DELETE ARTICLE
# =========================================

@app.route("/admin/delete/<int:article_id>", methods=["POST"])
@admin_required
def delete_article(article_id):

    connection = get_db()

    connection.execute(
        "DELETE FROM articles WHERE id = ?",
        (article_id,)
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================
# SITEMAP
# =========================================

@app.route("/sitemap.xml")
def sitemap():

    connection = get_db()

    articles = connection.execute(
        "SELECT id FROM articles"
    ).fetchall()

    connection.close()

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

    return Response(
        xml,
        mimetype="application/xml"
    )


# =========================================
# ROBOTS
# =========================================

@app.route("/robots.txt")
def robots():

    robots_text = """User-agent: *
Allow: /

Sitemap: https://byteshift-w1bw.onrender.com/sitemap.xml
"""

    return Response(
        robots_text,
        mimetype="text/plain"
    )


# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)