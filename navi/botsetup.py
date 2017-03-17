#!env/bin/python

import os
from slackclient import SlackClient
from lib import api_key
import pdb


BOT_NAME = 'navi'
key = api_key.get_key()
slack_client = SlackClient(key)

command_bot_id_set = '[ -z ${BOT_ID+x} ];'
bot_id_set = os.system(command_bot_id_set)

if bot_id_set is 0:
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if user.get('is_bot') and user.get('name') == BOT_NAME:
                bot_id = user.get('id')
                print(bot_id)

