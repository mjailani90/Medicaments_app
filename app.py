import re
from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import *
from sqlalchemy import text
from sqlalchemy.orm import backref
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = '123456'

db = SQLAlchemy(app)

class company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CompanyName = db.Column(db.String())
    CompanyLogo = db.Column(db.String())
    Items = db.relationship('Item',backref='owner')

    def __init__(self,CompanyName,CompanyLogo) -> None:
        self.CompanyName = CompanyName
        self.CompanyLogo = CompanyLogo
        
 
    def __repr__(self):
        return f"company('{self.id}','{self.CompanyName}','{self.CompanyLogo}')"

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
    CompanyID = db.Column(db.Integer,db.ForeignKey('company.id'))

    def __init__(self,ItemName,ItemPhoto,ItemDesc,ItemIngredient,ItemUse,ItemDose,ItemPrice,ItemCompetitor,CompanyID) -> None:
        self.ItemName = ItemName
        self.ItemPhoto = ItemPhoto
        self.ItemDesc = ItemDesc
        self.ItemIngredient = ItemIngredient
        self.ItemUse = ItemUse
        self.ItemDose = ItemDose
        self.ItemPrice = ItemPrice
        self.ItemCompetitor = ItemCompetitor
        self.CompanyID = CompanyID
        
    def __repr__(self):
        return f"company('{self.id}','{self.ItemName}','{self.ItemPhoto}','{self.ItemDesc}','{self.ItemIngredient}','{self.ItemUse}','{self.ItemDose}','{self.ItemPrice}','{self.ItemCompetitor}','{self.CompanyID}')"

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password
        
 
    def __repr__(self):
        return f"company('{self.id}','{self.username}','{self.password}')"


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_first_request
def create_table():
    db.create_all()


@app.route('/',methods=['GET','POST'])
def main():
    if request.method=='GET':
        sql = text('SELECT * FROM  company ORDER BY random() LIMIT 6;')
        companies = db.engine.execute(sql)
        return render_template("home.html",companies = companies)
    else:
        txtSearch = request.form.get('txtSearch')
        if txtSearch=='admin':
            return redirect("/admin/", code=302)
        else:
            return render_template('edititem.html')


@app.route('/item/')
def item():
    pass


@app.route('/company/')
def allcompany():
    args = request.args
    if 'id' in args:
        return 'one company'
    else:
        data = company.query.all()
        return render_template("companies.html",data=data)


@app.route('/admin/')
def admin():
    args = request.args
    if 'company' in args:
        comp = db.session.query(company).filter_by(id=args['company']).first()
        return render_template('editCompany.html',comp= comp)
    elif 'item' in args:
        ItemInfo = db.session.query(Item).filter_by(id=args['item']).first()
        print(ItemInfo)
        companies = company.query.all()
        return render_template('edititem.html',ItemInfo= ItemInfo,companies=companies)
    else:
        comps = company.query.all()
        item = Item.query.all()
        return render_template('admin.html',compaies=comps,Items=item)


@app.route('/admin/company', methods=['POST'])
def addCompany():
    frm = request.form
    photofilename=''
    if 'companyphoto' not in request.files:
        companyphoto = ''
    else:
        file = request.files['companyphoto']
    
    if file and allowed_file(file.filename):
        photofilename = secure_filename(file.filename)
        file.save(os.path.join('static/companies/', photofilename))
    
    if frm['CompanyID']:
        if photofilename=='':
            db.session.query(company).filter_by(id=frm['CompanyID']).update({company.CompanyName:frm['Companynametxt']})
        else:
            db.session.query(company).filter_by(id=frm['CompanyID']).update({company.CompanyName:frm['Companynametxt'],company.CompanyLogo:photofilename})
        db.session.commit()
    else:
        comp = company(frm['Companynametxt'],photofilename)
        db.session.add(comp)
        db.session.commit()

    return redirect(url_for("admin"))


@app.route('/admin/item', methods=['POST'])
def addItem():
    frm = request.form
    photofilename=''
    if 'ItemPhoto' not in request.files:
        Itemphoto = ''
    else:
        file = request.files['ItemPhoto']
    
    if file and allowed_file(file.filename):
        photofilename = secure_filename(file.filename)
        file.save(os.path.join('static/Items/', photofilename))
    
    if frm['ItemID']:
        if photofilename=='':
            db.session.query(Item).filter_by(id=frm['ItemID']).update({Item.ItemName:frm['itemName'],
            Item.ItemDesc:frm['itemDescription'],Item.ItemIngredient:frm['itemIngredient'],
            Item.ItemUse:frm['itemUse'],Item.ItemDose:frm['itemDose'],Item.ItemPrice:frm['itemPrice'],
            Item.ItemCompetitor:frm['itemCompetitor'],Item.CompanyID:frm['CompanyName']})
        else:
            db.session.query(Item).filter_by(id=frm['ItemID']).update({Item.ItemName:frm['itemName'],
            Item.ItemPhoto:photofilename,Item.ItemDesc:frm['itemDescription'],Item.ItemIngredient:frm['itemIngredient'],
            Item.ItemUse:frm['itemUse'],Item.ItemDose:frm['itemDose'],Item.ItemPrice:frm['itemPrice'],
            Item.ItemCompetitor:frm['itemCompetitor'],Item.CompanyID:frm['CompanyName']})
        db.session.commit()
    else:
        comp = Item(frm['itemName'],photofilename,frm['itemDescription'],frm['itemIngredient'],frm['itemUse'],frm['itemDose'],
        frm['itemPrice'],frm['itemCompetitor'],frm['CompanyName'])
        db.session.add(comp)
        db.session.commit()

    return redirect(url_for("admin"))



@app.route('/login/')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run()