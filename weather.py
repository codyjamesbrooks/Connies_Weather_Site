from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crags.db'
db = SQLAlchemy(app)


# DB Class Model 
class ClimbingArea(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))

    def __str__(self):
        return self.name


# Home page Route. 
@app.route('/', methods=['GET', 'POST'])
def index(): 
    crags = ClimbingArea.query.all()
    return render_template('home.html', crags=crags)


@app.route('/addarea/', methods=['GET', 'POST'])
def add_crag():
    if request.method == 'POST':
        # Add new climbing area. 
        pass
    else: 
        # Display Form for adding a new crag
        return render_template('addarea.html')



# Call the app
if __name__ == "__main__":
    app.run(debug=True)


