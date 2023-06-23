from app.extensions import db

class Contents(db.Model):
    content_id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('Users', back_populates = 'contents')

    def serialize(self): 
        return {
            "content_id": self.content_id,
            "caption": self.caption,
            "image_url":self.image_url,
            "created_at":self.created_at
        }