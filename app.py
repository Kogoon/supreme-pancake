#from elasticapm.contrib.flask import  ElasticAPM
from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#apm = ElasticAPM(app)

# or configure to use ELASTIC_APM in your application's settings
from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
# Set the required service name. Allowed characters:
# a-z, A-Z, 0-9, -, _, and space
#'SERVICE_NAME': 'unknown-python-service',
'SERVICE_NAME': 'python-service',

# Use if APM Server requires a secret token
'SECRET_TOKEN': 'asdfqwer1234',

# Set the custom APM Server URL (default: http://localhost:8200)
'SERVER_URL': 'http://localhost:8200',

# Set the service environment
'ENVIRONMENT': 'production',
}

apm = ElasticAPM(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #nullable blank Flase
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


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
           return 'There was a issue updating your task'
    else:
        return render_template('update.html', task=task)


if __name__  == '__main__':
    db.create_all()
    app.run(debug=True)
