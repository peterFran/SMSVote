from app import app
from flask import render_template
import xml.etree.ElementTree as ET
import services
# View for displaying candidates
@app.route('/viewCandidates')
def candidates():
	"""Display a table of candidates retrieved from the database"""
	candidates = services.candidates()
	return render_template("candidates.html",
		candidates = candidates)


