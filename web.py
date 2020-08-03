from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    
db.create_all()

import pandas as pd

df = pd.read_csv('grocery.csv')

for index,row in df.iterrows():
     item = Product(name=row['Name'], price=row['Price'], category=row['Category'])
     db.session.add(item)
db.session.commit()

@app.route("/")
def index():
    chicken = Product.query.filter(Product.category=='Chicken').all()
    pork = Product.query.filter(Product.category=='Pork').all()
    fish = Product.query.filter(Product.category=='Fish').all()
    menus = [chicken, pork, fish]
    return render_template('home.html', data=menus)

app.run(host='0.0.0.0')