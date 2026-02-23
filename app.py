from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Your 11 prizes (duplicates give higher odds for some)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin', methods=['POST'])
def spin():
    # No IP limit, no storage — just pick a random prize every time
    prize = random.choice(prizes)
    
    return jsonify({
        'prize': prize,
        'success': True
    })

# This line is only for local testing (Render ignores it)
if __name__ == '__main__':
    app.run(debug=True)
