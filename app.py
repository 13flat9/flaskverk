from flask import Flask, render_template, request
import wtforms
from models import Search
from search import Artist, Performance 


app = Flask(__name__)
#gera config skjal, með class Config:?
app.config['SECRET_KEY'] = 'leyndarmál'


# Hafa search hér og líka í /search?
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/search")
def search():
    search_query = request.args.get('search_query')
    if search_query:
        artist = Artist(search_query)

    form = Search()
    return render_template("search.html", form=form, title="Search", artist=artist)