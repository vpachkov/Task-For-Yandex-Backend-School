from database import db

class Import(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='import_group', lazy='dynamic')

    def __repr__(self):
        return '<Import %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, nullable=False)
    import_id = db.Column(db.Integer, db.ForeignKey('import.id'), nullable=False)
    town = db.Column(db.String(256), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    building = db.Column(db.String(256), nullable=False)
    apartment = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False) #dd.mm.gggg
    gender = db.Column(db.String(6), nullable=False) #male or female
    relatives = db.Column(db.String())

    def __init__(self, citizen_id, town, street, building, apartment, name, birth_date, gender, relatives):
        self.citizen_id = citizen_id
        self.town = town
        self.street = street
        self.building = building
        self.apartment = apartment
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.relatives = relatives

    def __repr__(self):
        return '<User %r>' % self.citizen_id
