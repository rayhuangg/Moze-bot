import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import generate_moze_urls

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MozeView(discord.ui.View):
    def __init__(self, boy_url: str, girl_url: str):
        super().__init__()
        # 建立兩個網址按鈕
        self.add_item(discord.ui.Button(label="👩 女友記帳", url=girl_url, emoji="👩"))
        self.add_item(discord.ui.Button(label="👦 男友記帳", url=boy_url, emoji="👦"))

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 同步斜線指令
        await self.tree.sync()
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_ready(self):
        print('Bot is Ready')

bot = MyBot()

@bot.tree.command(name="expense", description="記錄一筆共同花費")
@app_commands.describe(
    payer="誰付的錢？",
    subcategory="類別",
    amount="總金額",
    store="店家名稱 (選填)"
)
@app_commands.choices(payer=[
    app_commands.Choice(name="Ray", value="Ray"),
    app_commands.Choice(name="Moyichen", value="Moyichen"),
])
@app_commands.choices(subcategory=[
    app_commands.Choice(name="早餐", value="早餐"),
    app_commands.Choice(name="午餐", value="午餐"),
    app_commands.Choice(name="晚餐", value="晚餐"),
    app_commands.Choice(name="點心", value="點心"),
    app_commands.Choice(name="飲料", value="飲料"),
    app_commands.Choice(name="消夜", value="消夜"),
    app_commands.Choice(name="採購", value="採購"),
    app_commands.Choice(name="食材", value="食材"),
    app_commands.Choice(name="水果", value="水果"),
])
async def expense(
    interaction: discord.Interaction, 
    payer: app_commands.Choice[str], 
    subcategory: app_commands.Choice[str], 
    amount: int, 
    store: str = None
):
    # 產生 URL
    boy_url, girl_url = generate_moze_urls(payer.value, subcategory.value, amount, store)
    
    # 建立 Embed 訊息
    item_display = store if store else subcategory.value
    embed = discord.Embed(
        title=f"[{item_display}] 記帳確認",
        description=f"總額 {amount} / 由 {payer.name} 先墊",
        color=discord.Color.green()
    )
    
    # 回覆訊息與按鈕
    view = MozeView(boy_url, girl_url)
    await interaction.response.send_message(embed=embed, view=view)

def main():
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file.")
        return
    
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
