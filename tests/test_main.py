import asyncio
import pytest
import discord
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import utils
from main import date_autocomplete, time_autocomplete, ExpenseModal, expense

def test_date_autocomplete_empty_query(monkeypatch):
    # Mock get_taipei_now to return a fixed date (Wednesday)
    fixed_now = datetime(2026, 5, 20, 12, 0, tzinfo=utils.TAIPEI_TZ) # 2026.05.20 is Wednesday (weekday 2)
    monkeypatch.setattr(utils, "get_taipei_now", lambda: fixed_now)
    monkeypatch.setattr("main.get_taipei_now", lambda: fixed_now)

    # We need to run the async function
    loop = asyncio.get_event_loop()
    choices = loop.run_until_complete(date_autocomplete(None, ""))

    # We expect 8 choices: 1 custom + 7 days
    assert len(choices) == 8
    
    # Check the first choice (custom option)
    assert choices[0].name == "📅 自訂日期 (手動輸入)"
    assert choices[0].value == "自訂"

    # Check that the days are correctly calculated backwards from Wednesday
    # Wednesday, Tuesday, Monday, Sunday, Saturday, Friday, Thursday
    expected_days = [
        ("Wed", "2026.05.20"),
        ("Tue", "2026.05.19"),
        ("Mon", "2026.05.18"),
        ("Sun", "2026.05.17"),
        ("Sat", "2026.05.16"),
        ("Fri", "2026.05.15"),
        ("Thu", "2026.05.14"),
    ]
    for idx, (day_label, date_str) in enumerate(expected_days):
        choice = choices[idx + 1]
        assert choice.value == date_str
        assert day_label in choice.name

def test_date_autocomplete_filtered_query(monkeypatch):
    fixed_now = datetime(2026, 5, 20, 12, 0, tzinfo=utils.TAIPEI_TZ)
    monkeypatch.setattr(utils, "get_taipei_now", lambda: fixed_now)
    monkeypatch.setattr("main.get_taipei_now", lambda: fixed_now)

    loop = asyncio.get_event_loop()
    
    # Filter by specific string (e.g. "Mon" or "18")
    choices = loop.run_until_complete(date_autocomplete(None, "Mon"))
    
    # Should include "自訂" and the matched day "Mon"
    assert len(choices) == 2
    assert choices[0].value == "自訂"
    assert choices[1].value == "2026.05.18"
    assert "Mon" in choices[1].name

def test_time_autocomplete_empty_query(monkeypatch):
    fixed_now = datetime(2026, 5, 20, 14, 30, tzinfo=utils.TAIPEI_TZ)
    monkeypatch.setattr(utils, "get_taipei_now", lambda: fixed_now)
    monkeypatch.setattr("main.get_taipei_now", lambda: fixed_now)

    loop = asyncio.get_event_loop()
    choices = loop.run_until_complete(time_autocomplete(None, ""))

    # We expect: 
    # 1. 自訂
    # 2. 現在 (14:30)
    # 3. 30分鐘前 (14:00)
    # 4. 60分鐘前 (13:30)
    # 5. 整點 x 5: 14:00, 13:00, 12:00, 11:00, 10:00
    # Let's count them and verify
    assert len(choices) > 0
    
    # Check custom option
    assert choices[0].value == "自訂"
    
    # Check current time
    assert choices[1].value == "14:30"
    
    # Check 30 mins ago
    assert choices[2].value == "14:00"
    
    # Check 60 mins ago
    assert choices[3].value == "13:30"

    # Check some of the hour intervals
    hour_values = [c.value for c in choices[4:9]]
    assert "14:00" in hour_values
    assert "13:00" in hour_values
    assert "10:00" in hour_values

def test_time_autocomplete_filtered_query(monkeypatch):
    fixed_now = datetime(2026, 5, 20, 14, 30, tzinfo=utils.TAIPEI_TZ)
    monkeypatch.setattr(utils, "get_taipei_now", lambda: fixed_now)
    monkeypatch.setattr("main.get_taipei_now", lambda: fixed_now)

    loop = asyncio.get_event_loop()
    choices = loop.run_until_complete(time_autocomplete(None, "13:30"))

    # Should only return matches containing "13:30"
    for choice in choices:
        assert "13:30" in choice.name or "13:30" in choice.value


class MockInteractionResponse:
    def __init__(self):
        self.sent_messages = []
        self.sent_modals = []

    async def send_message(self, content=None, *, embed=None, ephemeral=False):
        self.sent_messages.append({
            "content": content,
            "embed": embed,
            "ephemeral": ephemeral
        })

    async def send_modal(self, modal):
        self.sent_modals.append(modal)


class MockUser:
    def __init__(self):
        self.name = "TestUser"
        self.id = 123456789


class MockInteraction:
    def __init__(self):
        self.response = MockInteractionResponse()
        self.user = MockUser()


