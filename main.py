import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import generate_moze_urls
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
    subcategory="類別 (必填)",
    amount="總金額 (必填)",
    store="店家名稱 (必填)",
    date="日期 YYYY.MM.dd (預設今日)",
    time="時間 HH:mm (預設現在)",
    currency="幣別 (預設 TWD)",
    note="備註 (選填)"
)
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
    subcategory: app_commands.Choice[str], 
    amount: int, 
    store: str,
    date: str = None,
    time: str = None,
    currency: str = "TWD",
    note: str = None
):
    # 處理預設時間
    now = datetime.now()
    final_date = date if date else now.strftime("%Y.%m.%d")
    final_time = time if time else now.strftime("%H:%M")
    
    # 產生 URL
    moze3_url, moze_url = generate_moze_urls(
        subcategory=subcategory.value, 
        amount=amount, 
        store=store, 
        date=final_date, 
        time=final_time, 
        currency=currency, 
        note=note
    )
    
    # 建立 Embed 訊息
    item_display = store
    
    description = (
        f"💰 **總額**: {amount} {currency}\n"
        f"🏪 **店家**: {store}\n"
        f"📅 **時間**: {final_date} {final_time}\n"
        f"📝 **備註**: {note if note else '無'}\n\n"
        f"🔗 **一鍵記帳**：\n"
        f"👩 [moze3 點我記帳]({moze3_url})\n"
        f"👦 [moze 點我記帳]({moze_url})\n\n"
        f"💡 *如果上方連結無法點選，請使用下方原始網址：*\n"
        f"👩 {moze3_url}\n"
        f"👦 {moze_url}"
    )
    
    embed = discord.Embed(
        title=f"[{item_display}] 記帳確認",
        description=description,
        color=discord.Color.green()
    )
    
    # 回覆訊息
    await interaction.response.send_message(embed=embed)

def main():
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file.")
        return
    
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
