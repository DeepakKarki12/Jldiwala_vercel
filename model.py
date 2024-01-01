from extension import db 

class YourModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50))
    column_1 = db.Column(db.String)  # Adjust the column datatype as needed
    column_2 = db.Column(db.String)
    # x_axis = db.Column(db.String)
    # y_axis = db.Column(db.String)
