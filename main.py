from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, MultipleFileField, FileField
from wtforms.validators import DataRequired, URL
from datetime import date
import os
from werkzeug.utils import secure_filename
from textwrap import wrap



#---------------------- YEAR FOR COPYRIGHT ---------------------- #
year = datetime.datetime.now().strftime('%Y')


#---------------------- FLASK ----------------------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)

#---------------------- CONNECT TO DB ----------------------#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#---------------------- CONFIGURE DB TABLE ----------------------#
class Cafes(db.Model):
    __tablename__ = "cafes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(500), unique=True, nullable=False)
    address = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)
    website = db.Column(db.String(250), unique=True)
    wifi_down = db.Column(db.String(250))
    seating_range = db.Column(db.String(20), nullable=False)
    coffee_price = db.Column(db.String(20), nullable=False)
    mon_open = db.Column(db.String(20))
    mon_close = db.Column(db.String(20))
    tue_open = db.Column(db.String(20))
    tue_close = db.Column(db.String(20))
    wed_open = db.Column(db.String(20))
    wed_close = db.Column(db.String(20))
    thu_open = db.Column(db.String(20))
    thu_close = db.Column(db.String(20))
    fri_open = db.Column(db.String(20))
    fri_close = db.Column(db.String(20))
    sat_open = db.Column(db.String(20))
    sat_close = db.Column(db.String(20))
    sun_open = db.Column(db.String(20))
    sun_close = db.Column(db.String(20))
    wifi_rating = db.Column(db.String(20), nullable=False)
    power_rating = db.Column(db.String(20), nullable=False)
    seating_rating = db.Column(db.String(20), nullable=False)
    coffee_rating = db.Column(db.String(20), nullable=False)
    review_date = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    image_paths = db.Column(db.String(1000), nullable=False)
    logo_image_path = db.Column(db.String(500), nullable=False)
    facebook = db.Column(db.String(500))
    instagram = db.Column(db.String(500))
    twitter = db.Column(db.String(500))
    open_status = db.Column(db.String(25))
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

##---------------------- RANDOM CAFES ---------------------- ##
# with app.app_context():
#     num_cafes = len(db.session.query(Cafes).all())
#
#     random_nums = random.sample(range(1, num_cafes + 1), 3)
#
#     random_1 = Cafes.query.get(random_nums[0])
#     random_2 = Cafes.query.get(random_nums[1])
#     random_3 = Cafes.query.get(random_nums[2])

