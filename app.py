from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session security

# Your 11 prizes (with duplicates = higher odds)
prizes = [
    "iPhone 15 Pro Max", "iPhone 15 Pro Max",
    "iPhone 17 Pro Max", "iPhone 17 Pro Max",
    "iPhone 16",
    "Samsung Tablet",
    "iPad", "iPad",
    "MacBook Pro",
    "HP Laptop",
    "Dell Laptop"
]

# Track spins per IP (in-memory for simplicity; use Redis/DB for production)
spin_counts = {}  # ip -> count

MAX_SPINS = 3

@app.route('/')
def index():
    ip = request.remote_addr
    spins_used = spin_counts.get(ip, 0)
    remaining = max(0, MAX_SPINS - spins_used)
    
    return render_template('index.html', remaining=remaining, max_spins=MAX_SPINS)

@app.route('/spin', methods=['POST'])
def spin():
    ip = request.remote_addr
    
    if ip not in spin_counts:
        spin_counts[ip] = 0
    
    if spin_counts[ip] >= MAX_SPINS:
        return jsonify({'error': 'Max spins reached (3 per IP). Come back later!'})
    
    # Spin logic
    prize = random.choice(prizes)
    spin_counts[ip] += 1
    remaining = MAX_SPINS - spin_counts[ip]
    
    return jsonify({
        'prize': prize,
        'spins_used': spin_counts[ip],
        'remaining': remaining
    })

# if __name__ == '__main__':
#     app.run()