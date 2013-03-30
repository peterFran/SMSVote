from app import app
from flask import render_template
import xml.etree.ElementTree as ET
import services
# View for displaying candidates
def candidates(voter):
	"""Display a table of candidates retrieved from the database"""
	candidates = services.candidates()

	return render_template("candidates.html",
		candidates = candidates, voter=voter)

def error():
	"""Display voter not found error"""
	return render_template("error.html")

@app.route("/vote", methods=["GET"])
def logonScreen():
	"""Display logon screen"""
	return render_template("auth.html")