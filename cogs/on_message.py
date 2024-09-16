from discord.ext import commands
from discord.utils import get
import discord

from config import Config

import asyncio
import random

class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

            msg = await self.bot.get_channel(message.channel.id).send("Start Wordle event, add reaction to join event")

            players = []

            timeoutBool = False
            while timeoutBool == False:
                try: 
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=5)
                except asyncio.TimeoutError:
                    timeoutBool = True
                else:
                    if user not in players:
                        players.append({
                            "player": user,
                            "skip_count": 0
                        })

            print(players)

            if players == []:
                await self.bot.get_channel(message.channel.id).send(f"No players, game does not start!")
                return

            guesses = ""
            words = open("assets/slowa5.txt", "r").read().splitlines()
            rand_word = words[random.randint(0, len(words)) - 1]

            print(rand_word)

            gameIsRunning = True
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
                        if message.content == rand_word:
                            await self.bot.get_channel(message.channel.id).send(f"{message.author.name} guessed word!")
                            gameIsRunning = False
                            break
                        idx = 0
                        for letter in message.content:
                            if letter == rand_word[idx]:
                                guesses += Config.get(letter.upper(), "GREEN_LETTERS")
                            elif letter in rand_word:
                                guesses += Config.get(letter.upper(), "YELLOW_LETTERS")
                            else:
                                guesses += Config.get(letter.upper(), "WHITE_LETTERS")
                            idx += 1
                        guesses += "\n"
                        await self.bot.get_channel(message.channel.id).send(guesses)
                    
                if players == []:
                    await self.bot.get_channel(message.channel.id).send(f"No players, game ended!")
                    gameIsRunning = False
                    break
            
            Config.set("EVENT_IS_RUNNING", False)




async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))