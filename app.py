from flask import Flask,render_template,request,redirect,session,url_for,send_from_directory
import sqlite3
import os
from werkzeug.security import generate_password_hash,check_password_hash
import requests
from init_db import init_db

app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","dev-fallback-key")

CS_FIELDS = [
    "Frontend",
    "Backend",
    "Full Stack",
    "DevOps",
    "Data Science",
    "AI/ML",
    "System Design",
    "UI/UX",
    "Cyber Security",
    "Cloud Computing",
    "Mobile Development",
    "Game Development",
    "Blockchain",
    "Testing / QA"
]


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Ensure DB and `users` table exist before handling any requests
init_db("database.db")

def get_db():
    return sqlite3.connect("database.db")

def connection_status(user_id,other_id):
    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("""
       
      select status 
                   from connections
                   where(sender_id=? AND receiver_id=?)
                   or (sender_id=? and receiver_id=?)
                LIMIT 1
""",(user_id,other_id,other_id,user_id))
    
    row=cursor.fetchone()
    conn.close()

    if not row:
        return "none"
    
    return row[0]

def get_trending_articles():
    url="https://dev.to/api/articles?top=1&per_page=3"

    try:
        response=requests.get(url,timeout=5)
        response.raise_for_status()
        return response.json()
    
    except Exception:
        return []

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
    interest_set=set(i.strip().lower() for i in interest.split(","))
    

    cursor.execute("""
          select id,name,skill_level,interests
                   from users
                   where id !=?
                   
""",(user_id,))
    
    others=cursor.fetchall()

    matches=[]

    for uid,name,skill,interests in others:
        other_interest_set=set(i.strip().lower() for i in interests.split(","))

        common=interest_set & other_interest_set #intersection
        status=connection_status(user_id,uid)

        if common:
            matches.append({
                "id":uid,
                "name":name,
                "skill":skill,
                "common_interests":list(common),
                "status":status
            })
    conn.close()

    return matches

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        hashed_password=generate_password_hash(password)
        skill=request.form["skill_level"]
       
        interests_list=request.form.getlist("interests")
        interests_str=",".join(interests_list)

        conn=get_db()
        cursor=conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users(name,email,password,skill_level,interests) values(?,?,?,?,?)", 
                (name,email,hashed_password,skill,interests_str)
            
        )

            conn.commit()
            user_id=cursor.lastrowid
            

            session["user_id"]=user_id
            session["user_name"]=name

            return redirect("/dashboard")
        
        except sqlite3.IntegrityError:
            return render_template("signup.html",error="Email Alreday registred",fields=CS_FIELDS)
    
        finally:
            conn.close()

    return render_template("signup.html",fields=CS_FIELDS)
        


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
        cursor.execute("SELECT id,name,password FROM users WHERE email=? ",(email,))
        user=cursor.fetchone()
        conn.close()

        if user:
            user_id=user[0]
            name=user[1]
            stored_hash=user[2]

            if check_password_hash(stored_hash,password):
                session["user_id"]=user_id
                session["user_name"]=name
            
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
    # print("matches",matches)

    articles=get_trending_articles()
    
    return render_template("dashboard.html",name=session["user_name"],matches=matches,articles=articles)

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

@app.route("/connect",methods=["POST"])
def connect():
    if "user_id" not in session:
        return redirect("/login")
    
    sender_id=session["user_id"]
    receiver_id=request.form["receiver_id"]

    #to aviod self connect
    if str(sender_id) == receiver_id:
        return redirect("/dashboard")
    
    conn=get_db()
    cursor=conn.cursor()

    #prevent duplicate requests

    cursor.execute("""
        select id from connections
                   where sender_id=? and receiver_id=? and status='pending'
""",(sender_id,receiver_id))
    
    existing=cursor.fetchone()

    if not existing:

        cursor.execute("""
      insert into connections(sender_id,receiver_id)
                       values(?,?)

     
""",(sender_id,receiver_id))
    
        conn.commit()

    conn.close()

    return redirect("/dashboard")

@app.route("/connections/accept",methods=["POST"])
def accept_connection():
    if  "user_id" not in session:
        return redirect("/login")
    
    request_id=request.form["request_id"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("""
           UPDATE connections 
                   set status='accepted'
                   where id=? and receiver_id=?
 
""",(request_id,session["user_id"]))
    
    conn.commit()
    conn.close()
    
    return redirect("/connections")


@app.route("/connections/reject",methods=["POST"])
def reject_connection():
    if "user_id" not in session:
        return redirect("/login")
    
    request_id=request.form["request_id"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("""
     UPDATE connections
                   set status='rejected'
                   where id=? and receiver_id=?
 
""",(request_id,session["user_id"]))
    
    conn.commit()
    conn.close()
    
    return redirect("/connections")

@app.route("/connections")
def connections():
    if "user_id" not in session:
        return redirect("/login")
    
    user_id=session["user_id"]
    conn=get_db()
    cursor=conn.cursor()

    #for incoming requests

    cursor.execute("""
              SELECT c.id,u.name,u.skill_level,u.interests
                   from connections c
                   join users u on c.sender_id=u.id
                   where c.receiver_id=? and c.status='pending'

""",(user_id,))
    
    incoming=cursor.fetchall()

    #for sent requests
    cursor.execute("""

       select c.id,u.name
                   from connections c
                   join users u on c.receiver_id=u.id
                   where c.sender_id=? AND c.status='pending'
""",(user_id,))
    
    sent=cursor.fetchall()

    #accepted connections
    cursor.execute("""

          select u.id,u.name,u.skill_level
                   from connections c
                   join users u
                   on(u.id=c.sender_id or u.id=c.receiver_id)
                   where c.status='accepted'
                   AND(c.sender_id=? or c.receiver_id=?)
                   and u.id !=?
""",(user_id,user_id,user_id))
    
    accepted=cursor.fetchall()

    conn.close()

    return render_template(
        "connections.html",
        incoming=incoming,
        sent=sent,
        accepted=accepted
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
