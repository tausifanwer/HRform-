from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import json



with open('config.json','r') as c:
    params=json.load(c)["params"]
local_server=True
app=Flask(__name__)


if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_url']
db = SQLAlchemy(app)

class EMP(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20),unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    # date = db.Column(db.String(12),nullable=True)
    
    
@app.route("/",methods=['GET','POST'])
def home():
    if (request.method=='POST'):
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        age=request.form.get('age')
        
        entry=EMP(firstname=firstname,lastname=lastname,email=email,age=age)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    item=EMP.query.all()
    return render_template('index.html',item=item,params=params)

app.run(debug=True)