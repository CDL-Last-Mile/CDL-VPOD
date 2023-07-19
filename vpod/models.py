from vpod import db

class Orders(db.Model):
    __tablename__ = "xView_Orders"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    ClientID = db.Column(db.Integer)
    ClientRefNo = db.Column(db.String(50))
    PODname = db.Column(db.String(50))
    PickupTargetFrom = db.Column(db.DateTime)
    PODcompletion = db.Column(db.DateTime)

class OrderDocuments(db.Model):
    __tablename__ = "xView_OrderDocuments"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    DocumentID = db.Column(db.Integer)

class Documents(db.Model):
    __tablename__ = "Documents"
    DocumentID = db.Column(db.BigInteger, primary_key=True)
    DocumentBinary = db.Column(db.LargeBinary)
    FileFormat = db.Column(db.String(4))
    IsVisibleOnline = db.Column(db.Integer)


class ClientMaster(db.Model):
    __tablename__ = "ClientMaster"
    ClientID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(75))
