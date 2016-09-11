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
        j = connection.reserve()
        
        plateLen = len(j.data["results"][0]["plate"])   
        response =({ "plate":j.data["results"][0]["plate"], "confidence":j.data["results"][0]["confidence"], "capturedTime":j.data["epoch_time"], "uuidCamera":j.data["uuid"][:10] })
        
        if plateLen >= 6:       
            print json.dumps(response)
            headers = {'content-type': 'application/json'}
        
            # POST with JSON
            r = requests.post(URLPOST, data=json.dumps(response), headers=headers)
            # Response, status etc
            # print r.text
            print "Status: " + str(r.status_code)
            
        j.Finish()
        #time.sleep(100)
    except Exception, e:
        print e
        continue  

