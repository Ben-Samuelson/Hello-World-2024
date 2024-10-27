import os
from dotenv import load_dotenv

import datetime
import interactions
from interactions import slash_command, SlashContext, listen, slash_option, OptionType, Snowflake
from raven.contrib.django.models import client

TOKEN = str(os.getenv("TOKEN"))
SERVER_ID = 1299784563018563714

NUMBER_OF_MESSAGES = 100  # max 101

HELP_DESCRIPTION = "Explains the commands"
HELLO_DESCRIPTION = "Responds with hello"
SERVER_MOOD_DESCRIPTION = "Gives the mood around the given date"
USER_MOOD_DESCRIPTION = "Gives the mood of a specific user"
DATE_DESCRIPTION = "The date to check - current date is used if none is given - YYYY-MM-DD format"
USER_DESCRIPTION = "The user to check - you are used if no user is given"

HELP_MESSAGE = f"""
help: {HELP_DESCRIPTION}\n
hello: {HELLO_DESCRIPTION}\n
server_mood [date]: {SERVER_MOOD_DESCRIPTION}\n
user_mood [date] [user]: {USER_MOOD_DESCRIPTION}\n
\n
[date]: {DATE_DESCRIPTION}\n
[user]: {USER_DESCRIPTION}\n
"""


bot = interactions.Client(token=TOKEN)


@listen()
async def on_ready():
    print(f"logged in as {bot.user}")


@slash_command(name="help", description=HELP_DESCRIPTION, scopes=[SERVER_ID])
async def help(ctx: SlashContext):
    await ctx.send(HELP_MESSAGE)


@slash_command(name="hello", description=HELLO_DESCRIPTION, scopes=[SERVER_ID])
async def hello(ctx: SlashContext):
    await ctx.send("Hello!")


@slash_command(name="server_mood", description=SERVER_MOOD_DESCRIPTION, scopes=[SERVER_ID])
@slash_option(name="date_input", description=DATE_DESCRIPTION, required=False, opt_type=OptionType.STRING)
async def server_mood(ctx: SlashContext, date_input: str = "today"):

    if date_input == "today":
        date = Snowflake.from_datetime(datetime.datetime.today())
    else:
        try:
            date = Snowflake.from_datetime(datetime.datetime.fromisoformat(date_input))
        except ValueError:
            await ctx.send("Invalid date")
            return

    messages = [message async for message in ctx.channel.history(limit=NUMBER_OF_MESSAGES, around=date)]

    user_messages = []
    for message in messages:
        if message.author == client:
            user_messages.append(message.content)

    await ctx.send(f"{user_messages}")


@slash_command(name="user_mood", description=USER_MOOD_DESCRIPTION, scopes=[SERVER_ID])
@slash_option(name="date_input", description=DATE_DESCRIPTION, required=False, opt_type=OptionType.STRING)
@slash_option(name="user_input", description=USER_DESCRIPTION, required=False, opt_type=OptionType.STRING)
async def user_mood(ctx: SlashContext, date_input: str = "today", user_input: str = "self"):

    if date_input == "today":
        date = Snowflake.from_datetime(datetime.datetime.today())
    else:
        try:
            date = Snowflake.from_datetime(datetime.datetime.fromisoformat(date_input))
        except ValueError:
            await ctx.send("Invalid date")
            return

    if user_input == "self":
        user = ctx.author.mention
    else:
        user = user_input

    messages = [message async for message in ctx.channel.history(limit=NUMBER_OF_MESSAGES, around=date)]
    user_messages = []
    for message in messages:
        if message.author.mention == user:
            user_messages.append(message.content)

    await ctx.send(f"{user_messages}")


if __name__ == "__main__":
    load_dotenv()
    bot.start(TOKEN)
