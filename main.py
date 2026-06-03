import os
import discord
import logging
import urllib.parse
import re
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import generate_moze_urls, get_taipei_now
from datetime import datetime, timedelta
from typing import List, Optional

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


class ExpenseModal(discord.ui.Modal, title="補充記帳資訊"):
    def __init__(
        self,
        interaction: discord.Interaction,
        amount: int,
        store: str,
        name: Optional[str],
        date: str,
        time: str,
        currency: str,
        note: Optional[str],
        subcategory_val: str,
        needs_category: bool,
        needs_date: bool,
        needs_time: bool
    ):
        super().__init__()
        self._interaction = interaction
        self._amount = amount
        self._store = store
        self._name = name
        self._date = date
        self._time = time
        self._currency = currency
        self._note = note
        self._subcategory_val = subcategory_val
        self._needs_category = needs_category
        self._needs_date = needs_date
        self._needs_time = needs_time

        if needs_category:
            self.category_input = discord.ui.TextInput(
                label="記帳類別 (如: 機票)",
                placeholder="請輸入類別名稱",
                max_length=50,
                required=True
            )
            self.add_item(self.category_input)

        if needs_date:
            self.date_input = discord.ui.TextInput(
                label="日期 (格式: YYYY.MM.dd)",
                placeholder="例如: 2024.01.01",
                default=date if date != "自訂" else get_taipei_now().strftime("%Y.%m.%d"),
                min_length=10,
                max_length=10,
                required=True
            )
            self.add_item(self.date_input)

        if needs_time:
            self.time_input = discord.ui.TextInput(
                label="時間 (格式: HH:mm)",
                placeholder="例如: 14:30",
                default=time if time != "自訂" else get_taipei_now().strftime("%H:%M"),
                min_length=5,
                max_length=5,
                required=True
            )
            self.add_item(self.time_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        final_subcategory = self.category_input.value if self._needs_category else self._subcategory_val
        final_date = self.date_input.value if self._needs_date else self._date
        final_time = self.time_input.value if self._needs_time else self._time

        # 簡單的正則驗證
        if self._needs_date and not re.match(r"^\d{4}\.\d{2}\.\d{2}$", final_date):
            await interaction.response.send_message("❌ 日期格式錯誤，請使用 YYYY.MM.dd (例如 2024.01.01)", ephemeral=True)
            return

        if self._needs_time and not re.match(r"^\d{2}:\d{2}$", final_time):
            await interaction.response.send_message("❌ 時間格式錯誤，請使用 HH:mm (例如 14:30)", ephemeral=True)
            return

        moze3_raw, moze_raw = generate_moze_urls(
            subcategory=final_subcategory,
            amount=self._amount,
            store=self._store,
            name=self._name,
            date=final_date,
            time=final_time,
            currency=self._currency,
            note=self._note,
        )

        moze3_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze3_raw, safe='')}"
        moze_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze_raw, safe='')}"

        description = (
            f"🏪 **類型**: {final_subcategory}\n"
            f"💰 **總額**: {self._amount} {self._currency}\n"
            f"🏪 **店家**: {self._store}\n"
            f"🛒 **商品**: {self._name if self._name else '無'}\n"
            f"📅 **時間**: {final_date} {final_time}\n"
            f"📝 **備註**: {self._note if self._note else '無'}\n\n"
            f"🔗 **記帳URL**：\n"
            f"👦 [moze3 點我記帳]({moze3_url})\n"
            f"👩 [moze 點我記帳]({moze_url})\n\n"
        )

        embed = discord.Embed(
            title=f"記帳確認",
            description=description,
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

# --- Autocomplete Functions ---

async def date_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    now = get_taipei_now()
    choices = []

    # 1. 自訂選項
    choices.append(app_commands.Choice(name="📅 自訂日期 (手動輸入)", value="自訂"))

    # 2. 提供最近 7 天的選項，使用星期縮寫顯示
    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        target_date = now - timedelta(days=i)
        date_str = target_date.strftime("%Y.%m.%d")
        label = weekday_labels[target_date.weekday()]

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

    # 1. 自訂選項
    choices.append(app_commands.Choice(name="⏰ 自訂時間 (手動輸入)", value="自訂"))

    # 2. 現在時間
    choices.append(app_commands.Choice(name=f"現在 ({now.strftime('%H:%M')})", value=now.strftime("%H:%M")))

    # 3. 常用間隔
    intervals = [30, 60]
    for mins in intervals:
        target_time = now - timedelta(minutes=mins)
        time_str = target_time.strftime("%H:%M")
        choices.append(app_commands.Choice(name=f"{mins} 分鐘前 ({time_str})", value=time_str))

    # 4. 最近的整點
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
    name='商品名稱 (選填)',
    date="日期",
    time="時間",
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
    app_commands.Choice(name="其他", value="其他"),
])
@app_commands.autocomplete(date=date_autocomplete, time=time_autocomplete)
async def expense(
    interaction: discord.Interaction,
    subcategory: app_commands.Choice[str],
    amount: int,
    store: str,
    name: str = None,
    date: str = None,
    time: str = None,
    currency: str = "TWD",
    note: str = None,
    other_category: str = None
):
    # 記錄指的接收
    logger.info(f"[指令接收] 用戶: {interaction.user.name} (ID: {interaction.user.id})")
    logger.info(f"類別={(other_category if other_category else (subcategory.value if subcategory else 'None'))}, 金額={amount}, 店家={store}, 名稱={name}, 日期={date}, 時間={time}, 幣別={currency}, 備註={note}")

    # 處理預設時間 (如果使用者沒有選擇也沒有手動輸入)
    now = get_taipei_now()

    # 判斷是否需要開啟 Modal
    needs_category = (subcategory and subcategory.value == '其他') and not other_category
    needs_date = (date == "自訂")
    needs_time = (time == "自訂")

    if needs_category or needs_date or needs_time:
        modal = ExpenseModal(
            interaction=interaction,
            amount=amount,
            store=store,
            name=name,
            date=date if date else now.strftime("%Y.%m.%d"),
            time=time if time else now.strftime("%H:%M"),
            currency=currency,
            note=note,
            subcategory_val=subcategory.value if subcategory else "其他",
            needs_category=needs_category,
            needs_date=needs_date,
            needs_time=needs_time
        )
        await interaction.response.send_modal(modal)
        return

    final_date = date if date else now.strftime("%Y.%m.%d")
    final_time = time if time else now.strftime("%H:%M")
    final_subcategory = other_category if other_category else (subcategory.value if subcategory else '未提供')

    # 產生原始 URL Scheme
    moze3_raw, moze_raw = generate_moze_urls(
        subcategory=final_subcategory,
        amount=amount,
        store=store,
        name=name,
        date=final_date,
        time=final_time,
        currency=currency,
        note=note
    )

    # 封裝為重導向連結
    moze3_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze3_raw, safe='')}"
    moze_url = f"{REDIRECT_BASE_URL}{urllib.parse.quote(moze_raw, safe='')}"

    description = (
        f"🏪 **類型**: {final_subcategory}\n"
        f"💰 **總額**: {amount} {currency}\n"
        f"🏪 **店家**: {store}\n"
        f"🛒 **商品**: {name if name else '無'}\n"
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
