from flask import Flask,render_template,request,redirect,session,url_for
import sqlite3

from init_db import init_db

app=Flask(__name__)
app.secret_key="super-secret-key-change-this"

# Ensure DB and `users` table exist before handling any requests
init_db("database.db")

def get_db():
    return sqlite3.connect("database.db")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        skill=request.form["skill_level"]
        interests=request.form["interests"]

        conn=get_db()
        cursor=conn.cursor()
        cursor.execute(
            "INSERT INTO users(name,email,password,skill_level,interests) values(?,?,?,?,?)", 
            (name,email,password,skill,interests)
            
        )

        conn.commit()
        conn.close()

        return redirect("/profile")
    
    return render_template("signup.html")

@app.route("/profile")
def profile():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    user=cursor.fetchone()
    conn.close()

    return f"WELCOME {user[1]}! Skill:{user[4]},Interests: {user[5]}"


@app.route("/")
def home():
    return "Welcome to CodeMate 🚀 — go to /signup"

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        conn=get_db()
        cursor=conn.cursor()
        cursor.execute("SELECT id,name FROM users WHERE email=? AND password=?",(email,password))
        user=cursor.fetchone()
        conn.close()

        if user:
            session["user_id"]=user[0]
            session["user_name"]=user[1]
            return redirect("/dashboard")
        
        else:
            return render_template("login.html",error="Invalid email or password")
        
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    
    return render_template("dashboard.html",name=session["user_name"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if __name__=="__main__":
    app.run(debug=True)