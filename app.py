import json
import logging
from datetime import datetime
from random import randint

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

# OpenTelemetry tutorial:
# https://opentelemetry.io/docs/languages/python/getting-started/
# https://scoutapm.com/blog/configuring-opentelemetry-python

# Set OpenTelemetry Resource Attributes
resource = Resource(attributes={
    "service.name": __name__
})

# Configure OpenTelemetry Tracer and Exporter
trace.set_tracer_provider(TracerProvider(resource=resource))

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

# Acquire a meter.
meter = metrics.get_meter("diceroller.meter")
# Now create a counter instrument to make measurements with
roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply OpenTelemetry Instrumentation
FlaskInstrumentor().instrument_app(app)
URLLibInstrumentor().instrument()


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
    with tracer.start_as_current_span("index") as span:
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
            span.set_attribute("tasks.total", len(tasks))
            return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    with tracer.start_as_current_span("delete") as span:
        task_to_delete = Todo.query.get_or_404(id)
        span.set_attribute("tasks.id", task_to_delete.id)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    with tracer.start_as_current_span("update") as span:
        task = Todo.query.get_or_404(id)
        span.set_attribute("tasks.id", task.id)
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
    with tracer.start_as_current_span("tasks") as span:
        if request.method == 'POST':
            task_id = request.get_json().get('id')
            task = Todo.query.get(task_id)
            span.set_attribute("tasks.id", task.id)
            if task:
                return jsonify(task.to_dict())
            else:
                return 'Task not found', 404
        else:
            tasks = Todo.query.all()
            tasks_dict = [task.to_dict() for task in tasks]
            span.set_attribute("tasks.total", len(tasks_dict))
            response = app.response_class(
                response=json.dumps(tasks_dict),
                status=200,
                mimetype='application/json'
            )
            return response


@app.route("/rolldice")
def roll_dice():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll_dice") as roll_span:
        player = request.args.get('player', default=None, type=str)
        result = str(roll())
        roll_span.set_attribute("roll.value", result)
        # This adds 1 to the counter for the given roll value
        roll_counter.add(1, {"roll.value": result})
        if player:
            logger.warning("%s is rolling the dice: %s", player, result)
        else:
            logger.warning("Anonymous player is rolling the dice: %s", result)
        return result


def roll():
    with tracer.start_as_current_span("roll") as roll_span:
        roll_span.set_attribute("roll.value", "Rolling the Dice")
        return randint(1, 6)


if __name__ == "__main__":
    app.run(debug=True)
