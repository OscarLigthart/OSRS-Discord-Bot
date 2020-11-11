from OSRS_Hiscores import Hiscores
import discord
import numpy as np

import matplotlib.pyplot as plt

class Scores:
    """
    This class is responsible for retrieving the OSRS hiscores if a name is given
    and optionally showing it in a fancy way

    @todo should there be a function for creating an embed?
    """

    def __init__(self, message):
        self.message = message
        return

    async def _create_compare_plot(self, scores):
        """
        This function creates a plot in the form of an image that will be embedded by the bot
        :return: image holding the plot
        """

        # what should be shown?
        labels = ['Rank', 'Level', 'Experience']

        # get the number of players
        players = list(scores.keys())
        num_players = len(players)

        x = np.arange(0, num_players, 0.5)

        fig, axes = plt.subplots(1, 3)

        for i, ax in enumerate(axes):

            # get all userscores
            measures = []
            for username, userscore in scores.items():
                measures.append(int(userscore[labels[i].lower()]))

            # plot scores
            for j, measure in enumerate(measures):
                ax.bar(x[j], measure, 0.5)

            ax.set_xlim(-0.5, x[num_players-1] + 0.5)
            ax.set_xticks([])
            ax.set_title(labels[i])

        axes[1].legend(labels=players, loc='upper center',
                     bbox_to_anchor=(0.5, -0.1), fancybox=False, shadow=False)

        fig.tight_layout(pad=3.0)
        fig.savefig('images/compare.png')
        plt.close(fig)

        await self._show_fig()
        return

    async def _show_fig(self):
        """
        Function to show a figure
        :return:
        """

        # create a description
        embedVar = discord.Embed(title="Comparing " + self.skill, description="", color=0x00ff00)
        file = discord.File("images/compare.png", filename="image.png")
        embedVar.set_image(url="attachment://image.png")
        await self.message.channel.send(file=file, embed=embedVar)
        return

    async def show_score(self, username, skill):

        # retrieve the username scores
        user = Hiscores(username, 'N')

        # get the info related to the skill
        info = user.stats[skill]

        # create a description
        embedVar = discord.Embed(title=username.replace('_', ' '), description=skill.capitalize(), color=0x00ff00)
        embedVar.add_field(name='Rank', value=info['rank'], inline=True)
        embedVar.add_field(name='Level', value=info['level'], inline=True)
        embedVar.add_field(name='XP', value=info['experience'], inline=True)
        embedVar.add_field(name="XP for next level", value=info['exp_to_next_level'], inline=True)
        await self.message.channel.send(embed=embedVar)

        return

    async def compare(self, players, skill):

        # create dict for holding scores
        scores = {}

        self.players = players
        self.skill = skill

        # go through all players
        for player in players:

            try:
                # retrieve the username scores
                user = Hiscores(player, 'N')
            except:
                # send the message
                pass

            # store the correct skill stat
            scores[player] = user.stats[skill]

        # create the compare plot
        await self._create_compare_plot(scores)

        return


