from operator import imod
from flask import Flask, render_template
from flask_sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = '123456'

db = SQLAlchemy(app)

class company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CompanyName = db.Column(db.String())

    def __init__(self,CompanyName) -> None:
        self.CompanyName = CompanyName
        
 
    def __repr__(self):
        return f"company('{self.id}','{self.CompanyName}')"

class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ItemName = db.Column(db.String())
    ItemPhoto = db.Column(db.String(),nullable=True)
    ItemDesc = db.Column(db.String(),nullable=True)
    ItemIngredient = db.Column(db.String(),nullable=True)
    ItemUse = db.Column(db.String(),nullable=True)
    ItemDose = db.Column(db.String(),nullable=True)
    ItemPrice = db.Column(db.Float(),nullable=True)
    ItemCompetitor = db.Column(db.String(),nullable=True)
    Company = relationship("company", back_populates="Item")

    def __init__(self,ItemName,ItemPhoto,ItemDesc,ItemIngredient,ItemUse,ItemDose,ItemPrice,ItemCompetitor,Company) -> None:
        self.ItemName = ItemName
        self.ItemPhoto = ItemPhoto
        self.ItemDesc = ItemDesc
        self.ItemIngredient = ItemIngredient
        self.ItemUse = ItemUse
        self.ItemDose = ItemDose
        self.ItemPrice = ItemPrice
        self.ItemCompetitor = ItemCompetitor
        self.Company = Company
        
 
    def __repr__(self):
        return f"company('{self.id}','{self.ItemName}','{self.ItemPhoto}','{self.ItemDesc}','{self.ItemIngredient}','{self.ItemUse}','{self.ItemDose}','{self.ItemPrice}','{self.ItemCompetitor}','{self.Company}')"

@app.before_first_request
def create_table():
    db.create_all()


@app.route('/',methods=['GET','POST'])
def main():
    # cons = database.dbconnection.query.all()
    # print(cons[0].connectionString)
    # for con in cons:
        # con.connectionString = database.decreypttxt(con.connectionString)
    return render_template("home.html")
    # return render_template("ConnectionGrid.html",conlist=cons)

# db.init_app(app)

@app.route('/item/')
def item():
    pass


@app.route('/company/')
def allcompany():
    pass


@app.route('/admin/')
def admin():
    pass




if __name__ == "__main__":
    app.run(debug=True)

# app.run(port=8080, host="0.0.0.0", debug=True)

# app.run() 