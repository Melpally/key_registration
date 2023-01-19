from cs50 import SQL
from flask import Flask, render_template, flash, redirect, request, session
from datetime import datetime
from flask_session import Session


# Configure the application
app = Flask(__name__)

# Ensure that templates are auto reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///keys.db")

@app.route("/")
def keys():
    """Fetch the registered keys from the database"""
    keys = []
    keys_db = db.execute("SELECT * FROM keys")

    for key in keys_db:
        if (key["available"]):
            student = db.execute("SELECT name FROM students WHERE id == ?", key["id_student_returned"])
            keys.append({
                "room": key["room"],
                "available": key["available"],
                "id": key["id_student_returned"],
                "time": key["time_returned"],
                "name": student[0]["name"]
            })
        else:
            student = db.execute("SELECT name FROM students WHERE id == ?", key["id_student_took"])
            keys.append({
                "room": key["room"],
                "available": key["available"],
                "id": key["id_student_took"],
                "time": key["time_taken"],
                "name": student[0]["name"]
            })

    return render_template("keys.html", keys=keys)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user and update the database"""
    if request.method == "POST":
        room = request.form.get("room")
        id = request.form.get("id")
        name = request.form.get("name")
        action = request.form.get("action")
        time = datetime.now()
        key = db.execute("SELECT * FROM keys WHERE room == ?", room)

        # Ensure the correct input has been provided
        if (not room):
            flash("Please enter a valid room number!")
            return render_template("register.html")
        elif (not id):
            flash("Please enter a valid id number!")
            return render_template("register.html")
        elif (not action):
            flash("Please choose an action to complete!")
            return render_template("register.html")
        else:
            # Update the database based on the chosen action
            if (action == "take"):
                # Ensure the availability of the key
                if (key[0]["available"] == 1):
                    if (len(key) == 1):
                        db.execute("UPDATE keys SET available = ?, id_student_took = ?, time_taken = ? WHERE room == ?", 0, id, time, room)
                        db.execute("UPDATE students SET took = ?, returned = ? WHERE id == ?", 1, 0, id)
                        flash("Registered successfully!")
                        return redirect("/")
                    else:
                        db.execute("INSERT INTO keys (room, available, id_student_took, time_taken) VALUES (?, ?, ?, ?)", room, 0, id, time)
                        db.execute("UPDATE students SET took = ?, returned = ? WHERE id == ?", 1, 0, id)
                        flash("Registered successfully!")
                        return redirect("/")
                else:
                    flash("The key is already taken!")
                    return redirect("/")
            else:
                if key[0]["available"] == 0:
                    if (len(key) == 1):
                        db.execute("UPDATE keys SET available = ?, id_student_returned = ?, time_returned = ? WHERE room == ?", 1, id, time, room)
                        db.execute("UPDATE students SET returned = ?, took = ? WHERE id == ?", 1, 0, id)
                        flash("Registered successfully!")
                        return redirect("/")
                    else:
                        db.execute("INSERT INTO keys (room, available, id_student_returned, time_returned) VALUES (?, ?, ?, ?)", room, 1, id, time, room)
                        db.execute("UPDATE students SET returned = ?, took = ? WHERE id == ?", 1, 0, id)
                        flash("Registered successfully!")
                        return redirect("/")
                else:
                    flash("The key is already available!")
                    return redirect("/")
    else:
        return render_template("register.html")