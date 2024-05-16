import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

    # Make the model serializable
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date_created': self.date_created.isoformat()
        }


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        task_id = request.get_json().get('id')
        task = Todo.query.get(task_id)
        if task:
            return jsonify(task.to_dict())
        else:
            return 'Task not found', 404
    else:
        tasks = Todo.query.all()
        tasks_dict = [task.to_dict() for task in tasks]
        response = app.response_class(
            response=json.dumps(tasks_dict),
            status=200,
            mimetype='application/json'
        )
        return response


if __name__ == "__main__":
    app.run(debug=True)
