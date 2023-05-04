from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)
bot = telebot.TeleBot("6107040954:AAFEHayVPz39VHKYsiJseEkXpM9bMAdDOEk")

@app.route('/bot', methods=['POST'])
def bot_handler():
    # принимаем запрос от Telegram и передаем его боту
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "ok", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(
        text="Kanalga obuna bo'ling", url="https://t.me/kunuzofficial")
    calculator_button = InlineKeyboardButton(
        text="Kalkulyator", callback_data="calculator")
    keyboard.add(url_button, calculator_button)

    bot.reply_to(message, "Assalomu aleykum.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "calculator":
        keyboard = InlineKeyboardMarkup()
        button_six_months = InlineKeyboardButton(
            text="6 oy", callback_data="six_months")
        button_twelve_months = InlineKeyboardButton(
            text="12 oy", callback_data="twelve_months")
        keyboard.add(button_six_months, button_twelve_months)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Davomiyligi qancha muddatga olasiz?", reply_markup=keyboard)
    elif call.data == "six_months":
        bot.send_message(call.message.chat.id, "Summani kiriting:")
        bot.register_next_step_handler(call.message, calculate_six_months)
    elif call.data == "twelve_months":
        bot.send_message(call.message.chat.id, "Summani kiriting:")
        bot.register_next_step_handler(call.message, calculate_twelve_months)


def calculate_six_months(message):
    try:
        amount = float(message.text)
        amount_with_interest = amount * 1.20 * 1.26 / 6
        installment = round(amount_with_interest / 1, 2)
        formatted_installment = "{:,.2f}".format(installment).replace(",", " ")
        bot.reply_to(
            message, f"6 oylik tolov {formatted_installment} sum.\n\nBosh menuga qaytish uchun /start ni bosing")
        bot.send_message(message.chat.id, "⬅️ Orqaga qaytish uchun", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data='calculator')]
        ]))
    except ValueError:
        bot.reply_to(message, "Yaroqli raqam kiriting.")


def calculate_twelve_months(message):
    try:
        amount = float(message.text)
        amount_with_interest = amount * 1.20 * 1.44 / 12
        installment = round(amount_with_interest / 1, 2)
        formatted_installment = "{:,.2f}".format(installment).replace(",", " ")
        bot.reply_to(
            message, f"12 oylik tolov {formatted_installment} sum.\n\nBosh menuga qaytish uchun /start ni bosing")
        bot.send_message(message.chat.id, "⬅️ Orqaga qaytish uchun", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data='calculator')]
        ]))
    except ValueError:
        bot.reply_to(message, "Yaroqli raqam kiriting.")


bot.polling(none_stop=True)