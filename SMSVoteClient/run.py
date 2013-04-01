#!flask/bin/python
import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from app import app
import initMachines
import initVoters
if __name__ == "__main__":
	initVoters.main()
	#initCandidates.main()
	initMachines.main()
	app.run(debug=True, port=7999, host='0.0.0.0')
