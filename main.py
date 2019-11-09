# -*- coding: utf-8 -*-
import os
import telebot
from telebot import types
import dictionary
import generators
from flask import Flask, request
import config
import botan


botan_token = config.botan_token
TOKEN = config.TOKEN
url_app = config.url_app
bot = telebot.TeleBot(TOKEN)
dictionary = dictionary.dictionary
server = Flask(__name__)


# Команды
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.clear_step_handler(message)
    bot.send_message(chat_id=message.chat.id,
                     text=(dictionary(
                         message.text,
                         message.from_user.first_name
                     )),
                     parse_mode='HTML',
                     reply_markup=new_menu_button_keyboard())


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.clear_step_handler(message)
    bot.send_message(chat_id=message.chat.id,
                     text=dictionary(message.text),
                     parse_mode='HTML',
                     reply_markup=new_menu_button_keyboard())


@bot.message_handler(commands=['menu'])
def menu_message(message):
    bot.send_chat_action(message.chat.id, action='typing')
    bot.clear_step_handler(message)
    bot.send_message(chat_id=message.chat.id,
                     text=dictionary('menu_title'),
                     reply_markup=menu_keyboard())


# Клавиатуры
def menu_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton
    keyboard.add(
        button(text=dictionary('yes_or_no_button'),
               callback_data='yes_or_no'),
        button(text=dictionary('choose_a_dice_button'),
               callback_data='choose_a_dice'),
        button(text=dictionary('from_0_to_100_button'),
               callback_data='from_0_to_100'),
        button(text=dictionary('min_to_max_button'),
               callback_data='min_to_max'),
        button(text=dictionary('one_from_seq_button'),
               callback_data='one_from_seq'),
        button(text=dictionary('nonrep_numbers_button'),
               callback_data='nonrep_numbers'),
        button(text=dictionary('nonrep_numbers_for_seq_button'),
               callback_data='nonrep_numbers_for_seq'),
        button(text=dictionary('nonrep_numbers_except_button'),
               callback_data='nonrep_numbers_except'),
        button(text=dictionary('nonrep_numbers_except_for_seq_button'),
               callback_data='nonrep_numbers_except_for_seq'),
        button(text=dictionary('share_button'),
               switch_inline_query=dictionary('share_query'))
    )
    return keyboard


def new_menu_button_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(new_menu_button())
    return keyboard


# Кнопки
def new_menu_button():
    button = types.InlineKeyboardButton(
        text=dictionary('menu_button'), callback_data='new_menu')
    return button


def back_to_menu_button(text='<<'):
    button = types.InlineKeyboardButton(
        text=text, callback_data='back_to_menu')
    return button


def continue_button(command):
    button = types.InlineKeyboardButton(
        text=dictionary('continue_button'), callback_data=command)
    return button


def dice_buttons_keyboard(command):
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    button = types.InlineKeyboardButton
    if (command == 'choose_a_dice'):
        menu_button = back_to_menu_button()
    else:
        menu_button = back_to_menu_button('Меню')
    keyboard.add(button(text=4, callback_data='dice 4'),
                 button(text=6, callback_data='dice 6'),
                 button(text=8, callback_data='dice 8'),
                 button(text=12, callback_data='dice 12'),
                 button(text=20, callback_data='dice 20'),
                 menu_button)
    return keyboard


