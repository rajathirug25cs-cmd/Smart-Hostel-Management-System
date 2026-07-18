from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = "hostel123"


# ---------------- DATABASE ----------------

def create_database():

    conn = sqlite3.connect("hostel.db")
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        room_no TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        breakfast TEXT,
        lunch TEXT,
        dinner TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaint(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        complaint TEXT,
        status TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        status TEXT
    )
    """)


    conn.commit()
    conn.close()



create_database()



# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("index.html")



# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        if username == "admin" and password == "1234":

            session["user"] = "admin"

            return redirect(url_for("dashboard"))



        elif username == "student" and password == "1234":

            session["user"] = "student"

            return redirect(url_for("dashboard"))


        else:

            return "Invalid Username or Password"


    return render_template("login.html")



# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(url_for("login"))


    return render_template(
        "dashboard.html",
        user=session["user"]
    )



# ---------------- MENU VIEW ----------------

@app.route("/menu")
def menu():

    conn = sqlite3.connect("hostel.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu")

    data = cursor.fetchall()

    conn.close()


    return render_template(
        "menu.html",
        menu=data
    )



# ---------------- ADD MENU ----------------

@app.route("/add_menu", methods=["GET","POST"])
def add_menu():

    if "user" not in session or session["user"] != "admin":

        return redirect(url_for("login"))


    if request.method == "POST":

        day = request.form["day"]
        breakfast = request.form["breakfast"]
        lunch = request.form["lunch"]
        dinner = request.form["dinner"]


        conn = sqlite3.connect("hostel.db")

        cursor = conn.cursor()


        cursor.execute(
        """
        INSERT INTO menu(day,breakfast,lunch,dinner)
        VALUES(?,?,?,?)
        """,
        (day,breakfast,lunch,dinner)
        )


        conn.commit()
        conn.close()


        return redirect(url_for("menu"))


    return render_template("add_menu.html")



# ---------------- COMPLAINT ----------------

@app.route("/complaint", methods=["GET","POST"])
def complaint():

    if "user" not in session:

        return redirect(url_for("login"))


    if request.method == "POST":

        name = request.form["name"]

        complaint = request.form["complaint"]


        conn = sqlite3.connect("hostel.db")

        cursor = conn.cursor()


        cursor.execute(
        """
        INSERT INTO complaint(name,complaint,status)
        VALUES(?,?,?)
        """,
        (name,complaint,"Pending")
        )


        conn.commit()

        conn.close()


        return "Complaint Submitted Successfully"


    return render_template("complaint.html")



# ---------------- VIEW COMPLAINT ----------------

@app.route("/view_complaints")
def view_complaints():

    if "user" not in session or session["user"] != "admin":

        return redirect(url_for("login"))


    conn = sqlite3.connect("hostel.db")

    cursor = conn.cursor()


    cursor.execute("SELECT * FROM complaint")


    data = cursor.fetchall()


    conn.close()


    return render_template(
        "view_complaints.html",
        complaints=data
    )



# ---------------- UPDATE COMPLAINT ----------------

@app.route("/update_complaint/<int:id>")
def update_complaint(id):

    conn = sqlite3.connect("hostel.db")

    cursor = conn.cursor()


    cursor.execute(
    """
    UPDATE complaint
    SET status='Resolved'
    WHERE id=?
    """,
    (id,)
    )


    conn.commit()

    conn.close()


    return redirect(url_for("view_complaints"))



# ---------------- ADD STUDENT ROOM ----------------

@app.route("/add_student", methods=["GET","POST"])
def add_student():

    if "user" not in session or session["user"] != "admin":

        return redirect(url_for("login"))


    if request.method == "POST":

        name = request.form["name"]

        department = request.form["department"]

        room_no = request.form["room_no"]


        conn = sqlite3.connect("hostel.db")

        cursor = conn.cursor()


        cursor.execute(
        """
        INSERT INTO students(name,department,room_no)
        VALUES(?,?,?)
        """,
        (name,department,room_no)
        )


        conn.commit()

        conn.close()


        return "Room Allocated Successfully"


    return render_template("add_student.html")



# ---------------- STUDENT LIST ----------------

@app.route("/students")
def students():

    if "user" not in session or session["user"] != "admin":

        return redirect(url_for("login"))


    conn = sqlite3.connect("hostel.db")

    cursor = conn.cursor()


    cursor.execute("SELECT * FROM students")


    data = cursor.fetchall()


    conn.close()


    return render_template(
        "students.html",
        students=data
    )



# ---------------- MY ROOM ----------------

@app.route("/my_room")
def my_room():

    if "user" not in session:

        return redirect(url_for("login"))


    conn = sqlite3.connect("hostel.db")

    cursor = conn.cursor()


    cursor.execute("SELECT * FROM students LIMIT 1")


    data = cursor.fetchone()


    conn.close()


    return render_template(
        "my_room.html",
        student=data
    )



# ---------------- ATTENDANCE ----------------

@app.route("/attendance", methods=["GET","POST"])
def attendance():

    if "user" not in session or session["user"] != "admin":

        return redirect(url_for("login"))


    if request.method == "POST":

        name = request.form["name"]

        date = request.form["date"]

        status = request.form["status"]


        conn = sqlite3.connect("hostel.db")

        cursor = conn.cursor()


        cursor.execute(
        """
        INSERT INTO attendance(name,date,status)
        VALUES(?,?,?)
        """,
        (name,date,status)
        )


        conn.commit()

        conn.close()


        return "Attendance Added Successfully"


    return render_template("attendance.html")



# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect(url_for("login"))



# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(debug=True)