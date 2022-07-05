from datetime import datetime
from email.policy import default
# from turtle import title
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# the below coed is used set false and SQLALCHEMY_TRACK_MODIFICATIONS is used for signal emiting.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # the --__repr__ function returns the string representation of the object passed. Here it prints object passed from the Todo.
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# @app.route("/", methods=["GET", "POST"])
# def hello_world():
    
#     if request.method == "POST":
#         print("post successfully")
#     #     # print(request.form['title'])
#     todo = Todo(title="First Todo",
#                 desc="Start Investing in the Stocks Market.")
#     db.session.add(todo)
#     db.session.commit()
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return render_template("index.html", allTodo=allTodo)
#     # return "<p>Hello, World!</p>"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        # print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is product page.'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        # print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    # print(allTodo)
    # return 'this is product page.'
    # return redirect('/')
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # return 'this is product page.'
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
