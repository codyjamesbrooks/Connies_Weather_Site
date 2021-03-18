from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)

# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crags.db'
db = SQLAlchemy(app)

# Google Maps API Key
path = "..\API Keys\ConniesAPIkey.txt"
with open(path, 'r') as f:
    maps_APIkey = f.read()


# Class to model the Climbing area table.
# Areas will be instantiated using a dict
# All areas are required to have a name, a longitude coordinate, and a latitude coordinate.


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

    def update(self, update_area_dict):
        for key, value in update_area_dict.items():
            setattr(self, key, value)


# Home page Route.
# Displays links for all crags in the ClimbingAreas table.
@app.route('/', methods=['GET', 'POST'])
def index():
    crags = ClimbingArea.query.all()
    return render_template('home.html', crags=crags)

# Redirects to a addarea page that allows user to enter in a new crag into the Climbing Area DB.


@app.route('/addarea/', methods=['GET', 'POST'])
def add_crag():
    # Google Map instance for plotting exact crag coordinates.
    mymap = Map(
        identifier="view-side",
        lat=31.9171,
        lng=-106.0391,
    )
    if request.method == 'POST':
        # Pull form data into a dict
        area_dict = {
            'name': request.form['name'],
            'city': request.form['city'],
            'state': request.form['state'],
            'longitude': request.form['longitude'],
            'latitude': request.form['latitude']
        }

        # use dict to create a ClimbingArea instance.
        add_area = ClimbingArea(area_dict)
        try:
            # Write instance to crags db
            db.session.add(add_area)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the area"
    else:
        # Display Form for adding a new crag
        return render_template('addarea.html', mymap=mymap)

# Redirects to a crags app page.


@app.route('/crag/<int:id>', methods=['GET', 'POST'])
def view_crag(id):
    crag = ClimbingArea.query.get_or_404(id)
    if request.method == 'POST':
        # Possibly will be used to update a crag.
        # Algthough I may use this function just for the view
        # And then will transation that work to a different route.
        pass
    else:
        return render_template('cragforecast.html', crag=crag)


@app.route('/updatecrag/<int:id>', methods=['GET', 'POST'])
def update_crag(id):
    crag = ClimbingArea.query.get_or_404(id)
    if request.method == 'POST':
        # Pull update from form
        area_dict = {
            'name': request.form['name'],
            'city': request.form['city'],
            'state': request.form['state'],
            'longitude': request.form['longitude'],
            'latitude': request.form['latitude']
        }
        # Update crag using update method
        crag.update(area_dict)
        try:
            db.session.commit()
            return redirect(f'/crag/{crag.id}')
        except:
            return "There was an issue updating the crag...."
    else:
        return render_template('updatecrag.html', crag=crag)


@app.route('/map/')
def map_func():
    return render_template('map.html', APIkey=maps_APIkey)


# Call the app
if __name__ == "__main__":
    app.run(debug=True)
