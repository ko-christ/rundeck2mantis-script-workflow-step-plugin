# rundeck2mantis :: Rundeck Plugin to attach output of a Rundeck job to Mantis Bug Tracker

import sys,os
import suds 
import base64
import urllib2
import datetime
from ConfigParser import SafeConfigParser

# get env variables
RD_JOB_SERVERURL = os.environ['RD_JOB_SERVERURL']
RD_JOB_NAME = os.environ['RD_JOB_NAME']
RD_JOB_USERNAME = os.environ['RD_JOB_USERNAME']
RD_JOB_EXECID = os.environ['RD_JOB_EXECID']
RD_PLUGIN_TMPDIR = os.environ['RD_PLUGIN_TMPDIR']
RD_CONFIG_NUMBER = os.environ['RD_CONFIG_NUMBER']
RD_CONFIG_ASIF = os.environ['RD_CONFIG_ASIF']
RD_PLUGIN_SCRIPTFILE = os.environ['RD_PLUGIN_SCRIPTFILE']
RD_JOB_LOGLEVEL = os.environ['RD_JOB_LOGLEVEL']
CONFFILE = os.path.splitext(RD_PLUGIN_SCRIPTFILE)[0]+".conf"

# get configuration options
parser = SafeConfigParser()
parser.read(CONFFILE)
MANTISURL = str ( parser.get('MANTIS','MANTISURL') )
USERNAME = str ( parser.get('MANTIS','USERNAME') )
PASSWD = str ( parser.get('MANTIS','PASSWD') )
TOKEN = str ( parser.get('TOKENS','TOKEN') )
# API Version to use
API_V = str ( parser.get('API','API_V') )

# create filename with timestamp
TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
FILENAME_NO_PATH = RD_JOB_NAME+"_"+RD_JOB_EXECID+"_"+TIMESTAMP+".txt"

# create url
url = RD_JOB_SERVERURL+'api/'+API_V+'/execution/'+RD_JOB_EXECID+'/output?format=text&authtoken='+TOKEN

# debug output
if RD_JOB_LOGLEVEL == 'DEBUG':
	print "Debug info"
	print "RD_JOB_LOGLEVEL = "+os.environ['RD_JOB_LOGLEVEL']
	print "RD_JOB_SERVERURL = "+os.environ['RD_JOB_SERVERURL']
	print "RD_JOB_NAME = "+os.environ['RD_JOB_NAME']
	print "RD_JOB_EXECID = "+os.environ['RD_JOB_EXECID']
	print "RD_PLUGIN_TMPDIR = "+os.environ['RD_PLUGIN_TMPDIR']
	print "RD_CONFIG_NUMBER = "+os.environ['RD_CONFIG_NUMBER']
	print "RD_CONFIG_ASIF = "+os.environ['RD_CONFIG_ASIF']
	print "RD_PLUGIN_SCRIPTFILE = "+os.environ['RD_PLUGIN_SCRIPTFILE']
	print "CONFFILE = "+CONFFILE
	print "FILENAME_NO_PATH = "+FILENAME_NO_PATH
	print "URL = "+url


client = suds.client.Client(MANTISURL)

# get job output to f
try:
	f = urllib2.urlopen ( url )
except urllib2.HTTPError, e:
	checksLogger.error('HTTPError = ' + str(e.code))
	sys.exit(0)
except urllib2.URLError, e:
	checksLogger.error('URLError = ' + str(e.reason))
	sys.exit(0)
except httplib.HTTPException, e:
	checksLogger.error('HTTPException')
	sys.exit(0)

# attach file to Mantis Bug Tracker
try:
	ff = f.read()
	attach = base64.encodestring(ff)
	ff = f.close()
	client.service.mc_issue_attachment_add(USERNAME,PASSWD,RD_CONFIG_NUMBER,FILENAME_NO_PATH,'application/octet-stream',attach)
	print 'File attached to Mantis Bug Tracker\n'
except:
	print '\nIO error "%s"' %()
	sys.exit(0)


# post an automated message to Mantis Bug Tracker
if RD_CONFIG_ASIF == "true":
	try:
		new_note = client.factory.create('IssueNoteData')
		new_note.text =  "Job with id "+RD_JOB_EXECID+" completed by "+RD_JOB_USERNAME+" \nOutput attached ["+FILENAME_NO_PATH+"]\n"
		client.service.mc_issue_note_add(USERNAME,PASSWD,RD_CONFIG_NUMBER,new_note)
	except:
		print '\nIO error "%s"' %()
		sys.exit(0)



sys.exit(0)
