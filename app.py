from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"ok": True, "msg": "Лаба 1: монолит работает"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})
