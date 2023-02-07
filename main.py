from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, URL
from datetime import date
import os
from werkzeug.utils import secure_filename


#---------------------- YEAR FOR COPYRIGHT ---------------------- #
year = datetime.datetime.now().strftime('%Y')

#---------------------- FLASK ----------------------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)

#---------------------- CONNECT TO DB ----------------------#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#---------------------- CONFIGURE DB TABLE ----------------------#
class Cafes(db.Model):
    __tablename__ = "cafes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), unique=True, nullable=False)
    website = db.Column(db.String(250), unique=True)
    wifi_up = db.Column(db.String(250))
    wifi_down = db.Column(db.String(250))
    seating_range = db.Column(db.String(20), nullable=False)
    coffee_price = db.Column(db.String(20), nullable=False)
    opens_wd = db.Column(db.String(20), nullable=False)
    closes_wd = db.Column(db.String(20), nullable=False)
    opens_we = db.Column(db.String(20), nullable=False)
    closes_we = db.Column(db.String(20), nullable=False)
    wifi_rating = db.Column(db.String(20), nullable=False)
    power_rating = db.Column(db.String(20), nullable=False)
    seating_rating = db.Column(db.String(20), nullable=False)
    coffee_rating = db.Column(db.String(20), nullable=False)
    review_date = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    image_paths = db.Column(db.String(1000), nullable=False)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
   db.create_all()

#---------------------- ADD CAFE ----------------------#
class AddNewCafeForm(FlaskForm):
    name = StringField("New Cafe Name", validators=[DataRequired()])
    location = StringField("Cafe location on Google Maps (URL)", validators=[DataRequired(), URL(require_tld=True, message="Is that a link?")])
    website = StringField("Website (URL)", validators=[URL(require_tld=True, message="Is that a link?")])
    wifi_up = StringField("WiFi Upload speed", validators=[DataRequired()])
    wifi_down = StringField("WiFi Download speed", validators=[DataRequired()])
    seating_range = SelectField(u"Seating Range", choices=[("0 - 5"), ("6 - 10"), ("11 - 15"), ("16 - 20"), ("20 +")], validators=[DataRequired()])
    coffee_price = StringField("Medium white coffee", validators=[DataRequired()])
    opens_wd = StringField("Cafe weekday open time", validators=[DataRequired()])
    closes_wd = StringField("Cafe weekday close time", validators=[DataRequired()])
    opens_we = StringField("Cafe weekend open time", validators=[DataRequired()])
    closes_we = StringField("Cafe weekend close time", validators=[DataRequired()])
    wifi_rating = SelectField(u'WiFi Strength Rating', choices=[("✘"), ("💪"), ("💪💪"), ("💪💪💪"), ("💪💪💪💪"), ("💪💪💪💪💪")], validators=[DataRequired()])
    power_rating = SelectField(u'Power Socket Availability', choices=[("✘"), ("🔌"), ("🔌🔌"), ("🔌🔌🔌"), ("🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌")], validators=[DataRequired()])
    seating_rating = SelectField(u'Seating Comfort', choices=[("✘"), ("💺"), ("💺💺"), ("💺💺💺"), ("💺💺💺💺"), ("💺💺💺💺💺")], validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', choices=[("✘"), ("☕"), ("☕☕"), ("☕☕☕"), ("☕☕☕☕"), ("☕☕☕☕☕")], validators=[DataRequired()])
    comments = StringField("Comments")
    images = MultipleFileField("Cafe Image", validators=[DataRequired()])
    submit = SubmitField("Submit")




@app.route("/")
def index():
    return render_template("index.html", year=year)

@app.route("/cafes/<int:cafe>", methods=["POST", "GET"])
def cafes(cafe):
    requested_cafe = Cafes.query.get(cafe)
    cafe_name = requested_cafe.name
    photos = requested_cafe.image_paths
    sep_photos = photos.split(",")

    return render_template("cafe_template.html", cafe=requested_cafe, photos=sep_photos, cafe_name=cafe_name)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = AddNewCafeForm()
    today = f"{date.today().strftime('%d')} of {date.today().strftime('%B')}, {date.today().strftime('%Y')}"
    if form.validate_on_submit():
        # Check if the folder exists, if not create it
        if not os.path.exists(f"static/images/cafes/{form.name.data}"):
            os.makedirs(f"static/images/cafes/{form.name.data}")

        files_filenames = []
        for file in request.files.getlist("images"):
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(f"static/images/cafes/{form.name.data}", file_filename))
            files_filenames.append(file_filename)

        new_cafe = Cafes(
            name=form.name.data,
            location=form.location.data,
            website=form.website.data,
            wifi_up=form.wifi_up.data,
            wifi_down=form.wifi_down.data,
            seating_range=form.seating_range.data,
            coffee_price=form.coffee_price.data,
            opens_wd=form.opens_wd.data,
            closes_wd=form.closes_wd.data,
            opens_we=form.opens_we.data,
            closes_we=form.closes_we.data,
            wifi_rating=form.wifi_rating.data,
            power_rating=form.power_rating.data,
            seating_rating=form.seating_rating.data,
            coffee_rating=form.coffee_rating.data,
            review_date=today,
            comments=form.comments.data,
            image_paths=','.join(files_filenames),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("index"))


    return render_template("add_cafe.html", form=form, year=year)

@app.route("/all_cafes")
def all_cafes():
    cafes = Cafes.query.all()
    return render_template("all_cafes.html", cafes=cafes)

if __name__ == "__main__":
    app.run(debug=True)
