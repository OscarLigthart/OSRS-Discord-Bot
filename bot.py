import os
import re

import discord
from dotenv import load_dotenv
from hiscores.scores import Scores

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

SKILLS = ['total', 'attack', 'defense', 'strength',
          'hitpoints', 'ranged', 'prayer', 'magic',
          'cooking', 'woodcutting', 'fletching', 'fishing',
          'firemaking', 'crafting', 'smithing', 'mining',
          'herblore', 'agility', 'thieving', 'slayer',
          'farming', 'runecrafting', 'hunter', 'construction']

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    """
    @todo put all commands in separate files
    :param message:
    :return:
    """

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # intializes a scores object
    hiscores = Scores(message)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    # get the command without !
    command = message.content.split()[0][1:]

    # retrieve the score of a player
    if message.content.startswith('!') and command in SKILLS:

        # retrieve the username that comes after the !level command and set underscores
        username = message.content.split()[1:]
        username = '_'.join(username)

        # get scores
        await hiscores.show_score(username, command)

    if message.content.startswith('!compare'):

        # get skill
        skill = message.content.split()[1]

        # check if the skill is valid, if not we compare based on total level and experience
        if not skill in SKILLS:

            # get the players
            players = ' '.join(message.content.split()[1:])
            players = players.split(' - ')

            for i, player in enumerate(players):
                players[i] = player.replace(' ', '_')

            # compare the players on total level if nothing is given
            await hiscores.compare(players, 'total')

        else:

            # get the players after the skill
            players = ' '.join(message.content.split()[2:])
            players = players.split(' - ')

            for i, player in enumerate(players):
                players[i] = player.replace(' ', '_')

            print(players)
            print(skill)
            # compare the players on total level if nothing is given
            await hiscores.compare(players, skill)


    if message.content.startswith('!pok'):
        msg = 'Heb je m al Marc?'.format(message)
        await message.channel.send(msg)


# @client.event
# async def on_ready():
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('------')

client.run(TOKEN)