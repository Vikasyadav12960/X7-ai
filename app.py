from flask import Flask, render_template, request
from db import init_db, save_scan, get_recent_scans

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    url = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            # placeholder verdict until we build real detection in Step 4
            save_scan(url, "pending", 0)
    scans = get_recent_scans()
    return render_template("index.html", url=url, scans=scans)


if __name__ == "__main__":
    app.run(debug=True)