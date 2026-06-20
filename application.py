from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Home page
@app.route("/")
def home():
    people = Person.query.all()
    return render_template("index.html", people=people)

# Add a new person
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]

    if name:
        new_person = Person(name=name)
        db.session.add(new_person)
        db.session.commit()

    return redirect("/")

# Delete a person
@app.route("/delete/<int:id>")
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)