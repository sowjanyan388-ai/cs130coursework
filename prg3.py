from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Update these with your actual MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sowjanya123@78', 
    'database': 'school_db'      
}

def get_db():
    """Helper function to cleanly open connections."""
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Note: MySQL uses AUTO_INCREMENT and VARCHAR/INT datatypes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT DEFAULT 0,
            course VARCHAR(100) DEFAULT 'Undecided'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/students', methods=['POST'])
def insert_student():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Grab the course, default to 'Undecided' if missing
    course = data.get('course', 'Undecided') 
    
    # 2. Add course to the INSERT query and the %s placeholders
    cursor.execute(
        'INSERT INTO students (name, email, age, course) VALUES (%s, %s, %s, %s)',
        (data['name'], data['email'], data.get('age', 0), course)
    )
    
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"message": "Student created", "id": student_id}), 201

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db()
    # dictionary=True automatically formats the rows as JSON-ready dictionaries!
    cursor = conn.cursor(dictionary=True) 
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    
    return jsonify(students), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
