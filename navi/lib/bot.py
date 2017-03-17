from slackclient import SlackClient
import api_key
import accepted_commands

def make_client():
    return SlackClient(api_key.get_key())

def bot_command(command, result, custom):
    response = custom + "\n\n"
    if command == "weather":
        response += result
    elif command == "test":
        response += "You did test"
    else:
        response += "That's not a valid command!"

    return response


def bot_parse(rtm_output, at_id):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                text = output['text']
                channel = output['channel']
                if text.startswith("!"):
                    opts =  text.split(" ")
                    cmd = opts[0][1:len(opts[0])]
                    options = opts[1:len(opts)]
                    if len(options) == 0:
                        options = None
                    if cmd in accepted_commands.get():
                        return cmd, \
                            options, \
                            channel
    return None, None, None
