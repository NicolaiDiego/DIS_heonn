import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import re
from flask import Flask, g, render_template, request, jsonify


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.join(BASE_DIR, 'dataset.json')

POSTGRES = {
    'dbname': 'hoenn_db',
    'user': 'postgres',
    'password': 'UIS',
    'host': 'db',
    'port': 5432
}

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=POSTGRES['dbname'],
            user=POSTGRES['user'],
            password=POSTGRES['password'],
            host=POSTGRES['host'],
            port=POSTGRES['port']
        )
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    conn = psycopg2.connect(**POSTGRES)
    cur = conn.cursor()

    cur.execute("DROP VIEW IF EXISTS trainer_details CASCADE")
    cur.execute("DROP TABLE IF EXISTS pokemon, trainers, locations CASCADE")

    cur.execute("""
    CREATE TABLE locations (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
    CREATE TABLE trainers (
        id SERIAL PRIMARY KEY,
        location_id INTEGER REFERENCES locations(id),
        name TEXT,
        money INTEGER,
        xp INTEGER
    );
    CREATE TABLE pokemon (
        id SERIAL PRIMARY KEY,
        trainer_id INTEGER REFERENCES trainers(id),
        name TEXT,
        level INTEGER,
        moves TEXT
    );
    CREATE VIEW trainer_details AS
        SELECT t.*, l.name AS location_name,
               (SELECT COUNT(*) FROM pokemon p WHERE p.trainer_id = t.id) AS pokemon_count
        FROM trainers t
        JOIN locations l ON t.location_id = l.id;
    """)

    with open(DATASET_FILE) as f:
        data = json.load(f)

    for loc in data:
        cur.execute('INSERT INTO locations (name) VALUES (%s) RETURNING id', (loc['name'],))
        loc_id = cur.fetchone()[0]
        for tr in loc['trainers']:
            cur.execute(
                'INSERT INTO trainers (location_id, name, money, xp) VALUES (%s, %s, %s, %s) RETURNING id',
                (loc_id, tr['name'], tr['money'], tr['xp'])
            )
            tr_id = cur.fetchone()[0]
            for p in tr['pokemon']:
                moves = ','.join(p['moves'])
                cur.execute(
                    'INSERT INTO pokemon (trainer_id, name, level, moves) VALUES (%s, %s, %s, %s)',
                    (tr_id, p['name'], p['level'], moves)
                )

    conn.commit()
    conn.close()



@app.route('/')
def index():
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM locations')
    locs = cur.fetchall()
    return render_template('index.html', locations=locs)

@app.route('/location/<int:loc_id>')
def location(loc_id):
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM locations WHERE id = %s', (loc_id,))
    loc = cur.fetchone()
    cur.execute('SELECT * FROM trainers WHERE location_id = %s', (loc_id,))
    trainers = cur.fetchall()
    return render_template('location.html', location=loc, trainers=trainers)

@app.route('/trainer/<int:trainer_id>')
def trainer(trainer_id):
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT t.*, l.name AS location_name
        FROM trainers t
        JOIN locations l ON t.location_id = l.id
        WHERE t.id = %s''', (trainer_id,))
    trainer = cur.fetchone()
    cur.execute('SELECT * FROM pokemon WHERE trainer_id = %s', (trainer_id,))
    pokemon = cur.fetchall()
    return render_template('trainer.html', trainer=trainer, pokemon=pokemon)

ROUTE_RE = re.compile(r'^[A-Za-z ]+$')

@app.route('/search')
def search():
    name = request.args.get('name', '').strip()
    if not ROUTE_RE.match(name):
        return jsonify({"error": "Invalid input"}), 400

    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT t.id, t.name, t.money, t.xp, l.name AS location_name
        FROM trainers t
        JOIN locations l ON t.location_id = l.id
        WHERE t.name ILIKE %s''',
        (f'%{name}%',))
    trainers = cur.fetchall()

    results = [{
        "id": t["id"],
        "name": t["name"],
        "money": t["money"],
        "xp": t["xp"],
        "location": t["location_name"]
    } for t in trainers]

    return jsonify(results)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
