from flask import Flask, render_template, request, jsonify, send_from_directory
import random, os
from datetime import datetime, timezone

app = Flask(__name__, static_folder='static')

# ── PRIZES ──────────────────────────────────────────────
WIN_PRIZES = [
    "iPhone 17 Pro Max",
    "MacBook Pro",
    "iPad Pro",
    "Samsung Galaxy Tab S9",
    "HP Laptop",
    "$500 Gift Card",
    "$3,000 Cash",
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
DAILY_POOL     = 30

# ── SERVER-SIDE POOL STATE ───────────────────────────────
_pool_date    = ""
_pool_claimed = 0

def today_key():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def get_pool_state():
    global _pool_date, _pool_claimed
    today = today_key()
    if _pool_date != today:
        _pool_date    = today
        _pool_claimed = 0
    return _pool_claimed, max(0, DAILY_POOL - _pool_claimed)

# ── ROUTES ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pool', methods=['GET'])
def pool():
    claimed, left = get_pool_state()
    return jsonify({'claimed': claimed, 'left': left, 'total': DAILY_POOL})

@app.route('/spin', methods=['POST'])
def spin():
    global _pool_claimed
    data       = request.get_json(silent=True) or {}
    jackpot_ok = data.get('jackpotReady', False)

    claimed, left = get_pool_state()

    pool  = WIN_PRIZES + TRY_AGAIN
    prize = random.choice(pool)
    is_try_again = prize in TRY_AGAIN

    if prize == JACKPOT_PRIZE and not jackpot_ok:
        prize        = FALLBACK_PRIZE
        is_try_again = False

    if not is_try_again and left > 0:
        _pool_claimed += 1

    claimed_after, left_after = get_pool_state()

    return jsonify({
        'success'    : True,
        'prize'      : prize,
        'isTryAgain' : is_try_again,
        'isCash'     : prize == JACKPOT_PRIZE,
        'poolClaimed': claimed_after,
        'poolLeft'   : left_after,
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
