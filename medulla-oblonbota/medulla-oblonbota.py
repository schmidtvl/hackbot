import os
import time
import wiki
import wikipedia
from models.film import Film
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack and Twilio clients
slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(slack_token)
username = ""

def handled_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use one of the supported commands."
    if command.startswith("find movie: "):
        result = wiki.getMoviePage(command.split(":",1)[1])
        if len(result) > 1:
            response = "Multiple results found:"
            for page in result:
                response += "\n" + page.url
        elif len(result) > 0:
            response = result[0].url
        elif len(result) == 0:
            response = "Could not find a movie with that name."
    elif command.startswith("suggest movie:" or "suggest film:"):
        movie_name = (command.split(": ",1)[1])
        pages = wiki.getMoviePage(movie_name)

        if len(pages) == 1:
            page = pages[0]
            if page.title.endswith(' (film)'):
                movie_name = page.title[:-7]
            else:
                movie_name = page.title
            response = add_or_update_entry(movie_name)
        elif len(pages) > 1:
            response = "Multiple results found, please select an exact title and try again:"
            for page in pages:
                response += ("\n" + page.url)
        else:
            add_or_update_entry(movie_name)
            response = movie_name + "added to the database. Please note no online entry was found."
    elif command.startswith("get random"):
        response = wiki.getRandomPage()
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def add_or_update_entry(movie_name):
    movie_name = str(movie_name)
    existing_entry = Film.find_one({'name': movie_name})
    username = "username" #used to test multiple users suggesting the same film
    if existing_entry is not None:
        suggesters = existing_entry['suggesters']
        if username not in suggesters:
            suggesters.append(username)
            existing_entry.update_instance({"name":movie_name, "suggesters":suggesters})
            response = "User added to suggestion list for " + movie_name + "."
        else:
            response = "User has already suggested " + movie_name + "."
    else:
        film = Film({
            "name": movie_name,
            "suggesters": [username]
        })
        film.save()
        response = movie_name + " added to the database."

    return response

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
                set_username(output)
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                        output['channel']
            elif output and 'text' in output and ('!hey' in output['text']):
                set_username(output)
                # return text after the !hey, whitespace removed
                return output['text'].split('!hey')[1].strip().lower(), \
                        output['channel']
    return None, None

def set_username(output):
    global username
    if output and 'user' in output:
        user_ID = output['user']
        user = slack_client.api_call("users.info", user=user_ID)['user']
        username = str(user['name'])

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
