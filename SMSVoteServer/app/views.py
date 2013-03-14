from app import app
from CandidateManagement.CandidateModel import CandidateModel
from flask import render_template
import sqlite3
# View for displaying candidates
@app.route('/candidates')
def candidates():
	"""Display a table of candidates retrieved from the database"""
	con = sqlite3.connect('./app/static/data/candidates.db')
	candidate_model  = CandidateModel(con)
	candidates = candidate_model.getAllCandidates()
	con.close()
	return render_template("candidates.html",
		candidates = candidates)
