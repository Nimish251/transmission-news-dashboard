from flask import Flask, render_template
from datetime import datetime
from news_fetcher import get_news

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    region_data = get_news()
    last_updated = datetime.now().strftime("%d %b %Y, %I:%M %p")

    return render_template(
        "index.html",
        region_data=region_data,
        last_updated=last_updated
    )

if __name__ == "__main__":
    app.run(debug=True)