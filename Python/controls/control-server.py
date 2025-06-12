from flask import Flask, render_template, request, jsonify
import random
import socket

app = Flask(__name__)

CONTROLS = [
    "arrowup",
    "arrowdown",
    "arrowleft",
    "arrowright",
    "space",
    "enter",
    "escape",
    "w",
    "a",
    "s",
    "d",
]
CONTROL_ICONS = ["↑", "↓", "←", "→", "␣", "↵", "⎋ Esc", "W", "A", "S", "D"]


def send_udp_message(message):
    udp_rec = "led-box.bbrouter"
    try:
        udp_ip = socket.gethostbyname(udp_rec)
    except socket.gaierror:
        udp_ip = "localhost"
    udp_port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (udp_ip, udp_port))
    sock.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/random-control")
def random_control():
    idx = random.randint(0, len(CONTROLS) - 1)
    return jsonify({"control": CONTROLS[idx], "icon": CONTROL_ICONS[idx]})


@app.route("/key-pressed", methods=["POST"])
def key_pressed():
    data = request.get_json()
    key = data.get("key", "")
    if key in CONTROLS:
        send_udp_message(key)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})


if __name__ == "__main__":
    app.run(port=8060)
