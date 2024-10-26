from operator import truediv

import discord
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

COMMAND_CHARACTER = '/'
NUMBER_OF_MESSAGES = 100    # max 101


HELP_MESSAGE = """
help: explains the commands\n
hello: responds with hello\n
getMood [date]: gives the mood around the given date\n
        gets current mood if no date is given\n
getUserMood [user] [date]: gives the mood of a specific user around the given date\n
        gets the sender's mood if no user is specified\n
        gets current mood if no date is given\n 
\ndate is in the format YYYY-MM-DD\n
"""

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user or not message.content.startswith(COMMAND_CHARACTER):
        return

    command = message.content[1:].split(" ")
    channel = message.channel

    if command[0] == "help":
        await channel.send(HELP_MESSAGE)

    elif command[0] == "hello":
        await channel.send("Hello!")

    elif command[0] == "getMood":
        await getMood(command,message.channel)

    elif command[0] == "getUserMood":
        await getUserMood(command,message.channel, message)

    else:
        await channel.send("Unknown command - use /help to see available commands")


async def getMood(command, channel):
    if len(command) == 2:
        try:
            date = datetime.datetime.fromisoformat(command[1])
        except ValueError:
            await channel.send("Invalid date")
            return
    else:
        date = datetime.datetime.today()

    messages = [message async for message in channel.history(limit=NUMBER_OF_MESSAGES,
                                                                 around=date)]
    await channel.send(f"{date}")

async def getUserMood(command, channel, message):
    userMention = message.author.mention
    date = datetime.datetime.today()

    match len(command):
        case 2:
            if isUserMention(command[1]):
                userMention = command[1]
            else:
                try:
                    date = datetime.datetime.fromisoformat(command[1])
                except ValueError:
                    await channel.send("Invalid date")
                    return

        case 3:
            userMention = command[1]
            try:
                date = datetime.datetime.fromisoformat(command[2])
            except ValueError:
                await channel.send("Invalid date")
                return

    messages = [message async for message in channel.history(limit=NUMBER_OF_MESSAGES,
                                                             around=date)]
    for n in range(len(messages)):
        if not messages[n].author.mention == userMention:
            messages.pop(n)

    await channel.send(f"{date}, {userMention}")

def isUserMention(str):
    return str.startswith('@')

if __name__ == '__main__':
    client.run(TOKEN)
