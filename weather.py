from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

weather = Flask(__name__)

# Configure DB
weather.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crags.db'
db = SQLAlchemy(weather)

# Google Maps API Key
path = "..\API Keys\ConniesAPIkey.txt"
with open(path, 'r') as f: 
    maps_APIkey = f.read()


# DB Class Model 
class ClimbingArea(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))

    def __init__(self, area_dict):
        self.name = area_dict['name']
        self.city = area_dict['city']
        self.state = area_dict['state']
        self.longitude = area_dict['longitude']
        self.latitude = area_dict['latitude']

    def __str__(self):
        return self.name


# Home page Route. 
@weather.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@weather.route('/addarea/', methods=['GET', 'POST'])
def add_crag():
    if request.method == 'POST':
        area_dict = {   
                    'name' : request.form['name'],
                    'city' : request.form['city'],
                    'state' : request.form['state'],
                    'longitude' : request.form['longitude'],
                    'latitude' : request.form['latitude']
        }
        add_area = ClimbingArea(area_dict)
        try: 
            db.session.add(add_area)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the area"
    else: 
        # Display Form for adding a new crag
        return render_template('addarea.html')



# Call the app
if __name__ == "__main__":
    weather.run(debug=True)


