import telebot
from telebot import types

TOKEN = "7507029019:AAEZKgTcidprRP79kQzUu9QLGPQA-8gtVr0"
CHANNEL_USERNAME = "@w1nst0n_sunsh1ne"

bot = telebot.TeleBot(TOKEN)


def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📢 Подписаться на канал",
            url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "✅ Проверить подписку",
            callback_data="check"
        )
    )

    bot.send_message(
        message.chat.id,
        "👋 Привет!\n\n"
        "Подпишись на нашего спонсора, чтобы получить полный доступ 🔒",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(c):
    if check_subscription(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ Подписка подтверждена")
        bot.send_message(c.message.chat.id, "🔓 Доступ открыт!")
    else:
        bot.answer_callback_query(c.id, "❌ Ты не подписан")
        bot.send_message(c.message.chat.id, "⚠️ Подпишись и попробуй снова")


bot.polling()
