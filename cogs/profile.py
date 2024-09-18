from discord import app_commands
from discord.ext import commands
from discord.utils import get
import discord

from datetime import datetime

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = bot.session

    @app_commands.command(name="profile")
    async def profile(self, interaction: discord.Interaction):
        member = self.session.get_member(interaction.user.id)
        print(member, interaction.user)
        embed = discord.Embed(description=f"**<:w_w:1283958934130131056><:w_o:1283957502635020288><:w_r:1283957842784813157><:w_d:1283816214338080809><:w_s:1283958173077606432> Guessed:** `{member.words_guessed}`\n\n**<:g_g:1283820775429771414><:g_r:1283957879472259115><:g_e:1283817004389761086><:g_e:1283817004389761086><:g_n:1283832407207710781> Guessed:** `{member.green_guessed}`\n\n**<:y_y:1283959106545389618><:y_e:1283816984735387743><:y_l:1283823157660090378><:y_l:1283823157660090378><:y_o:1283957528740237394><:y_w:1283958955403378688> Guessed:** `{member.yellow_guessed}`",color=discord.Color.from_rgb(255, 255, 255))
        embed.set_author(name=f"{interaction.user.name}'s Profile", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))