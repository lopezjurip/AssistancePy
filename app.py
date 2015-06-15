import os
from flask import Flask, request, jsonify, Response
from student import Student

# Initialization
app = Flask(__name__)
app.debug = True

students = {s.id: s for s in [
    Student("Pato", "MrPatiwi", True)
]}


# Controllers
@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/students", methods=['GET', 'POST'])
def students_index():
    if request.method == 'GET':
        items = [s.serialize() for (identifier, s) in students.iteritems()]
        return jsonify(students=items)

    elif request.method == 'POST':
        name = request.values.get('name')
        username = request.values.get('username')
        assistance = request.values.get('assistance')

        if name and username and assistance:
            student = Student(name, username, assistance)
            students[student.id] = student
            return jsonify(student.serialize()), 201
        else:
            return Response(status=400)

    else:
        return Response(status=405)


@app.route("/students/<student_id>", methods=['GET', 'DELETE', 'PATCH'])
def student(student_id):
    if student_id.isdigit() == False:
        return Response(status=404)

    student_id = int(student_id)

    if student_id not in students:
        return Response(status=404)

    if request.method == 'GET':
        return jsonify(students[student_id].serialize())

    elif request.method == 'DELETE':
        return jsonify(students.pop(student_id, None).serialize())

    elif request.method == 'PATCH':
        student = students[student_id]
        student.name = request.args.get('name')
        student.username = request.args.get('username')
        student.assistance = request.args.get('assistance')
        return jsonify(student), 202

    else:
        return Response(status=405)


# Start app
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )
