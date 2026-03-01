import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Syncing slash commands would go here
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_ready(self):
        print('Bot is Ready')

def main():
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file.")
        return
    
    bot = MyBot()
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
