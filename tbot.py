import telebot
import time
import subprocess
import re
import datetime
import json
import webbrowser
from termcolor import colored
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def autoketik(autoketik):
    for char in autoketik:
        print(char, end='', flush=True)
        time.sleep(0.03)

def send_typing_action(bot, chat_id):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)

def log_chat_history(message):
    username = message.from_user.username
    user_message = message.text
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(colored(f"\n\n[#] LOGS [#]", 'light_green'))
    print(colored(f"[#] TIME: {timestamp}", 'light_blue'))
    print(colored(f"[#] USERNAME: {username}", 'light_blue'))
    print(colored(f"[#] MESSAGE: {user_message}", 'light_blue'))

def log_callback_data(call):
    username = call.from_user.username
    callback_data = call.data
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(colored(f"\n\n[#] CALLBACK [#]", 'light_green'))
    print(colored(f"[#] TIME: {timestamp}", 'light_blue'))
    print(colored(f"[#] USERNAME: {username}", 'light_blue'))
    print(colored(f"[#] CALLBACK DATA: {callback_data}", 'light_blue'))

def save_token(token):
    with open('bot_token.json', 'w') as file:
        json.dump({"token": token}, file)

def load_token():
    try:
        with open('bot_token.json', 'r') as file:
            data = json.load(file)
            return data['token']
    except FileNotFoundError:
        return None

def create_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("SCRIPT", url="https://github.com/rizkykianadji/tbot"),
               InlineKeyboardButton("YOUTUBE", url="https://youtube.com/@rizkykianadji"))
    return markup

def start_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        log_chat_history(message)
        send_typing_action(bot, message.chat.id)
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Hello im your telegram bot click /help for command list", reply_markup=create_markup())

    @bot.message_handler(commands=['help'])
    def send_help(message):
        log_chat_history(message)
        send_typing_action(bot, message.chat.id)
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Avaliable Commands:\n/start - Start bot function\n/help - help\n/mp3 <youtube_url> - Download youtube video to audio\n/mp4 <youtube_url> - Download youtube video to mp4", reply_markup=create_markup())

    def youtube_to_mp4(url):
        try:
            subprocess.run(["youtube-dl", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4", "-o", "output.mp4", url], check=True)
            return "Download Success."
        except subprocess.CalledProcessError as e:
            return f"Something Error: {e.output.decode()}"

    def youtube_to_mp3(url):
        try:
            subprocess.run(["youtube-dl", "-x", "--audio-format", "mp3", "-o", "output.mp3", url], check=True)
            return "Download Success."
        except subprocess.CalledProcessError as e:
            return f"Something Error: {e.output.decode()}"

    @bot.message_handler(commands=['mp4'])
    def mp4_command(message):
        log_chat_history(message)
        send_typing_action(bot, message.chat.id)
        url = message.text.split(' ', 1)[1]
        if re.match(r'^https://www.youtube.com/watch\?v=[\w-]+$', url):
            bot.reply_to(message, youtube_to_mp4(url))
        else:
            bot.reply_to(message, "INVALID YOUTUBE URL.")

    @bot.message_handler(commands=['mp3'])
    def mp3_command(message):
        log_chat_history(message)
        send_typing_action(bot, message.chat.id)
        url = message.text.split(' ', 1)[1]
        if re.match(r'^https://www.youtube.com/watch\?v=[\w-]+$', url):
            bot.reply_to(message, youtube_to_mp3(url))
        else:
            bot.reply_to(message, "INVALID YOUTUBE URL.")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        log_chat_history(message)
        send_typing_action(bot, message.chat.id)
        bot.send_message(message.chat.id, message.text, reply_markup=create_markup())

    autoketik(colored("BOT SESSION STARTED! ...", 'light_green'))
    bot.polling()

def before_start_bot():
    title = """
████████ ██████   ██████  ████████ 
   ██    ██   ██ ██    ██    ██    
   ██    ██████  ██    ██    ██    
   ██    ██   ██ ██    ██    ██    
   ██    ██████   ██████     ██    

[99] GITHUB: https://github.com/rizkykianadji
[96] YOUTUBE: https://youtube.com/@rizkykianadji
"""
    print(colored(title, 'light_cyan'))
    autoketik(colored("THANKS FOR USED THIS SCRIPT!, ITS FREE TO RECODE! DON'T FORGET PUT A STAR DUDE!!\n", 'light_green'))
    time.sleep(1)
    autoketik(colored("[01] START BOT\n", 'light_blue'))
    autoketik(colored("[02] RESUME SESSION\n", 'light_blue'))
    autoketik(colored("[03] EXIT\n\n", 'light_red'))

    pilih = input(colored("> ", 'light_green'))
    if pilih == "1":
        choose = input(colored("Insert token: ", 'light_green'))
        save_token(choose)
        start_bot(choose)
    elif pilih == "2":
        token = load_token()
        if token:
            start_bot(token)
        else:
            print(colored("[!] ERROR NO SESSION FOUND [!]", 'light_red'))
            before_start_bot()
    elif pilih == "3":
        print(colored("[!] PROGRAM ENDED [!]", 'light_red'))
    elif pilih == "99":
        webbrowser.open("https://github.com/rizkykianadji")
        before_start_bot()
    elif pilih == "96":
        webbrowser.open("https://youtube.com/@rizkykianadji")
        before_start_bot()
    else:
        print(colored("[!] INVALID [!]", 'light_red'))
        before_start_bot()

if __name__ == "__main__":
    before_start_bot()
            
