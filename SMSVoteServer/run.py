#!flask/bin/python
import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from app import app
import initCandidates
import initMachines

if __name__ == "__main__":
	initCandidates.main()
	initMachines.main()
	app.run(debug=True, port=8000, host='0.0.0.0')
