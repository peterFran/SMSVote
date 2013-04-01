from app import app
from flask import render_template, request
import xml.etree.ElementTree as ET
import services
# View for displaying candidates
def candidates(voter):
	"""Display a table of candidates retrieved from the database"""
	candidates = services.candidates()

	return render_template("candidates.html",
		candidates = candidates, voter=voter)

def error(message):
	"""Display voter not found error"""
	return render_template("error.html", message=message)

@app.route("/welcome", methods=["GET"])
def logonScreen():
	"""Display logon screen"""
	return render_template("auth.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
	voter = services.authenticate(int(request.form["voter_id"]),1)
	if voter is not None:
		return candidates(voter)
	else:
		voted = services.checkVoted(int(request.form["voter_id"]), 1)
		if voted is None:
			return error("Voter ID is not registered")
		else:
			return error("%s %s has already voted" % (voted["first_name"], voted["last_name"]))
	
def success(voter):
	return render_template("success.html",
		voter=voter)