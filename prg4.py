from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
# Database changed back to college_db
DB_CONFIG = {'host':'localhost', 'user':'root', 'password':'Sowjanya123@78', 'database':'college_db'}

def db(query, args=(), fetch=None):
    """Executes DB queries. Auto-commits if not a SELECT statement."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute(query, args)
    if 'SELECT' not in query: conn.commit()
    
    res = cur.fetchall() if fetch == 'all' else (cur.fetchone() if fetch == 'one' else cur.lastrowid or cur.rowcount)
    conn.close()
    return res

def init_db():
    db('CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), age INT DEFAULT 0)')

# --- CREATE (POST) and READ (GET ALL) ---
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        return jsonify(db('SELECT * FROM students', fetch='all')), 200
    
    d = request.get_json()
    new_id = db('INSERT INTO students (name, email, age) VALUES (%s, %s, %s)', (d['name'], d['email'], d.get('age', 0)))
    return jsonify({"message": "Created", "id": new_id}), 201

# --- READ ONE (GET), UPDATE NAME (PATCH), DELETE (DELETE) ---
@app.route('/students/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def student(id):
    if request.method == 'GET':
        data = db('SELECT * FROM students WHERE id = %s', (id,), fetch='one')
        return (jsonify(data), 200) if data else (jsonify({"error": "Not found"}), 404)
        
    # Requirement 4.b: Delete student record by ID
    if request.method == 'DELETE':
        count = db('DELETE FROM students WHERE id = %s', (id,))
        return (jsonify({"message": "Student deleted"}), 200) if count else (jsonify({"error": "Not found"}), 404)
        
    # Requirement 4.a: Update student name by ID
    if request.method == 'PATCH':
       d = request.get_json()

    if not d or 'name' not in d:
       return jsonify({
            "error": "Please provide a 'name' to update"
        }), 400

    # Check whether student exists
    data = db(
        'SELECT * FROM students WHERE id = %s',
        (id,),
        fetch='one'
    )

    if not data:
        return jsonify({
            "error": "Not found"
        }), 404

    # Update name
    db(
        'UPDATE students SET name=%s WHERE id=%s',
        (d['name'], id)
    )

    return jsonify({
        "message": "Student name updated"
    }), 200
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

