from flask import Flask, jsonify
from flask.ext.cors import CORS
import sqlite3

app = Flask(__name__)
cors = CORS(app)

empty_database_quote = {
    "quote": "Well what do you know? I ran out of piggies.",
    "author": "Tweety bird",
    "comment": "THE DATABASE IS EMPTY"
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_random_quote(path):
    with sqlite3.connect('quotes.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT quote, name FROM quote '\
                    'INNER JOIN author ON quote.author = author.id '\
                    'ORDER BY random() LIMIT 1;')
        rows = cur.fetchone()
    if rows:
        return jsonify(quote=rows[0], author=rows[1])
    else:
        return jsonify(**empty_database_quote)


if __name__ == '__main__':
    app.run(debug=True)
