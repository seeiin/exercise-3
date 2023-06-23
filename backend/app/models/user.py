from app.extensions import db

# table database user
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(512), nullable=False)

    # one to one dengan table profile
    profiles = db.relationship('Profiles', uselist=False, back_populates='user')

    # one to many dengan table contents
    contents = db.relationship('Contents', back_populates='user')

    # fungsi serialize untuk mengembalikan data dictionary
    def serialize(self): 
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email":self.email,
            "password":self.password
        }