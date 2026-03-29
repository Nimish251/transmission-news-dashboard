from flask import Flask, render_template
from datetime import datetime
from news_fetcher import get_news

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    news_items = get_news(limit=5)
    last_updated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return render_template("index.html", news_items=news_items, last_updated=last_updated)


if __name__ == "__main__":
    app.run(debug=True)