from manage import db

class Import(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='import', lazy=True)

    def __repr__(self):
        return '<Import %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, nullable=False)
    import_id = db.Column(db.Integer, db.ForeignKey('import.id'), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    apartment = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False) #dd.mm.gggg
    gender = db.Column(db.String(6), nullable=False) #male or female
    relatives = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.citizen_id
