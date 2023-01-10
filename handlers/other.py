from aiogram import types

#список команд
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Let's start!"),
        types.BotCommand("stop", "If entered incorrectly"),
        types.BotCommand("help", "Do you have questions?")

    ])