from app import app
from flask import render_template
import services
# View for displaying candidates
@app.route('/candidates')
def candidates():
	"""Display a table of candidates retrieved from the database"""
	candidates = services.candidates()
	return render_template("candidates.html",
		candidates = candidates)

@app.route('/results')
def results():
	"""Display table of results"""
	results = services.countVotes(1)
	return render_template("results.html",
		results = results)


