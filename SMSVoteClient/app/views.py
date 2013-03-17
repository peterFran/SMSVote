from app import app
from flask import render_template
import xml.etree.ElementTree as ET
import services
# View for displaying candidates
@app.route('/viewCandidates')
def candidates():
	"""Display a table of candidates retrieved from the database"""
	candidatesXML = services.candidates().response[0]
	candidates = ET.fromstring(candidatesXML)
	candidateslist = candidates._children
	return render_template("candidates.html",
		candidates = candidateslist)