# Хэндлер для inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    command = call.data
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    if (command == 'new_menu'):
        menu_message(message)
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id)
    elif (command == 'back_to_menu'):
        bot.clear_step_handler(message)
        bot.edit_message_text(text=dictionary('menu_title'),
                              chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=menu_keyboard())
    elif (command == 'yes_or_no'):
        bot.edit_message_text(text=generators.yes_or_no(),
                              chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=new_menu_button_keyboard())
        botan.track(token=botan_token,
                    uid=message.chat.id,
                    message=message,
                    name='Да или нет')
    elif (command == 'choose_a_dice'):
        bot.edit_message_text(text=dictionary('how_many_faces'),
                              chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=dice_buttons_keyboard(command))
        botan.track(token=botan_token,
                    uid=message.chat.id,
                    message=message,
                    name='Кубики')
    elif (command == 'change_dice'):
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id)
        bot.send_message(chat_id=chat_id,
                         text=dictionary('how_many_faces'),
                         reply_markup=dice_buttons_keyboard(command))
    elif (command == 'dice 4' or
          command == 'dice 6' or
          command == 'dice 8' or
          command == 'dice 12' or
          command == 'dice 20'):
        dice = command.split(' ')[1]
        buttons_with_dices = types.InlineKeyboardMarkup(row_width=2)
        buttons_with_dices.add(
            types.InlineKeyboardButton(
                text='🎲',
                callback_data=dice
            ),
            types.InlineKeyboardButton(
                text=dictionary('change_dice'),
                callback_data='change_dice'),
            new_menu_button()
        )
        bot.edit_message_text(text=dice + dictionary('facees_of_dice'),
                              chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=buttons_with_dices)
    elif (command in ['4', '6', '8', '12', '20']):
        bot.send_message(
            chat_id=chat_id, text=generators.roll_a_dice(int(command)))
    elif (command == 'from_0_to_100'):
        bot.edit_message_text(text=generators.from_zero_to_hundred(),
                              chat_id=chat_id,
                              message_id=message_id,
                              reply_markup=new_menu_button_keyboard())
        botan.track(token=botan_token,
                    uid=message.chat.id,
                    message=message,
                    name='От 0 до 100')
    elif (command == 'min_to_max'):
        result_of_the_command(message, command, 'enter_min_and_max')
    elif (command == 'enter_min_and_max'):
        instruction_for_the_command(message, command, enter_min_and_max)
    elif (command == 'one_from_seq'):
        result_of_the_command(message, command, 'enter_seq')
    elif (command == 'enter_seq'):
        instruction_for_the_command(message, command, enter_seq)
    elif (command == 'nonrep_numbers'):
        result_of_the_command(message, command, 'enter_number')
    elif (command == 'enter_number'):
        instruction_for_the_command(message, command, enter_number)
    elif (command == 'nonrep_numbers_for_seq'):
        result_of_the_command(message, command, 'enter_number_and_seq')
    elif (command == 'enter_number_and_seq'):
        instruction_for_the_command(message, command, enter_number_and_seq)
    elif (command == 'nonrep_numbers_except'):
        result_of_the_command(message, command, 'enter_number_and_exc')
    elif (command == 'enter_number_and_exc'):
        instruction_for_the_command(message, command, enter_number_and_exc)
    elif (command == 'nonrep_numbers_except_for_seq'):
        result_of_the_command(message, command, 'enter_number_and_exc_and_seq')
    elif (command == 'enter_number_and_exc_and_seq'):
        instruction_for_the_command(
            message, command, enter_number_and_exc_and_seq)


def result_of_the_command(message, command, next_command):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(back_to_menu_button(),
                 continue_button(next_command))
    bot.edit_message_text(text=dictionary(command),
                          chat_id=message.chat.id,
                          message_id=message.message_id,
                          reply_markup=keyboard,
                          parse_mode='HTML')


def instruction_for_the_command(message, command, next_step):
    bot.clear_step_handler(message)
    bot.edit_message_text(text=dictionary(command),
                          chat_id=message.chat.id,
                          message_id=message.message_id,
                          reply_markup=new_menu_button_keyboard(),
                          parse_mode='HTML')
    bot.register_next_step_handler(message, next_step)


def send_result(message, generator, command):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, action='typing')
    try:
        if (not check_comands(message)):
            bot.send_message(chat_id=chat_id,
                             text=generator(message.text),
                             parse_mode='HTML')
    except Exception:
        bot.send_message(chat_id=chat_id,
                         text=dictionary('error'),
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML')
    bot.register_next_step_handler(message, command)


def check_comands(message):
    text = message.text
    if (text == '/start'):
        start(message)
        return True
    elif (text == '/menu'):
        menu_message(message)
        return True
    elif (text == '/help'):
        help(message)
        return True
    return False


def enter_min_and_max(message):
    send_result(message=message,
                generator=generators.from_min_to_max,
                command=enter_min_and_max)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='От мин до макс')


def enter_seq(message):
    send_result(message=message,
                generator=generators.one_from_seq,
                command=enter_seq)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='Один из посл.')


def enter_number(message):
    send_result(message=message,
                generator=generators.nonrepeating_numbers,
                command=enter_number)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='Список чисел')


def enter_number_and_seq(message):
    send_result(message=message,
                generator=generators.nonrepeating_numbers_for_seq,
                command=enter_number_and_seq)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='Числа для списка')


def enter_number_and_exc(message):
    send_result(message=message,
                generator=generators.nonrepeating_numbers_except,
                command=enter_number_and_exc)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='Числа с искл')


def enter_number_and_exc_and_seq(message):
    send_result(message=message,
                generator=generators.nonrepeating_numbers_except_for_seq,
                command=enter_number_and_exc_and_seq)
    botan.track(token=botan_token,
                uid=message.chat.id,
                message=message,
                name='Список с искл.')

# Вебхук
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=url_app + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
