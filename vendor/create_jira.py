#!/usr/bin/env python
__author__ = 'bassetma'

import json
import sys
import smtplib
from jira.client import JIRA


message = """From: Snorby-Jira Script <snorby-jira@secalert.net.hpcloud.net>
To: Mark Bassett <mark.wil.bassett@hp.com>, James Shupe <james.shupe@hp.com>
Subject: Snorby Jira failure

"""


def jira_connect():
    # Connect to JIRA
    jira_user = ""
    jira_pass = ""
    with open('/opt/snorby/.jiracreds') as f:
        credentials = [x.strip().split(':') for x in f.readlines()]
    for a, b in credentials:
        jira_user = a
        jira_pass = b
    jira_options = {
        'server': 'https://jira.hpcloud.net',
        'verify': '/etc/ssl/certs/ca-certificates.crt'
    }
    jira = JIRA(jira_options, basic_auth=(jira_user, jira_pass))
    return jira


def create_jira(jira, data):
    data = json.loads(data)
    description = "{}\n{{code}}{}{{code}}".format(
        data['jira']['description'], data['event']['payload']['data_payload'].decode("hex")
    )
    issue = {
        'project': data['jira']['project'],
        'summary': data['jira']['subject'],
        'description': description,
        'issuetype': {'name': 'Task'}
    }
    new_issue = jira.create_issue(fields=issue)
    return new_issue


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

def send_email(message):
  sender = 'snorby-jira@secalert.net.hpcloud.net'
  receivers = ['mark.wil.bassett@hp.com', 'james.shupe@hp.com']
  try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, message)
      print "Successfully sent email"
  except SMTPException:
      print "Error: unable to send email"

if __name__ == "__main__":
    for line in sys.stdin:
        if is_json(line):
            jira = jira_connect()
            issue = create_jira(jira, line)
        else:
            send_email(message + "Unable to create JIRA from " + line)