def test_expense_modal_validation_and_submit():
    # Test valid submission
    interaction = MockInteraction()
    modal = ExpenseModal(
        interaction=interaction,
        amount=150,
        store="Starbucks",
        name="Latte",
        date="2026.05.20",
        time="14:30",
        currency="TWD",
        note="Afternoon tea",
        subcategory_val="飲料",
        needs_category=True,
        needs_date=True,
        needs_time=True
    )
    # Simulate user input into TextInput fields
    modal.category_input._value = "Coffee"
    modal.date_input._value = "2026.05.20"
    modal.time_input._value = "14:30"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(modal.on_submit(interaction))

    assert len(interaction.response.sent_messages) == 1
    msg = interaction.response.sent_messages[0]
    assert msg["content"] is None  # It sends an embed, not plain text
    embed = msg["embed"]
    assert embed is not None
    assert embed.title == "記帳確認"
    assert "Coffee" in embed.description
    assert "150 TWD" in embed.description
    assert "Starbucks" in embed.description
    assert "Latte" in embed.description
    assert "2026.05.20 14:30" in embed.description
    assert "Afternoon tea" in embed.description


def test_expense_modal_invalid_date():
    interaction = MockInteraction()
    modal = ExpenseModal(
        interaction=interaction,
        amount=150,
        store="Starbucks",
        name="Latte",
        date="2026.05.20",
        time="14:30",
        currency="TWD",
        note="Afternoon tea",
        subcategory_val="飲料",
        needs_category=False,
        needs_date=True,
        needs_time=False
    )
    modal.date_input._value = "2026-05-20"  # Invalid format (should be YYYY.MM.dd)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(modal.on_submit(interaction))

    assert len(interaction.response.sent_messages) == 1
    msg = interaction.response.sent_messages[0]
    assert "日期格式錯誤" in msg["content"]
    assert msg["ephemeral"] is True


def test_expense_modal_invalid_time():
    interaction = MockInteraction()
    modal = ExpenseModal(
        interaction=interaction,
        amount=150,
        store="Starbucks",
        name="Latte",
        date="2026.05.20",
        time="14:30",
        currency="TWD",
        note="Afternoon tea",
        subcategory_val="飲料",
        needs_category=False,
        needs_date=False,
        needs_time=True
    )
    modal.time_input._value = "2:30 PM"  # Invalid format (should be HH:mm)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(modal.on_submit(interaction))

    assert len(interaction.response.sent_messages) == 1
    msg = interaction.response.sent_messages[0]
    assert "時間格式錯誤" in msg["content"]
    assert msg["ephemeral"] is True


def test_expense_command_needs_modal_category():
    interaction = MockInteraction()
    subcategory = discord.app_commands.Choice(name="其他", value="其他")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        expense.callback(
            interaction=interaction,
            subcategory=subcategory,
            amount=200,
            store="SomeStore",
            date="2026.05.20",
            time="14:30"
        )
    )
    
    assert len(interaction.response.sent_modals) == 1
    modal = interaction.response.sent_modals[0]
    assert modal._needs_category is True
    assert modal._needs_date is False
    assert modal._needs_time is False


def test_expense_command_needs_modal_date():
    interaction = MockInteraction()
    subcategory = discord.app_commands.Choice(name="午餐", value="午餐")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        expense.callback(
            interaction=interaction,
            subcategory=subcategory,
            amount=200,
            store="SomeStore",
            date="自訂",
            time="14:30"
        )
    )
    
    assert len(interaction.response.sent_modals) == 1
    modal = interaction.response.sent_modals[0]
    assert modal._needs_category is False
    assert modal._needs_date is True
    assert modal._needs_time is False


def test_expense_command_needs_modal_time():
    interaction = MockInteraction()
    subcategory = discord.app_commands.Choice(name="午餐", value="午餐")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        expense.callback(
            interaction=interaction,
            subcategory=subcategory,
            amount=200,
            store="SomeStore",
            date="2026.05.20",
            time="自訂"
        )
    )
    
    assert len(interaction.response.sent_modals) == 1
    modal = interaction.response.sent_modals[0]
    assert modal._needs_category is False
    assert modal._needs_date is False
    assert modal._needs_time is True


def test_expense_command_direct_send():
    interaction = MockInteraction()
    subcategory = discord.app_commands.Choice(name="午餐", value="午餐")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        expense.callback(
            interaction=interaction,
            subcategory=subcategory,
            amount=200,
            store="McDonalds",
            name="Burger",
            date="2026.05.20",
            time="12:30",
            currency="TWD",
            note="Lunch time"
        )
    )
    
    assert len(interaction.response.sent_messages) == 1
    msg = interaction.response.sent_messages[0]
    embed = msg["embed"]
    assert embed is not None
    assert embed.title == "記帳確認"
    assert "午餐" in embed.description
    assert "200 TWD" in embed.description
    assert "McDonalds" in embed.description
    assert "Burger" in embed.description
    assert "2026.05.20 12:30" in embed.description
    assert "Lunch time" in embed.description
