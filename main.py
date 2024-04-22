from flask import request, render_template, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired

app = Flask(__name__)
username = 'root'
password = 'password123'
server   = 'localhost'
dbname   = '/homework'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + username + ':' + password + '@' + server + dbname 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning
app.config['SECRET_KEY'] = "supersecretkey" #required for wtforms
db = SQLAlchemy(app)

class Supplier(db.Model):
    __tablename__ = 'supplier'
    Sno = db.Column(db.String(255), primary_key = True, unique=True, nullable=False)
    Sname = db.Column(db.String(255), nullable=False)
    Status =db.Column(db.Integer)
    City = db.Column(db.String(255))

    def get_id(self):
        return self.Sno
    
    def __init__(self, sno, sname, status="", city=""):
        self.Sno = sno
        self.Sname = sname
        self.Status = status
        self.City = city

class Part(db.Model):
    __tablename__ = "Part"
    Pno = db.Column(db.String(255), primary_key = True, unique=True, nullable=False)
    Pname = db.Column(db.String(255), nullable=False)
    Color = db.Column(db.String(255))
    Weight = db.Column(db.Integer)
    City = db.Column(db.String(255))

    def get_id(self):
        return self.Pno
    
    def __init__(self, pno, pname, color="", weight="", city=""):
        self.Pno = pno
        self.Pname = pname
        self.Color = color
        self.Weight = weight
        self.city = city

class Shipment(db.Model):
    Sno = db.Column(db.String(255), db.ForeignKey("supplier.Sno"), nullable=False, primary_key=True)
    Pno = db.Column(db.String(255), db.ForeignKey("Part.Pno"), nullable=False, primary_key=True)
    Qty = db.Column(db.Integer, default=100)
    Price = db.Column(db.Float((10,3), asdecimal=True))

    def __init__(self, sno, pno, qty = 100, price = 0.0):
        self.Sno = sno
        self.Pno = pno
        self.Qty = qty
        self.Price = price

class CreateShipmentForm(FlaskForm):
    sno = StringField("Shipment Number", validators=[DataRequired()])
    pno = StringField("Part Number", validators=[DataRequired()])
    qty = IntegerField("Quantity")
    price = DecimalField("Price", places=3)
    submit = SubmitField("Submit")

class PartLookupForm(FlaskForm):
    part_no = sno = StringField("Part Number", validators=[DataRequired()])
    submit = SubmitField("Submit")



@app.route("/",  methods=['GET', 'POST'])
def index():
    message = ""
    form = CreateShipmentForm()
    if form.validate_on_submit():
        shipment = Shipment(form.sno.data, form.pno.data, form.qty.data, form.price.data)
        try:
            db.session.add(shipment)
            db.session.commit()
            message = "Successfully added to database"
        except:
            message = "Failed to add to databse"

    return render_template('index.html', form = form, message = message)

@app.route("/updateSupplierStatus", methods=['GET', 'POST'])
def updateSupplierStatus():
    if request.method == 'POST':
        updateAmount  = request.form["statusChange"]
        Supplier.query.update({Supplier.Status: Supplier.Status * updateAmount})
        db.session.commit()
    suppliers = Supplier.query.all()
    return render_template("updateSupplierStatus.html", suppliers = suppliers)

@app.route("/partLookup.html", methods=['GET', 'POST'])
def partLookup():
    form = PartLookupForm()
    suppliers = []
    if request.method == 'POST':
        Shipment.query.filter_by(Pno = form.part_no.data)
        for sh, su in db.session.query(Shipment, Supplier).\
                                filter(Shipment.Sno == Supplier.Sno).\
                                filter(Shipment.Pno == form.part_no.data).\
                                distinct():
            suppliers.append(su)
        
    return render_template("partlookup.html", form = form, suppliers = suppliers)

