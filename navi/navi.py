#!env/bin/python

import os
import time
from slackclient import SlackClient
from lib.bot import bot_command
from lib.bot import bot_parse
from lib.bot import make_client
from lib import accepted_commands

import lib.weather.weather as weather

import pdb

class Navi():
    _BOT_ID = os.environ.get("BOT_ID")
    _AT_BOT = "<@" + _BOT_ID + ">"
    def __init__(self):
        self.client = make_client()

    def is_connected(self):
        if self.client.rtm_connect():
            print("NaviBot connected and running!")
            return True
        else:
            print("Connection failed.")
            return False

    def parse_input(self):
        user_input= self.client.rtm_read()
        command, options, channel = bot_parse(rtm_output=user_input, at_id=navi._AT_BOT)

        return command, options, channel

    def command(self, command, result, channel):
        sass = "HEY!! LISTEN!!"
        response = bot_command(command, result, sass)
        self.client.api_call("chat.postMessage", channel=channel,
                            text=response, as_user=True)

    def decide_command(self, command, options):
        if command in accepted_commands.get():
            if command == "weather":
                result = weather.get(options)
            elif command == "test":
                result = "This is a test"
            else:
                result = "Command not yet implemented"
        else:
            result = "Invalid command"

        return result

if __name__ == "__main__":
    navi = Navi()
    READ_WEBSOCKET_DELAY = 1
    if navi.is_connected():
        while True:
            command, options, channel = navi.parse_input()
            if command and channel:
                result = navi.decide_command(command, options)
                response = navi.command(command, result, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
