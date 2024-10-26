import datetime
import interactions
from interactions import slash_command, SlashContext, listen, slash_option, OptionType

TOKEN = "MTI5OTc4NTA1OTM1MTQwMDU3MA.GVBOny.lvWoL-xR-Wq9lYAz_wEp8q-PTeCRKgKTRkZC0c"
SERVER_ID = 1299784563018563714

NUMBER_OF_MESSAGES = 100    # max 101

HELP_DESCRIPTION = "Explains the commands"
HELLO_DESCRIPTION = "Responds with hello"
GET_MOOD_DESCRIPTION = "Gives the mood around the given date"
GET_USER_MOOD_DESCRIPTION = "Gives the mood of a specific user"
DATE_DESCRIPTION = "The date to check - current date is used if none is given - YYYY-MM-DD format"
USER_DESCRIPTION = "The user to check - you are used if no user is given"

HELP_MESSAGE = f"""
help: {HELP_DESCRIPTION}\n
hello: {HELLO_DESCRIPTION}\n
get_mood [date]: {GET_MOOD_DESCRIPTION}\n
get_user_mood [date] [user]: {GET_USER_MOOD_DESCRIPTION}\n
\n
[date]: {DATE_DESCRIPTION}\n
[user]: {USER_DESCRIPTION}\n
"""


bot = interactions.Client(token=TOKEN)


@listen()
async def on_ready():
    print(f"logged in as {bot.user}")

@slash_command(
    name="help",
    description=HELP_DESCRIPTION,
    scopes=[SERVER_ID]
)
async def help(ctx: SlashContext):
    await ctx.send(HELP_MESSAGE)

@slash_command(
    name="hello",
    description=HELLO_DESCRIPTION,
    scopes=[SERVER_ID]
)
async def hello(ctx: SlashContext):
    await ctx.send("Hello!")


@slash_command(
    name="get_mood",
    description=GET_MOOD_DESCRIPTION,
    scopes=[SERVER_ID]
)
@slash_option(
    name="date_input",
    description=DATE_DESCRIPTION,
    required=False,
    opt_type=OptionType.STRING
)
async def get_mood(ctx: SlashContext, date_input: str = "today"):

    if date_input == "today":
        date = datetime.date.today()
    else:
        try:
            date = datetime.datetime.fromisoformat(date_input)
        except ValueError:
            await ctx.send("Invalid date")
            return

    messages = [message async for message in ctx.channel.history(limit=NUMBER_OF_MESSAGES,
                                                             around=date)]

    await ctx.send(f"{date}")


@slash_command(
    name="get_user_mood",
    description=GET_USER_MOOD_DESCRIPTION,
    scopes=[SERVER_ID]
)
@slash_option(
    name="date_input",
    description=DATE_DESCRIPTION,
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="user_input",
    description=USER_DESCRIPTION,
    required=False,
    opt_type=OptionType.STRING
)
async def get_user_mood(ctx: SlashContext, date_input: str = "today", user_input: str = "self"):

    if date_input == "today":
        date = datetime.date.today()
    else:
        try:
            date = datetime.datetime.fromisoformat(date_input)
        except ValueError:
            await ctx.send("Invalid date")
            return

    if user_input == "self":
        user = ctx.author.mention
    else:
        user = user_input

    messages = [message async for message in ctx.channel.history(limit=NUMBER_OF_MESSAGES,
                                                                 around=date)]

    user_messages = []
    for n in range(len(messages)):
        if messages[n].author.mention == user:
            user_messages.append(messages[n])

    await ctx.send(f"{date}, {user}")


if __name__ == '__main__':
    bot.start(TOKEN)
