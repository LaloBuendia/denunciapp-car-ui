# stdlib imports
import sys
import time
import json
import requests

from beanstalk import serverconn
from beanstalk import job

SERVER = '127.0.0.1'
PORT = 11300
URLPOST = "http://172.16.11.235:8080/plate"

# try:
# setup connection
connection = serverconn.ServerConn(SERVER, PORT)

connection.watch('alprd')

connection.job = job.Job

print "Starting queue processing..."

# consume data
while True:    
    try:
        tmp = connection.reserve()
        #import pdb; pdb.set_trace()
	j = json.loads(tmp.data)

        plateLen = (j["results"][0]["plate"])  
 
        response =({ "plate":j["results"][0]["plate"], "confidence":j["results"][0]["confidence"], "capturedTime":j["epoch_time"], "uuidCamera":j["uuid"][:10] })
        
        if plateLen >= 6:       
            print json.dumps(response)
            headers = {'content-type': 'application/json'}
        
            # POST with JSON
            r = requests.post(URLPOST, data=json.dumps(response), headers=headers)
            # Response, status etc
            # print r.text
            print "Status: " + str(r.status_code)
            
        tmp.Finish()
	#time.sleep(1)
    except Exception, e:
        print e
        continue  

