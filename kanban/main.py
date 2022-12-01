import os
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request,jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime
import json
from flask_cors import CORS
current_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"testdb.sqlite3")
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

usersid=random.randint(2,10000)
listsid=random.randint(2,10000)
cardsid=random.randint(2,10000)
class Users(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    password =db.Column(db.String,nullable=False)
    username = db.Column(db.String, unique=True,nullable=False)
class Auth(db.Model):
    __tablename__='auth'
    email=db.Column(db.String,primary_key=True)
    auth=db.Column(db.Integer)
class Lists(db.Model):
    __tablename__='lists'
    userid=db.Column(db.Integer,nullable=False)
    listname = db.Column(db.String,nullable=False)
    # cardid = db.Column(db.Integer,nullable=False)
    listid=db.Column(db.Integer, primary_key=True,nullable=False)
class Cards(db.Model):
    __tablename__='cards'
    card_id=db.Column(db.Integer,nullable=False, primary_key=True)
    card_name=db.Column(db.String,nullable=False)
    card_txt = db.Column(db.String,nullable=False)
    card_date = db.Column(db.String,nullable=False)
    card_status = db.Column(db.Integer,nullable=False)
    listid=db.Column(db.Integer,nullable=False)
    userid=db.Column(db.Integer,nullable=False)




@app.route("/login/<uname>/<passw>",methods=["Get"])

def userlogin(uname,passw):
    if request.method=="GET":
        user1=Users.query.filter_by(username=uname).first()
        if user1==None:
            return jsonify(auth="False",user="False")
        elif user1.password==passw:
            user2=Auth.query.filter_by(email=user1.username).first()
            user2.auth=1
            db.session.commit()
            return jsonify(auth="True",user="True")
        else:
            return jsonify(auth="False",user="True")
@app.route("/getauth/<id0>",methods=["Get"])
def getauth(id0):
    if request.method=="GET":
        user2=Auth.query.filter_by(email=id0).first()
        if user2.auth==1:
            return jsonify(auth="True")
        else:
            return jsonify(auth="False")
@app.route("/getlist/<id0>",methods=["Get"])
def getlist(id0):
    if request.method=="GET":
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(userid=user1.id).all()
        d={}
        c=[]
        for i in list:
            d[i.listname]=[]
            c.append(i.listname)
        for i in list:
            cards=Cards.query.filter_by(listid=i.listid).all()
            for j in cards:

                d[i.listname].append([j.card_name,j.card_txt,j.card_date,j.card_status])
                g=[j.card_name,j.card_txt,j.card_date,j.card_status,j.listid]
                print(g)
        # d['userlist']=c
        return jsonify(d)


@app.route("/createlist/<id0>/<lisname>",methods=["Get"])
def createlist(id0,lisname):
    if request.method=="GET":
        global listsid
        user1=Users.query.filter_by(username=id0).first()
        list1=Lists(userid=user1.id,listname=lisname,listid=listsid)
        listsid+=1
        db.session.add(list1)
        db.session.commit()
        return jsonify(commit='True')
        
@app.route("/addcard/<id0>/<lisname>/<summary>/<date>/<lname>",methods=["Get"])
def addcard(id0,lisname,summary,date,lname):
    if request.method=="GET":
        global cardsid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(listname=lname,userid=user1.id).first()
        list1=Cards(card_id=cardsid,card_name=lisname,card_txt=summary,card_date=date,card_status=0,listid=list.listid,userid=user1.id)
        cardsid+=1
        db.session.add(list1)
        db.session.commit()
        return jsonify(commit='True')
@app.route("/editlist/<id0>/<lisname>/<flname>",methods=["Get"])
def editlist(id0,lisname,flname):
    if request.method=="GET":
        global listsid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(userid=user1.id,listname=lisname).first()
        list.listname=flname
        listsid+=1
        db.session.add(list)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/deletelist/<id0>/<lisname>",methods=["Get"])
def deletelist(id0,lisname):
    if request.method=="GET":
        global listsid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(userid=user1.id,listname=lisname).first()
        listsid+=1
        db.session.delete(list)
        card=Cards.query.filter_by(listid=list.listid,).all()
        for i in card:
            db.session.delete(i)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/editcard/<id0>/<lisname>/<summary>/<date>/<lname>/<cname>",methods=["Get"])
def editcard(id0,lisname,summary,date,lname,cname):
    if request.method=="GET":
        global cardsid
        global usersid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(listname=lisname,userid=user1.id).first()
        card=Cards.query.filter_by(listid=list.listid,card_name=cname,userid=user1.id).first()
        card.card_name=lname
        card.card_txt=summary
        card.card_date=date
        db.session.add(card)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/deletecard/<id0>/<lisname>/<cname>",methods=["Get"])
def deletecard(id0,lisname,cname):
    if request.method=="GET":
        global cardsid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(listname=lisname,userid=user1.id).first()
        card=Cards.query.filter_by(listid=list.listid,card_name=cname,userid=user1.id).first()
        db.session.delete(card)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/stat1card/<id0>/<lisname>/<cname>",methods=["Get"])
def stat1card(id0,lisname,cname):
    if request.method=="GET":
        user1=Users.query.filter_by(username=id0).first()
        global cardsid
        list=Lists.query.filter_by(listname=lisname,userid=user1.id).first()
        card=Cards.query.filter_by(listid=list.listid,card_name=cname,userid=user1.id).first()
        card.card_status=1
        db.session.add(card)
        db.session.commit()
        return jsonify(commit='True')
@app.route("/stat0card/<id0>/<lisname>/<cname>",methods=["Get"])
def stat0card(id0,lisname,cname):
    if request.method=="GET":
        user1=Users.query.filter_by(username=id0).first()
        global cardsid
        list=Lists.query.filter_by(listname=lisname,userid=user1.id).first()
        card=Cards.query.filter_by(listid=list.listid,card_name=cname,userid=user1.id).first()
        card.card_status=0
        db.session.add(card)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/movecard/<id0>/<lisname>/<lis2name>/<cname>",methods=["Get"])
def movecard(id0,lisname,lis2name,cname):
    if request.method=="GET":
        global cardsid
        user1=Users.query.filter_by(username=id0).first()
        list=Lists.query.filter_by(listname=lisname,userid=user1.id).first()
        list2=Lists.query.filter_by(listname=lis2name,userid=user1.id).first()
        card=Cards.query.filter_by(listid=list.listid,card_name=cname,userid=user1.id).first()
        print(card)
        card.listid=list2.listid
        db.session.add(card)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/logout/<id0>",methods=["Get"])
def logout(id0):
    if request.method=="GET":
        global cardsid
        user1=Users.query.filter_by(username=id0).first()
        auth=Auth.query.filter_by(email=user1.username).first()
        auth.auth=0
        db.session.add(auth)
        db.session.commit()
        return jsonify(commit='True')

@app.route("/newuser/<email>/<pwd>/<uname>",methods=["Get"])
def newuser(email,pwd,uname):
    if request.method=="GET":
        global cardsid
        global usersid
        user1=Users(id=usersid,name=uname,email=email,password=pwd,username=uname)
        auth=Auth(email=uname,auth=1)
        usersid+=1
        db.session.add(user1)
        db.session.add(auth)
        db.session.commit()
        return jsonify(commit='True')
# @app.route("/dashboard",methods=["Get","Post"])
# def dashboard():
#     if request.method=="GET":
#         return render_template("index.html")
		
# @app.route("/dashboard",methods=["Get","Post"])
# def dashboard():
# 	if request.method=="GET":
# 		cntr=0
# 		t=[]
# 		r=[]
# 		x=y=z=0
# 		decks=Deckdouble.query.all()
# 		global usersct
# 		s=User.query.filter_by(user_id=usersct).first()

# 		for i in decks:
			
		    


# 			t.append(i.deckname)
# 			t.append(i.lastopened)
			
# 			score=Deckscore.query.filter_by(deckid=i.deckid)
# 			for j in score:
# 				if j.user_id==usersct:
# 					t.append(j.score)
# 			t.append(cntr+1)
# 			cntr=cntr+1


# 			rev=Deck_cards.query.filter_by(deckid=i.deckid).all()
# 			for j in rev:
# 				if j.difficulty=="Easy":
# 					x=x+1
# 				if j.difficulty=="Medium":
# 					y=y+1
# 				if j.difficulty=="Hard":
# 					z=z+1
# 			Max = x
# 			if y>Max:
# 				Max=y
# 			if z>Max:
# 				Max=z
# 			if Max==x:
# 				t.append("Easy")	
# 			elif Max==y:
# 				t.append("Medium")	
# 			elif Max==z:
# 				t.append("Hard")
# 			t.append(i.deckid)	
# 			n=t.copy()
# 			r.append(n)
# 			t.clear()
				

# 		return render_template("dashboard.html",decklist=r,name=s.name)
# @app.route("/home",methods=["Get","Post"])
# def home():
# 	if request.method=="GET":
# 		cntr=0
# 		t=[]
# 		r=[]
# 		x=y=z=0
# 		decks=Deckdouble.query.all()
# 		global usersct
# 		s=User.query.filter_by(user_id=usersct).first()

# 		for i in decks:
			
		    


# 			t.append(i.deckname)
# 			t.append(i.lastopened)
			
# 			score=Deckscore.query.filter_by(deckid=i.deckid)
# 			for j in score:
# 				if j.user_id==usersct:
# 					t.append(j.score)
# 			t.append(cntr+1)
# 			cntr=cntr+1
			

# 			rev=Deck_cards.query.filter_by(deckid=i.deckid).all()
# 			for j in rev:
# 				if j.difficulty=="Easy":
# 					x=x+1
# 				if j.difficulty=="Medium":
# 					y=y+1
# 				if j.difficulty=="Hard":
# 					z=z+1
# 			Max = x
# 			if y>Max:
# 				Max=y
# 			if z>Max:
# 				Max=z
# 			if Max==x:
# 				t.append("Easy")	
# 			elif Max==y:
# 				t.append("Medium")	
# 			elif Max==z:
# 				t.append("Hard")
# 			t.append(i.deckid)	
# 			n=t.copy()
# 			r.append(n)
# 			t.clear()
				

# 		return render_template("dashboard.html",decklist=r,name=s.name)
# @app.route("/deck",methods=["Get","Post"])
# def deck():
# 	if request.method=="GET":
# 		cntr=0
# 		t=[]
# 		r=[]
# 		decks=Deckdouble.query.all()

# 		for i in decks:
# 			t.append(i.deckname)
# 			t.append(i.lastopened)
			
# 			score=Deckscore.query.filter_by(deckid=i.deckid)
# 			global usersct
# 			for j in score:
# 				if j.user_id==usersct:
# 					t.append(j.score)
# 			t.append(cntr+1)
# 			cntr=cntr+1
# 			t.append(i.deckid)

# 			n=t.copy()
# 			r.append(n)
# 			t.clear()
				

# 		return render_template("deck.html",decklist=r)
# @app.route("/add_deck",methods=["Get","Post"])
# def add_deck():
# 	counter=1
# 	if request.method=="GET":
# 		return render_template("add_deck.html",counter=1)
# 	if request.method=="POST":
# 		counter=counter+1
# 		dname=request.form["deckname"]
# 		t=[]

# 		decks=Deck.query.all()
# 		for i in decks:
# 			t.append(i.deckname)
# 			n=t.copy()
# 		t.clear()
# 		if dname not in n and dname !="":
# 			new_deck=Deck(deckname=dname)

# 			db.session.add(new_deck)
# 			db.session.commit()
# 			did=new_deck.deckid
# 			users=User.query.all()
# 			for i in users:
# 				scid=Deckscore(deckid=did,score="0/0",user_id=i.user_id,name=i.name)
# 				db.session.add(scid)
# 				db.session.commit()

# 			db.session.close()
# 			global deck_id
# 			deck_id=did
# 			global deck_name
# 			deck_name=dname
# 			return redirect("/add_deck_cards")
# 		elif dname in n:
# 			return redirect("/add_deck_error")

# @app.route("/add_deck_error",methods=["Get","Post"])
# def add_deck_error():
# 	if request.method=="GET":
# 		return render_template("add_deck_error.html")
# 	if request.method=="POST":
# 		dname=request.form["deckname"]
# 		t=[]

# 		decks=Deck.query.all()
# 		for i in decks:
# 			t.append(i.deckname)
# 			n=t.copy()
# 		t.clear()
# 		if dname not in n and dname !="":
# 			new_deck=Deck(deckname=dname)

# 			db.session.add(new_deck)
# 			db.session.commit()
# 			did=new_deck.deckid

# 			db.session.close()
# 			global deck_id
# 			deck_id=did
# 			global deck_name
# 			deck_name=dname
# 			return redirect("/add_deck_cards")
# 		elif dname in n:
# 			return redirect("/add_deck_error")


# @app.route("/add_deck_cards",methods=["Get","Post"])
# def add_deck_cards():
# 	global counter
# 	global deck_name
# 	global deck_id
# 	if request.method=="GET":
# 		return render_template("add_deck_cards.html",counter=counter,deckname=deck_name)
# 	if request.method=="POST":
# 		counter=counter+1
# 		q=request.form["question"]
# 		a=request.form["answer"]
# 		o1=request.form["option1"]
# 		o2=request.form["option2"]
# 		o3=request.form["option3"]
# 		o4=request.form["option4"]
# 		if q=="" or a=="" or o1=="" or o2=="" or o3=="" or o4=="":

# 			return redirect("/add_deck_cards_error")
# 		new_card=Deck_cards(deckid=deck_id,question=q,answer=a,option1=o1,option2=o2,option3=o3,option4=o4)
# 		newdeck=Deckdouble(deckname=deck_name,deckid=deck_id)
# 		db.session.add(newdeck)
# 		db.session.add(new_card)
# 		db.session.commit()
# 		db.session.close()
# 		return render_template("add_deck_cards.html",counter=counter)
# @app.route("/add_deck_cards_error",methods=["Get","Post"])
# def add_deck_cards_error():
# 	global counter
# 	global deck_name
# 	global deck_id
# 	if request.method=="GET":
# 		return render_template("add_deck_cards_error.html",deckname=deck_name,counter=counter)
# 	if request.method=="POST":
# 		counter=counter+1
# 		q=request.form["question"]
# 		a=request.form["answer"]
# 		o1=request.form["option1"]
# 		o2=request.form["option2"]
# 		o3=request.form["option3"]
# 		o4=request.form["option4"]
# 		if q=="" or a=="" or o1=="" or o2=="" or o3=="" or o4=="":
# 			return redirect("/add_deck_cards_error")
# 		new_card=Deck_cards(deckid=deck_id,question=q,answer=a,option1=o1,option2=o2,option3=o3,option4=o4)
# 		newdeck=Deckdouble(deckname=deck_name,deckid=deck_id)
# 		db.session.add(newdeck)
# 		db.session.add(new_card)
# 		db.session.commit()
# 		db.session.close()
# 		return render_template("add_deck_cards.html",counter=counter)

# @app.route("/changedeck",methods=["Get","Post"])
# def changedeck():
# 	cntr=0
# 	t=[]
# 	r=[]
# 	decks=Deckdouble.query.all()
# 	for i in decks:
# 		t.append(i.deckname)
# 		t.append(i.lastopened)
# 		score=Deckscore.query.filter_by(deckid=i.deckid)
# 		global usersct
# 		for j in score:
# 			if j.user_id==usersct:
# 				t.append(j.score)
# 		t.append(cntr+1)
# 		cntr=cntr+1
# 		t.append(i.deckid)

# 		n=t.copy()
# 		r.append(n)
# 		t.clear()
# 	return render_template("changedeck.html",decklist=r)
# @app.route("/editdeck/<sid>",methods=["Get","Post"])
# def editdeck(sid):
# 	succ=0
# 	print(sid[-1])
# 	if sid[-1].isalpha():
# 		succ="1"
# 		id=int(sid[0])
# 	else:
# 		id=sid
# 	if request.method=="GET":
# 		deckcards=Deck_cards.query.filter_by(deckid=id).all()
# 		deck_name=Deck.query.filter_by(deckid=id).all()
# 		for i in deck_name:
# 			dname=i.deckname

# 		t=[]
# 		r=[]
# 		d=0
# 		for i in deckcards:
# 			print(1)
# 			t.append(i.question)
# 			t.append(i.answer)
# 			t.append(i.option1)
# 			t.append(i.option2)
# 			t.append(i.option3)
# 			t.append(i.option4)
# 			t.append(d+1)
# 			d=d+1
# 			n=t.copy()
# 			r.append(n)
# 			t.clear()

# 		return render_template("editdeck.html",deckname=dname,deckcards=r,succ=succ)
# 	if request.method == 'POST':
# 		if request.form['submit_button'] == "add":
# 			url=str("/editdeck_cards/"+str(id))
# 			return redirect(url)
# 		if request.form['submit_button'] == "del":
# 			a=request.form.getlist('checker')
# 			for i in a:
# 				card=Deck_cards.query.filter_by(question=i).all()
# 				for i in card:
# 					db.session.delete(i)
# 					db.session.commit()
# 					db.session.close()

# 			return redirect("/editdeck/"+str(id))
# 		if request.form['submit_button'] == "deld":
# 			dec=Deck_cards.query.filter_by(deckid=sid).all()
# 			for i in dec:
# 				db.session.delete(i)
# 				db.session.commit()
# 				db.session.close()
# 			deckdoub=Deckdouble.query.filter_by(deckid=id).first()
# 			db.session.delete(deckdoub)
# 			db.session.commit()
# 			db.session.close()

# 			return redirect("/changedeck")



# 		if request.form['submit_button'] == "chn":
# 			c=request.form.getlist('checker')
# 			deck_name=Deck.query.filter_by(deckid=id).all()
# 			for i in deck_name:
# 				dname=i.deckname
# 			c.append(dname)
# 			n=""
# 			for i in c:
# 				n=n+"|"+i
# 			print(n)
# 			global questions2

# 			n=n[1:]
# 			questions2=n
# 			print(n.split("|"))


# 			return redirect("/change_cards/"+n)
			

# @app.route("/editdeck_cards/<id>",methods=["Get","Post"])
# def addentry(id):
# 	if request.method=="GET":
# 		deck_name=Deck.query.filter_by(deckid=id).all()
# 		for i in deck_name:
# 			dname=i.deckname

# 		return render_template("editdeck_addcard.html",deckname=dname)
# 	if request.method=="POST":
# 		q=request.form["question"]
# 		a=request.form["answer"]
# 		o1=request.form["option1"]
# 		o2=request.form["option2"]
# 		o3=request.form["option3"]
# 		o4=request.form["option4"]
# 		deck_name=Deck.query.filter_by(deckid=id).all()
# 		for i in deck_name:
# 			dname=i.deckname
# 		if q=="" or a=="" or o1=="" or o2=="" or o3=="" or o4=="":
# 			return render_template("editdeck_addcard.html",deckname=dname,error="1")
# 		new_card=Deck_cards(deckid=id,question=q,answer=a,option1=o1,option2=o2,option3=o3,option4=o4)
# 		db.session.add(new_card)
# 		db.session.commit()
# 		db.session.close()
# 		return render_template("editdeck_addcard.html",deckname=dname,error="2")



# @app.route("/change_cards/<questions>",methods=["Get","Post"])
# def change_cards(questions):
# 	if request.method=="GET":
# 		global question2
# 		print(questions)
# 		n=questions2.split("|")
# 		print(n)
# 		dname=n[-1]
# 		print(dname)
# 		n=n[:len(n)-1]
# 		entries=[]
# 		d=0
# 		for i in n:
# 			deckcards=Deck_cards.query.filter_by(question=i).all()

# 			t=[]
# 			r=[]
# 			for i in deckcards:
# 				t.append(i.question)
# 				t.append(i.answer)
# 				t.append(i.option1)
# 				t.append(i.option2)
# 				t.append(i.option3)
# 				t.append(i.option4)
# 				t.append(d+1)
# 				d=d+1
# 				n=t.copy()
# 				r.append(n)
# 				t.clear()
# 			entries.append(r)

# 		return render_template("change_cards.html",deckname=dname,t=entries)
# 	if request.method=="POST":
# 		global question2
# 		n=questions2.split("|")
# 		dname=n[-1]
# 		n=n[:len(n)-1]
# 		d=0
# 		for i in n:
# 			q=request.form.get("question"+str(d+1))
# 			a=request.form["answer"+str(d+1)]
# 			o1=request.form["option1"+str(d+1)]
# 			o2=request.form["option2"+str(d+1)]
# 			o3=request.form["option3"+str(d+1)]
# 			o4=request.form["option4"+str(d+1)]
# 			d=d+1
# 			change = Deck_cards.query.filter_by(question=q).first()
# 			change.question=q
# 			change.answer=a
# 			change.option1=o1
# 			change.option2=o2
# 			change.option3=o3
# 			change.option4=o4
# 			db.session.commit()
# 		did=Deck.query.filter_by(deckname=dname).first()
# 		id=did.deckid
# 		return redirect("/editdeck/"+str(id)+str(a))

# @app.route("/deckgame/<id>",methods=["Get","Post"])
# def deckgame(id):
# 	if request.method=="GET":
# 		deck_name=Deck_cards.query.filter_by(deckid=id).all()
# 		deck_name2=Deck.query.filter_by(deckid=id).all()
# 		for i in deck_name2:
# 			dname=i.deckname

# 		card=random.choice(deck_name)
# 		global ans
# 		global cards
# 		cards=card
# 		ans=card.answer


# 		return render_template("deckgame.html",question = card.question,o1=card.option1,o2=card.option2,o3=card.option3,o4=card.option4,deckname=dname)
# 	if request.method=="POST":
# 		fcard=Deck_cards.query.filter_by(question=cards.question).first()
# 		scorecard=Deckscore.query.filter_by(deckid=id).first()

# 		deck_name2=Deck.query.filter_by(deckid=id).first()
# 		deck_name3=Deckdouble.query.filter_by(deckid=id).first()

# 		dname=deck_name2.deckname
# 		a=request.form["ans"]
# 		global usersct
# 		try:
# 			if request.form["chk"]=="check":
# 				now = datetime.now()
# 				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# 				deck_name2.lastopened=dt_string
# 				deck_name3.lastopened=dt_string
# 				db.session.commit()
# 				if a==ans:
# 					fcard.checkanswer="Correct"
# 					scmod=scorecard.score
# 					scmod2=scmod.split("/")
# 					scmod2[0]=str(1+int(scmod2[0]))
# 					scmod2[1]=str(1+int(scmod2[1]))
# 					scmod3=scmod2[0]+"/"+scmod2[1]
					
# 					scorecard=Deckscore.query.filter_by(deckid=id).all()
# 					for i in scorecard:
# 						if i.user_id==usersct:
# 							i.score=scmod3
# 							db.session.commit()


# 					return render_template("deckgame.html",succ="1",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname)
# 				else :
# 					fcard.checkanswer="Wrong"
# 					scmod=scorecard.score
# 					scmod2=scmod.split("/")
# 					scmod2[0]=str(int(scmod2[0]-1))
# 					scmod2[1]=str(1+int(scmod2[1]))
# 					scmod3=scmod2[0]+"/"+scmod2[1]
# 					scorecard=Deckscore.query.filter_by(deckid=id).all()
# 					for i in scorecard:
# 						if i.user_id==usersct:
# 							i.score=scmod3
# 						db.session.commit()
# 					return render_template("deckgame.html",succ="2",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname)
# 			elif request.form["chk"]=="next":
# 				now = datetime.now()
# 				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# 				deck_name2.lastopened=dt_string
# 				db.session.commit()
# 				return redirect("/deckgame/"+str(id))
# 		except:
# 			if request.form["hard"]=="easy":
# 				fcard.difficulty="Easy"
# 				db.session.commit()
# 				return render_template("deckgame.html",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname,th="1")
# 			elif request.form["hard"]=="medium":
# 				thanks="Thank you for your feedback."
# 				fcard.difficulty="Medium"
# 				db.session.commit()
# 				return render_template("deckgame.html",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname,th="1")
# 			elif request.form["hard"]=="hard":
# 				thanks="Thank you for your feedback."
# 				fcard.difficulty="Hard"
# 				db.session.commit()
# 				return render_template("deckgame.html",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname,th="1")
# 			elif request.form["hard"]=="vhard":
# 				thanks="Thank you for your feedback."
# 				fcard.difficulty="Very Hard"
# 				db.session.commit()
# 				return render_template("deckgame.html",question=("The answer is "+cards.answer),o1=cards.option1,o2=cards.option2,o3=cards.option3,o4=cards.option4,deckname=dname,th="1")

# @app.route("/viewscore",methods=["Get","Post"])
# def viewscore():
# 	if request.method=="GET":
# 		cntr=0
# 		t=[]
# 		r=[]
# 		users=User.query.all()
# 		for k in users:
# 			decks=Deckdouble.query.all()
# 			for i in decks:
# 				t.append(i.deckname)
# 				score=Deckscore.query.filter_by(deckid=i.deckid)
# 				usersct=k.user_id
# 				for j in score:
# 					if j.user_id==usersct:
# 						t.append(j.score)
# 				t.append(cntr+1)
# 				cntr=cntr+1
# 				t.append(k.name)
# 				n=t.copy()
# 				r.append(n)
# 				t.clear()
# 	return render_template("viewscore.html",decklist=r)
# @app.route("/logout",methods=["Get","Post"])
# def logout():
# 	return redirect("/")
# @app.route("/newuser",methods=["Get","Post"])
# def newuser():
# 	if request.method=="GET":
# 		return render_template("newuser.html")
# 	elif request.method=="POST":
# 		nameofp=request.form["name"]
# 		emailofp=request.form["email"]
# 		passwordofp=request.form["password"]
# 		try :
# 			newuser=User(name=nameofp,email=emailofp,password=passwordofp)
# 			db.session.add(newuser)
# 			db.session.commit()
# 			deck_cards=Deck.query.all()
# 			user_cards=User.query.all()
# 			maxm=0
# 			for i in user_cards:
# 				if maxm<=i.user_id:
# 					maxm=maxm+1
# 			print(deck_cards)
# 			for i in deck_cards:
# 				scid=Deckscore(deckid=i.deckid,score="0/0",user_id=maxm,name=nameofp)
# 				db.session.add(scid)
# 				db.session.commit()
# 		except:
# 			db.session.rollback()
# 		db.session.close()
# 		return redirect("/")
if __name__=="__main__":
	app.run(
		host='0.0.0.0',
		debug=True,
		port=8080)
