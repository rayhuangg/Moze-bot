import os
import discord
import logging
import urllib.parse
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import generate_moze_urls, get_taipei_now
from datetime import datetime, timedelta
from typing import List

# 設定標準日誌輸出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Redirector URL from docs/USAGE.md
REDIRECT_BASE_URL = "https://rayhuangg.github.io/Moze-bot/index.html?target="

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 同步斜線指令
        logger.info("正在同步斜線指令 (tree.sync)...")
        await self.tree.sync()
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("斜線指令同步完成！")

    async def on_ready(self):
        logger.info('Bot is Ready')
        logger.info(f"目前登入身份: {self.user} (ID: {self.user.id})")
        logger.info('Bot 已經就緒並在線上')


bot = MyBot()

# --- Autocomplete Functions ---

async def date_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    now = get_taipei_now()
    choices = []

    # 提供最近 7 天的選項
    labels = ["今天", "昨天", "前天"]
    for i in range(7):
        target_date = now - timedelta(days=i)
        date_str = target_date.strftime("%Y.%m.%d")
        label = labels[i] if i < len(labels) else f"{i} 天前"

        display_name = f"{label} ({date_str})"
        # 如果使用者已經開始輸入，過濾符合的選項
        if current.lower() in display_name.lower() or current in date_str:
            choices.append(app_commands.Choice(name=display_name, value=date_str))

    return choices[:25]

async def time_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    now = get_taipei_now()
    choices = []

    # 1. 現在時間
    choices.append(app_commands.Choice(name=f"現在 ({now.strftime('%H:%M')})", value=now.strftime("%H:%M")))

    # 2. 常用間隔
    intervals = [5, 10, 15, 30, 60]
    for mins in intervals:
        target_time = now - timedelta(minutes=mins)
        time_str = target_time.strftime("%H:%M")
        choices.append(app_commands.Choice(name=f"{mins} 分鐘前 ({time_str})", value=time_str))

    # 3. 最近的整點
    current_hour = now.hour
    for i in range(5):
        hour = (current_hour - i) % 24
        time_str = f"{hour:02d}:00"
        choices.append(app_commands.Choice(name=f"{time_str}", value=time_str))

    return [
        choice for choice in choices
        if current.lower() in choice.name.lower() or current in choice.value
    ][:25]

# --- Command ---

@bot.tree.command(name="expense", description="記錄一筆共同花費")
@app_commands.describe(
    subcategory="類別 (必填)",
    amount="總金額 (必填)",
    store="店家名稱 (必填)",
    date="日期 (可點選或輸入 YYYY.MM.dd)",
    time="時間 (可點選或輸入 HH:mm)",
    currency="幣別 (預設 TWD)",
    note="備註 (選填)"
)
@app_commands.choices(subcategory=[
    app_commands.Choice(name="午餐", value="午餐"),
    app_commands.Choice(name="晚餐", value="晚餐"),
    app_commands.Choice(name="飲料", value="飲料"),
    app_commands.Choice(name="採購", value="採購"),
    app_commands.Choice(name="早餐", value="早餐"),
    app_commands.Choice(name="點心", value="點心"),
    app_commands.Choice(name="宵夜", value="宵夜"),
    app_commands.Choice(name="水果", value="水果"),
    app_commands.Choice(name="日常用品", value="日常用品"),
    app_commands.Choice(name="住宿", value="住宿"),
    app_commands.Choice(name="電影", value="電影"),
])
@app_commands.autocomplete(date=date_autocomplete, time=time_autocomplete)
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
    # 記錄斜線指令的接收
    logger.info(f"[指令接收] 用戶: {interaction.user.name} (ID: {interaction.user.id})")
    logger.info(f"類別={subcategory.value}, 金額={amount}, 店家={store}, 日期={date}, 時間={time}, 幣別={currency}, 備註={note}")

    # 處理預設時間 (如果使用者沒有選擇也沒有手動輸入)
    now = get_taipei_now()
    final_date = date if date else now.strftime("%Y.%m.%d")
    final_time = time if time else now.strftime("%H:%M")

    # 產生原始 URL Scheme
    moze3_raw, moze_raw = generate_moze_urls(
        subcategory=subcategory.value,
        amount=amount,
        store=store,
        date=final_date,
        time=final_time,
        currency=currency,
        note=note
    )

    # 封裝為重導向連結
    moze3_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze3_raw, safe='')}"
    moze_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze_raw, safe='')}"

    description = (
        f"🏪 **類型**: {subcategory.value}\n"
        f"💰 **總額**: {amount} {currency}\n"
        f"🏪 **店家**: {store}\n"
        f"📅 **時間**: {final_date} {final_time}\n"
        f"📝 **備註**: {note if note else '無'}\n\n"
        f"🔗 **記帳URL**：\n"
        f"👦 [moze3 點我記帳]({moze3_url})\n"
        f"👩 [moze 點我記帳]({moze_url})\n\n"
    )

    embed = discord.Embed(
        title=f"記帳確認",
        description=description,
        color=discord.Color.green()
    )

    # 回覆訊息
    await interaction.response.send_message(embed=embed)

def main():
    if not TOKEN:
        logger.error("DISCORD_TOKEN not found in .env file.")
        return

    bot.run(TOKEN)

if __name__ == "__main__":
    main()
