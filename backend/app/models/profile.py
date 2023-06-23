from app.extensions import db

class Profiles(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.Text)
    profile_image_url = db.Column(db.String(255))
    website = db.Column(db.String(255))
    location = db.Column(db.String(255))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('Users', back_populates = 'profiles')

    def serialize(self): 
        return {
            "profile_id": self.profile_id,
            "biography": self.biography,
            "profile_image_url":self.profile_image_url,
            "website":self.website,
            "location":self.location,
            "user_id":self.user_id
        }