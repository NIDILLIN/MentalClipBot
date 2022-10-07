from aiogram import Dispatcher, types
from Server.exceptions.bot_blocked import reg_block
from Server.handlers.commands import register_notes, register_common_cmd
from Server.handlers.commands.article import register_creating_telegraph_acc, register_article_creating, register_my_accounts
from Server.handlers.commands.article.profile.my_profile import register_my_profile
# from Server.handlers.fast_note.fast_note import register_fast_note


async def register_all(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("telegraph_section", "СЕКЦИЯ TELEGRAPH"),
            types.BotCommand("new_article", "Создать новую статью"),
            types.BotCommand("my_articles", "Список моих статей"),
            types.BotCommand("my_groups", "Список моих групп"),
            types.BotCommand("my_accounts", "Список моих аккаунтов"),
            types.BotCommand("create_account", "Создать telegraph аккаунт"), 
            types.BotCommand("profile", "Мой профиль"),
            types.BotCommand("notes_section", "СЕКЦИЯ ЗАМЕТОК"),
        ]
    )
    reg_block(dp)
    register_common_cmd(dp)
    register_notes(dp)
    register_creating_telegraph_acc(dp)
    register_article_creating(dp)
    register_my_accounts(dp)
    register_my_profile(dp)