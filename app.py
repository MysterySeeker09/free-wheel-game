from flask import Flask, render_template, request, jsonify, send_from_directory
import random, os

app = Flask(__name__, static_folder='static')

# ── PRIZES ──────────────────────────────────────────────
WIN_PRIZES = [
    "$3,000 Cash",
    "iPhone 17 Pro Max",
    "MacBook Pro",
    "iPad Pro",
    "Samsung Galaxy Tab S9",
    "$500 Gift Card",
    "HP Laptop",
]

TRY_AGAIN = [
    "Try Again",
    "Not This Time",
    "Almost!",
    "Keep Spinning",
    "Next Time!",
    "So Close!",
]

JACKPOT_PRIZE  = "$3,000 Cash"
FALLBACK_PRIZE = "iPhone 17 Pro Max"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin', methods=['POST'])
def spin():
    data        = request.get_json(silent=True) or {}
    jackpot_ok  = data.get('jackpotReady', False)

    pool  = WIN_PRIZES + TRY_AGAIN
    prize = random.choice(pool)

    if prize == JACKPOT_PRIZE and not jackpot_ok:
        prize = FALLBACK_PRIZE

    is_try_again = prize in TRY_AGAIN
    return jsonify({
        'success'    : True,
        'prize'      : prize,
        'isTryAgain' : is_try_again,
        'isCash'     : prize == JACKPOT_PRIZE,
    })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )

@app.route('/og-image.png')
def og_image():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'og-image.png', mimetype='image/png'
    )

if __name__ == '__main__':
    app.run(debug=True)
