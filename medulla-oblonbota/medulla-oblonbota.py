import os
import time
import wiki
import pdb
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack and Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handled_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use one of the supported commands."
    if command.startswith("find movie: "):
        result = wiki.getMovieUrl(command.split(":",1)[1])
        if len(result) > 1:
            response = "Multiple results found:"
            for url in result:
                response += "\n" + url
        elif len(result) > 0:
            response = result[0]
        elif len(result) == 0:
            response = "Could not find a movie with that name."
    elif command.startswith("find video game: "):
        result = wiki.getGameUrl(command.split(":",1)[1])
        if len(result) > 1:
            response = "Multiple results found:"
            for url in result:
                response += "\n" + url
        elif len(result) > 0:
            response = result[0]
        elif len(result) == 0:
            response = "Could not find a game with that name."
    elif command.startswith("get random"):
        response = wiki.getRandomPage()
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and (AT_BOT in output['text']):
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']
            elif output and 'text' in output and ('!hey' in output['text']):
                # return text after the @ mention, whitespace removed
                return output['text'].split('!hey')[1].strip().lower(), \
                        output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Medulla Oblonbota connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handled_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
