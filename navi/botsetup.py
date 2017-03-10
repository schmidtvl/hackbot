#env/bin/python

import os
from slackclient import SlackClient
import pdb

BOT_NAME = 'navi'
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == '__main__':
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:

