from flask import Flask, request, jsonify
from mongoengine import Document, StringField, IntField, EmailField, connect

app = Flask(__name__)

# Configure the MongoDB database
app.config['MONGODB_SETTINGS'] = {
    'db': 'school',
    'host': 'localhost',
    'port': 27017
}

# Connect to MongoDB
connect('school', host='localhost', port=27017)

class Student(Document):
    name = StringField(required=True, max_length=100)
    roll_number = StringField(required=True, unique=True)
    age = IntField(required=True, min_value=1)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(required=True, unique=True, max_length=15)

@app.route('/')
def home():
    return "Welcome to the Student API", 200

# Add student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    try:
        student = Student(
            name=data['name'],
            roll_number=data['roll_number'],
            age=data['age'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        student.save()
        return jsonify(student.to_json()), 201
    except Exception as e:
        return str(e), 400

# Edit student
@app.route('/students/<roll_number>', methods=['PUT'])
def edit_student(roll_number):
    data = request.get_json()
    try:
        student = Student.objects.get(roll_number=roll_number)
        student.update(
            name=data.get('name', student.name),
            age=data.get('age', student.age),
            email=data.get('email', student.email),
            phone_number=data.get('phone_number', student.phone_number)
        )
        return jsonify(Student.objects.get(roll_number=roll_number).to_json()), 200
    except Exception as e:
        return str(e), 400

# Delete student
@app.route('/students/<roll_number>', methods=['DELETE'])
def delete_student(roll_number):
    try:
        student = Student.objects.get(roll_number=roll_number)
        student.delete()
        return '', 204
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
