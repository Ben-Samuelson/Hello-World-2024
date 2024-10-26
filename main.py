import nltk
from nrclex import NRCLex
from operator import truediv

import discord
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TOKEN = "MTI5OTc4NTA1OTM1MTQwMDU3MA.GVBOny.lvWoL-xR-Wq9lYAz_wEp8q-PTeCRKgKTRkZC0c"
COMMAND_CHARACTER = '/'
NUMBER_OF_MESSAGES = 100    # max 101

HELP_MESSAGE = """
**/help:\n** explains the commands
**/hello:\n** responds with hello
**/getMood [date]:\n** gives the mood around the given date\ngets current mood if no date is given
**/getUserMood [user] [date]:\n** gives the mood of a specific user around the given date
gets the sender's mood if no user is specified
gets current mood if no date is given
date is in the format YYYY-MM-DD\n
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
    user = message.author

    if command[0] == "help":
        await channel.send(HELP_MESSAGE)

    elif command[0] == "hello":
        await channel.send(f"Hello, {user}!")

    elif command[0] == "servermood":
        await getMood(command, message.channel)

    elif command[0] == "user_mood":
        await getUserMood(command, message.channel, message)

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

    res = {
        "fear": 0,
        "anger": 0,
        "anticipation": 0,
        "trust": 0,
        "surprise": 0,
        "positive": 0,
        "negative": 0,
        "sadness": 0,
        "disgust": 0,
        "joy": 0
    }
    for message in messages:
        if message.author.id == 1299785059351400570:
            continue
        if message.startsWith("/"):
            continue
        emotion = NRCLex(message.content)
        resm = emotion.raw_emotion_scores
        for emo in res:
            if emo in resm:
                res[emo]+= resm[emo]

    tot_sc = sum(res.values())
    if tot_sc>0:
        emotion_perc = {emotion: (score / tot_sc) * 100 for emotion, score in res.items()}
    else:
        emotion_perc = {emotion: 0 for emotion in res}
    emotion_perc = sorted(emotion_perc.items(), key=lambda item: item[1], reverse=True)
    str = ""
    strbar = ""
    check = True
    for emo in emotion_perc:
        if emo[1]== 0:
            break
        strbar = '🟩'*res[emo[0]] + '⬛'*(tot_sc - res[emo[0]])
        str += f"{emo[0].capitalize()}: {emo[1]:.2f}%\n{strbar}\n"
        check=False
    if check:
        await channel.send("No emotions detected. Is everyone here perfectly stoic? :no_mouth:")
    else:
        await channel.send(f"Here are the top emotions in the server!")
        await channel.send(str)

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