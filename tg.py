import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
from threading import Thread

# Установите ваш токен от BotFather
API_TOKEN = "7346569102:AAEh4S1kwJOVn6HAN25XuSlIWYz9YxlPUUk"
CHANNEL_USERNAME = "kussokofficial"  # Имя пользователя вашего канала (без https://t.me/)
FILM_LINK = "https://t.me/+RTSVbES7UdQ5NzBi"  # Ссылка на фильм или сериал

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    try:
        # Проверяем подписку пользователя
        status = bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id).status
        
        if status in ['member', 'administrator', 'creator']:
            # Если подписан, отправляем сообщение с доступом к фильму
            bot.send_message(
                message.chat.id,
                f"*Ваш фильм или сериал уже Вас ждёт🤗*\n\n[Перейти к фильму или сериалу]({FILM_LINK})",
                parse_mode="Markdown"
            )
        else:
            # Если не подписан, отправляем сообщение с кнопкой
            markup = InlineKeyboardMarkup()
            check_button = InlineKeyboardButton(
                text="Проверить подписку",
                callback_data="check_subscription"
            )
            markup.add(check_button)

            bot.send_message(
                message.chat.id,
                f"*Подпишись на спонсора, чтобы узнать фильм или сериал😉*\n\n[Подписаться на канал](https://t.me/{CHANNEL_USERNAME})",
                parse_mode="Markdown",
                reply_markup=markup
            )
    except Exception as e:
        # В случае ошибки, например, если пользователь заблокировал бота
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при проверке подписки. Попробуйте позже."
        )
        print(f"Ошибка: {e}")

# Обработчик нажатия на кнопку "Проверить подписку"
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    try:
        # Проверяем подписку
        status = bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id).status
        
        if status in ['member', 'administrator', 'creator']:
            # Если подписан, обновляем сообщение, удаляя кнопку
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(
                call.message.chat.id,
                f"*Ваш фильм или сериал уже Вас ждёт🤗*\n\n[Перейти к фильму или сериалу]({FILM_LINK})",
                parse_mode="Markdown"
            )
        else:
            # Если не подписан, отправляем уведомление
            bot.answer_callback_query(
                call.id,
                text="Вы ещё не подписались на канал. Подпишитесь, чтобы продолжить!",
                show_alert=True
            )
    except Exception as e:
        # В случае ошибки, отправляем уведомление
        bot.answer_callback_query(
            call.id,
            text="Произошла ошибка при проверке подписки. Попробуйте позже.",
            show_alert=True
        )
        print(f"Ошибка: {e}")

# Удаляем активный Webhook перед запуском polling
bot.remove_webhook()

if __name__ == "__main__":
    # Запускаем Flask-сервер в фоновом режиме
    Thread(target=run).start()
    print("Бот запущен...")
    bot.infinity_polling()
