from flask import Flask, render_template, request
from db import init_db, save_scan, get_recent_scans
from checker import check_url

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            score, verdict, reasons = check_url(url)
            save_scan(url, verdict, score, reasons)
            result = {"url": url, "score": score, "verdict": verdict, "reasons": reasons}
    scans = get_recent_scans()
    return render_template("index.html", result=result, scans=scans)


if __name__ == "__main__":
    app.run(debug=True)