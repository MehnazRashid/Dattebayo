from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

BASE_URL = "https://dattebayo-api.onrender.com"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    user_input = request.args.get('name', '').strip()
    if not user_input:
        return render_template('index.html', error="Please enter a character name.")

    user_word = user_input.lower()

    # API request
    try:
        resp = requests.get(
            f"{BASE_URL}/characters",
            params={"name": user_input},
            timeout=8
        )
    except requests.RequestException:
        return render_template('index.html', error=f'No character named "{user_input}" was found.')

    if resp.status_code != 200:
        return render_template('index.html', error=f'No character named "{user_input}" was found.')

    data = resp.json()

    # Extract characters
    if isinstance(data, dict) and "characters" in data:
        characters = data["characters"]
    else:
        characters = []

    if not characters:
        return render_template('index.html', error=f'No character named "{user_input}" was found.')

    # Full word match only
    matches = []
    for c in characters:
        words = c["name"].lower().split()
        if user_word in words:
            matches.append(c)

    if not matches:
        return render_template('index.html', error=f'No character named "{user_input}" was found.')

    # Show all exact-word matches
    return render_template(
        'results.html',
        characters=matches,
        query=user_input
    )


if __name__ == '__main__':
    app.run(debug=True)
