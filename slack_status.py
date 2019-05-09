#!/usr/bin/env python3

#working remote status update example
#curl -X POST https://slack.com/api/users.profile.set\?profile\=%7B%0A%20%20%20%20%22status_text%22%3A%20%22working%20remotely%22%2C%0A%20%20%20%20%22status_emoji%22%3A%20%22%3Ahouse_with_garden%3A%22%0A%7D\&token\=xoxp-19620222548-19620222564-611406198307-d7f963d3979e20f29794c0077061dcd0

#working from office status update example
#curl -X POST https://slack.com/api/users.profile.set\?profile\=%7B%0A%20%20%20%20%22status_text%22%3A%20%22San%20Diego%22%2C%0A%20%20%20%20%22status_emoji%22%3A%20%22%3Apost_office%3A%22%0A%7D\&token\=xoxp-19620222548-19620222564-611406198307-d7f963d3979e20f29794c0077061dcd0

#example api post request for status update below:
#POST /api/users.profile.set
#Host: slack.com
#Authorization: Bearer xoxp-19620222548-19620222564-611406198307-d7f963d3979e20f29794c0077061dcd0
#Content-type: application/json; charset=utf-8
#{
#    "profile": {
#        "status_text": "Working Remotely",
#        "status_emoji": ":house_with_garden:",
#        "status_expiration": 0,
#    }
#}

import subprocess
import requests
#import os

wifi_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
#wifi_path_cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk "/ SSID/ {print substr($0, index($0, $2))}"'

slack_token = 'xoxp-19620222548-19620222564-611406198307-d7f963d3979e20f29794c0077061dcd0'
slack_headers = {'Authorization': 'Bearer '+ slack_token, 'Content-Type': 'application/json'}

office_ssid = b'NOW-Corporate'
def office_status_update():
    office_status_body = {
        "profile": {
                "status_text": "San Diego",
                "status_emoji": ":post_office:",
                "status_expiration": 0,
            }
    }
    office_status = requests.post('https://slack.com/api/users.profile.set', json=office_status_body, headers=slack_headers)
    office_output = office_status.json()
    print (office_output['ok'])
    print ('Status updated to: '+ office_output['profile']['status_text'])
    #office_status.raise_for_status()

#do not need to specify ssid, since if you are in office SSID will = office_ssid
#wfh_ssid = b'ThanosDidNothingWrong'
def wfh_status_update():
    wfh_status_body = {
        "profile": {
                "status_text": "Working Remotely",
                "status_emoji": ":house_with_garden:",
                "status_expiration": 0,
            }
    }
    wfh_status = requests.post('https://slack.com/api/users.profile.set', json=wfh_status_body, headers=slack_headers)
    wfh_output = wfh_status.json()
    print (wfh_output['ok'])
    print ('Status updated to: ' + wfh_output['profile']['status_text'])
    #On your response object you can call: .raise_for_status(). Throw an exception if something wetn wrong, otherwise keep going
    #wfh_status.raise_for_status()



def update_slack_status():
    try:
        process = subprocess.Popen([wifi_path, '-I'], stdout=subprocess.PIPE)
        output, error = process.communicate()
        process.wait()
        if office_ssid in output:
            office_status_update()
            print ('Office')
        else:
            wfh_status_update()
            print ('WFH')
    except Exception as e:
        print('Something failed: ' + e)


#update_slack_status()

# add if name = main statement
if __name__ == '__main__':
    update_slack_status()
    print('Status update successful')