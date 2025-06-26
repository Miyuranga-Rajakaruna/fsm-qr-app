from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("qr_codes.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS qrcodes (code TEXT PRIMARY KEY, remaining INTEGER)")
    c.execute("SELECT COUNT(*) FROM qrcodes")
    if c.fetchone()[0] == 0:
        for code in ['458325', '917634', '123879', '650432', '874120',
                     '320194', '562879', '703218', '492761', '819374',
                     '205948', '764321', '186239', '937540', '384710',
                     '628190', '749302', '910283', '135720', '843910']:
            c.execute("INSERT INTO qrcodes (code, remaining) VALUES (?, ?)", (code, 3))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_qr/<code>")
def check_qr(code):
    conn = sqlite3.connect("qr_codes.db")
    c = conn.cursor()
    c.execute("SELECT remaining FROM qrcodes WHERE code = ?", (code,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return jsonify({"valid": False})
    return jsonify({"valid": True, "remaining": row[0]})

@app.route("/redeem_qr/<code>", methods=["POST"])
def redeem_qr(code):
    conn = sqlite3.connect("qr_codes.db")
    c = conn.cursor()
    c.execute("UPDATE qrcodes SET remaining = remaining - 1 WHERE code = ? AND remaining > 0", (code,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
