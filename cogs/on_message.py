from discord.ext import commands
from discord.utils import get
import discord

from config import Config

import asyncio
import random

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = bot.session

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Check if author is bot
        if message.author.bot == True:
            return
        
        # Check if event is running
        if Config.get("EVENT_IS_RUNNING") == True:
            return
        
        # Update message_count
        Config.set("MESSAGES_COUNT", Config.get("MESSAGES_COUNT") + 1)

        # Check if messages_count is equal to count_to_start_wordle_event
        if Config.get("MESSAGES_COUNT") >= Config.get("COUNT_TO_START_WORDLE_EVENT"):
            Config.set("EVENT_IS_RUNNING", True)
            Config.set("MESSAGES_COUNT", 0)

            embed = discord.Embed(description="<:announcement:1285518810882904145> **It is time to play <:w_w:1283958934130131056><:y_o:1283957528740237394><:g_r:1283957879472259115><:w_d:1283816214338080809><:w_l:1283823138416890019><:g_e:1283817004389761086>, add reaction to this message to join event**", color=discord.Color.from_rgb(255, 255, 255))

            msg = await self.bot.get_channel(message.channel.id).send(embed=embed)
            await msg.add_reaction("<:add:1285518781434691584>")

            players = []

            timeoutBool = False
            while timeoutBool == False:
                try: 
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=5)
                except asyncio.TimeoutError:
                    timeoutBool = True
                else:
                    if user.bot == False:
                        if user not in players:
                            players.append({
                                "player": user,
                                "skip_count": 0
                            })

            if players == []:
                await self.bot.get_channel(message.channel.id).send(f"No players, game does not start!")
                return
            
            embed = discord.Embed(description="**<:announcement:1285518810882904145> Let's guess the <:w_w:1283958934130131056><:y_o:1283957528740237394><:g_r:1283957879472259115><:w_d:1283816214338080809>**",color=discord.Color.from_rgb(255, 255, 255))
            players_field_desc = ""
            for idx, player in enumerate(players):
                players_field_desc += f"{idx+1}. {player['player']}\n"
            embed.add_field(name="Players", value=players_field_desc)
            await self.bot.get_channel(message.channel.id).send(embed=embed)

            guesses = ""
            words = open("assets/slowa5.txt", "r").read().splitlines()
            rand_word = "fisze"

            print(rand_word)

            gameIsRunning = True
            green_letters = [None, None, None, None, None]
            yellow_letters = []
            guesses_count = 0
            while gameIsRunning:
                for player in players:
                    try:
                        def check(m):
                            return m.author == player["player"]
                        
                        await self.bot.get_channel(message.channel.id).send(f"<@{player['player'].id}> now is your turn!")
                        message = await self.bot.wait_for("message", timeout=10, check=check)

                        if len(message.content) > 5:
                            raise commands.CommandError("Less than 6 letters!")
                        if message.content not in words:
                            raise commands.CommandError("There is no such word!")
                    except asyncio.TimeoutError:
                        player["skip_count"] += 1
                        await self.bot.get_channel(message.channel.id).send(f"<@{player['player'].id}> your time has ended! Skipped count {player['skip_count']}/3")
                        if player["skip_count"] >= 3:
                            players.remove(player)
                    except commands.CommandError as e:
                        await self.bot.get_channel(message.channel.id).send(f"Error: {e}")
                    else:
                        if message.content.lower() == rand_word:
                            await self.bot.get_channel(message.channel.id).send(f"{message.author.name} guessed word!")
                            self.session.increment_win(player["player"].id)
                            gameIsRunning = False
                            break
                        idx = 0
                        if guesses_count == 6:
                            guesses_count = 0
                            guesses = ""
                        for letter in message.content.lower():
                            if letter == rand_word[idx]:
                                guesses += Config.get(letter.upper(), "GREEN_LETTERS")
                                if green_letters[idx] == None:
                                    green_letters[idx] = letter
                                    self.session.increment_green_guessed(player["player"].id)
                                    
                            elif letter in rand_word:
                                guesses += Config.get(letter.upper(), "YELLOW_LETTERS")
                                if letter not in yellow_letters:
                                    yellow_letters.append(letter)
                                    self.session.increment_yellow_guessed(player["player"].id)
                            else:
                                guesses += Config.get(letter.upper(), "WHITE_LETTERS")
                            idx += 1
                        guesses += "\n"
                        guesses_count += 1

                        desc = "**<:announcement:1285518810882904145> Let's guess the <:w_w:1283958934130131056><:y_o:1283957528740237394><:g_r:1283957879472259115><:w_d:1283816214338080809>**\n\n"
                        for letter in green_letters:
                            if letter == None:
                                desc += "<:w_empty:1285529933065621514>"
                            else:
                                desc += Config.get(letter.upper(), "GREEN_LETTERS")

                        desc += " "
                        for letter in yellow_letters:
                            if letter in green_letters:
                                if green_letters.count(letter) < rand_word.count(letter):
                                    desc += Config.get(letter.upper(), "YELLOW_LETTERS")
                            else:
                                print(letter, yellow_letters.count(letter), rand_word.count(letter), yellow_letters.count(letter) <= rand_word.split().count(letter))
                                if yellow_letters.count(letter) <= rand_word.count(letter):
                                    desc += Config.get(letter.upper(), "YELLOW_LETTERS")

                        embed = discord.Embed(description=desc,color=discord.Color.from_rgb(255, 255, 255))
                        embed.add_field(name="Guesses", value=guesses)
                        await self.bot.get_channel(message.channel.id).send(embed=embed)
                    
                if players == []:
                    await self.bot.get_channel(message.channel.id).send(f"No players, game ended!")
                    gameIsRunning = False
                    break
            
            Config.set("EVENT_IS_RUNNING", False)




async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))