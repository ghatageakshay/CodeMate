from flask import Flask,render_template,request,redirect,session,url_for,send_from_directory
import sqlite3
import os

from init_db import init_db

app=Flask(__name__)
app.secret_key="super-secret-key-change-this"

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Ensure DB and `users` table exist before handling any requests
init_db("database.db")

def get_db():
    return sqlite3.connect("database.db")

def get_matches(user_id):
    conn=get_db()
    cursor=conn.cursor()

    #get current user info
    cursor.execute("select skill_level,interests from users where id=?",(user_id,))
    user=cursor.fetchone()

    if not user:
        conn.close()
        return []
    
    skill,interest=user

    cursor.execute("""
          select id,name,skill_level,interests
                   from users
                   where id !=?
                   and(skill_level=? or interests=?)
""",(user_id,skill,interest))
    
    matches=cursor.fetchall()
    conn.close()

    return matches

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
        try:
            cursor.execute(
                "INSERT INTO users(name,email,password,skill_level,interests) values(?,?,?,?,?)", 
                (name,email,password,skill,interests)
            
        )

            conn.commit()
            user_id=cursor.lastrowid
            

            session["user_id"]=user_id
            session["user_name"]=name

            return redirect("/dashboard")
        
        except sqlite3.IntegrityError:
            return render_template("signup.html",error="Email Alreday registred")
    
        finally:
            conn.close()

    return render_template("signup.html")
        


# @app.route("/profile")
# def profile():
#     conn=get_db()
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
#     user=cursor.fetchone()
#     conn.close()

#     return f"WELCOME {user[1]}! Skill:{user[4]},Interests: {user[5]}"


@app.route("/")
def home():
    return render_template("home.html")

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
    
    user_id=session["user_id"]
    matches=get_matches(user_id)
    print("matches",matches)
    
    return render_template("dashboard.html",name=session["user_name"],matches=matches)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")
    
    user_id=session["user_id"]
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("select name,email,skill_level,interests FROM users WHERE id=?",(user_id,))
    user=cursor.fetchone()
    
    return render_template("profile.html",user=user)

@app.route("/profile/edit",methods=["GET","POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")
    
    conn=get_db()
    cursor=conn.cursor()

    if request.method=="POST":
        name=request.form["name"]
        skill=request.form["skill_level"]
        interests=request.form["interests"]

        cursor.execute("""
                       UPDATE users
                       set name=?,skill_level=?,interests=?
                       where id=?
                       """,
                       (name,skill,interests,session["user_id"])

        )

        conn.commit()
        conn.close()

        session["user_name"]=name 
        return redirect("/profile")
    
    cursor.execute("SELECT name,skill_level,interests from users where id=?",(session["user_id"],))
    user=cursor.fetchone()
    conn.close()

    return render_template("edit_profile.html",user=user)
if __name__=="__main__":
    app.run(debug=True)