#---------------------- ADD CAFE ----------------------#
class AddNewCafeForm(FlaskForm):
    name = StringField("New Cafe Name", validators=[DataRequired()])
    location = StringField("Cafe location on Google Maps (URL)", validators=[DataRequired()])
    address = StringField("Street Address", validators=[DataRequired()])
    description = StringField("Short Description", validators=[DataRequired()])
    website = StringField("Website (URL)")
    facebook = StringField("Facebook (URL)")
    instagram = StringField("Instagram (URL)")
    twitter = StringField("Twitter (URL)")
    wifi_down = StringField("WiFi Download speed")
    seating_range = SelectField(u"Seating Range", choices=[("0 - 5"), ("6 - 10"), ("11 - 15"), ("16 - 20"), ("20 +")], validators=[DataRequired()])
    coffee_price = StringField("Medium white coffee", validators=[DataRequired()])
    mon_open = StringField("Cafe Monday open time")
    mon_close = StringField("Cafe Monday close time")
    tue_open = StringField("Cafe Tuesday open time")
    tue_close = StringField("Cafe Tuesday close time")
    wed_open = StringField("Cafe Wednesday open time")
    wed_close = StringField("Cafe Wednesday close time")
    thu_open = StringField("Cafe Thursday open time")
    thu_close = StringField("Cafe Thursday close time")
    fri_open = StringField("Cafe Friday open time")
    fri_close = StringField("Cafe Friday close time")
    sat_open = StringField("Cafe Saturday open time")
    sat_close = StringField("Cafe Saturday close time")
    sun_open = StringField("Cafe Sunday open time")
    sun_close = StringField("Cafe Sunday close time")
    wifi_rating = SelectField(u'WiFi Strength Rating', choices=["✘", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], validators=[DataRequired()])
    power_rating = SelectField(u'Power Socket Availability', choices=["✘", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], validators=[DataRequired()])
    seating_rating = SelectField(u'Seating Comfort', choices=["✘", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', choices=["✘", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], validators=[DataRequired()])
    comments = StringField("Comments")
    logo_image = FileField("Cafe logo", validators=[DataRequired()])
    images = MultipleFileField("Cafe Image", validators=[DataRequired()])
    submit = SubmitField("Submit")


#---------------------- IS IT OPEN? ----------------------#
def time_value(time):
    split = time.split(":")
    if len(split) == 2:
        hour = split[0]
        min = split[1]
        time_value = int((int(hour) * 60) + int(min))
        return time_value
    elif len(split) != 2:
        split = time.split(":")
        new_split = split[1].split("-")
        hour_1 = split[0]
        hour_2 = new_split[1]
        min_1 = new_split[0]
        min_2 = split[2]
        value_1 = int((int(hour_1) * 60) + int(min_1))
        value_2 = int((int(hour_2) * 60) + int(min_2))
        return [value_1, value_2]


def is_it_open(open_time, close_time, current_time):
    if not open_time:
        return "Closed"
    elif not close_time:
        return "Closed"
    elif len(open_time) == 5:
        if time_value(close_time) < 120:
            if time_value(current_time) > time_value(open_time) and time_value(current_time) < (time_value(close_time) + 1440):
                return "Open"
            else:
                return "Closed"
        else:
            if time_value(current_time) > time_value(open_time) and time_value(current_time) < (time_value(close_time)):
                return "Open"
            else:
                return "Closed"
    else:
        am_hours = time_value(open_time)
        if time_value(current_time) > am_hours[0] and time_value(current_time) < am_hours[1]:
            return "Open"
        pm_hours = time_value(close_time)
        if time_value(current_time) > pm_hours[0] and time_value(current_time) < pm_hours[1]:
            return "Open"
        else:
            return "Closed"

@app.route("/")
def index():
    cafes = Cafes.query.all()
    cafe_1 = Cafes.query.get(1)
    return render_template("index.html",
                           year=year,
                           cafe_1=cafe_1,
                           cafes=cafes
                           )

@app.route("/cafes/<int:cafe>", methods=["POST", "GET"])
def cafes(cafe):
    requested_cafe = Cafes.query.get(cafe)
    cafe_name = requested_cafe.name
    photos = requested_cafe.image_paths
    sep_photos = photos.split(",")

    return render_template("cafe_template.html",
                           cafe=requested_cafe,
                           photos=sep_photos,
                           cafe_name=cafe_name,
                           year=year
                           )

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = AddNewCafeForm()
    today = f"{date.today().strftime('%d')} of {date.today().strftime('%B')}, {date.today().strftime('%Y')}"
    if form.validate_on_submit():
        # Check if the folder exists, if not create it
        if not os.path.exists(f"static/images/cafes/{form.name.data}"):
            os.makedirs(f"static/images/cafes/{form.name.data}")
        #Save cafe images
        files_filenames = []
        for file in request.files.getlist("images"):
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(f"static/images/cafes/{form.name.data}", file_filename))
            files_filenames.append(file_filename)
        #Save cafe logo image
        logo = form.logo_image.data
        logo_filename = secure_filename(logo.filename)
        logo.save(os.path.join(f"static/images/cafes/{form.name.data}", logo_filename))
        logo_path = str(logo_filename)
        #Convert map link
        full_map_link = form.location.data
        map_link = full_map_link.split('"', 3)[1]

        new_cafe = Cafes(
            name=form.name.data,
            location=map_link,
            address=form.address.data,
            description=form.description.data,
            website=form.website.data,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            twitter=form.twitter.data,
            wifi_down=form.wifi_down.data,
            seating_range=form.seating_range.data,
            coffee_price=form.coffee_price.data,
            mon_open=form.mon_open.data,
            mon_close=form.mon_close.data,
            tue_open=form.tue_open.data,
            tue_close=form.tue_close.data,
            wed_open=form.wed_open.data,
            wed_close=form.wed_close.data,
            thu_open=form.thu_open.data,
            thu_close=form.thu_close.data,
            fri_open=form.fri_open.data,
            fri_close=form.fri_close.data,
            sat_open=form.sat_open.data,
            sat_close=form.sat_close.data,
            sun_open=form.sun_open.data,
            sun_close=form.sun_close.data,
            wifi_rating=form.wifi_rating.data,
            power_rating=form.power_rating.data,
            seating_rating=form.seating_rating.data,
            coffee_rating=form.coffee_rating.data,
            review_date=today,
            comments=form.comments.data,
            image_paths=','.join(files_filenames),
            logo_image_path=logo_path,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("index"))


    return render_template("add_cafe.html", form=form, year=year)

@app.route("/all_cafes", methods=["GET", "POST"])
def all_cafes():
    cafes = Cafes.query.all()
    now = datetime.datetime.now()
    day_today = now.strftime("%A")
    time_now = now.strftime("%H:%M")
    day = wrap(day_today.lower(), 3)[0]
    for cafe in cafes:
        open_hour = getattr(cafe, f"{day}_open")
        close_hour = getattr(cafe, f"{day}_close")
        cafe.open_status = is_it_open(open_hour, close_hour, time_now)

    return render_template("all_cafes.html",
                           cafes=cafes,
                           year=year
                           )



if __name__ == "__main__":
    app.run(debug=True)
