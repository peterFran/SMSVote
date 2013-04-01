#!flask/bin/python
import sys
sys.path.append('/Users/petermeckiffe/Desktop/Work/University/UWE/Year 3/Computing Project/ComputingProject/SMSVote/PythonGateway')
from app import app
import initElection
import initMachines

if __name__ == "__main__":
	initElection.main()
	initMachines.main()
	
	app.run(debug=True, port=8000, host='0.0.0.0')
	
