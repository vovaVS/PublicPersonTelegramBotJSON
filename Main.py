from cgitb import text
from collections import UserDict
from dataclasses import replace
from distutils.command.config import config
from email import message
from unicodedata import name
from telebot import types
import telebot
import os
import fnmatch
import json
import datetime

name_public = []
name_users = []
bot = telebot.TeleBot('5544156373:AAGTKM87LOZR3EcpwdzBtu0QMPOVl9Vktao')

@bot.message_handler(commands=['start'])
def start(message):
    menu_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить группу")
    btn2 = types.KeyboardButton("Открыть группу")
    menu_button.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Приветствую вас " + '['+message.from_user.username+']', reply_markup=menu_button)
  
@bot.message_handler(content_types=["text"])
def funct_button(message):
    global taskname
    if message.text == "Добавить группу":
             bot.send_message(message.chat.id, text="Введите номер(имя) группы")
             bot.register_next_step_handler(message, create_json_is_public)
    if message.text == "Открыть группу":
        class_list_public(message)   
    if message.text == "Выйти и сохранить":
        start(message)    
        clear_cash()    
    for u in range(len(name_public)):
         if message.text == name_public[u]: 
           global jsons
           jsons = name_public[u]
           list_user_json(message)
    if message.text == "Добавить участника":
            bot.send_message(message.chat.id, text="Введите имя участника. Примечание: имя участника должно быть из латинских букв и с нижним подчеркиванием. Пример: Vova_Chernov")
            bot.register_next_step_handler(message, settings_json)

    for i in range(len(name_users)):
         if message.text == name_users[i]:
          taskname = name_users[i]
          actions_on_participants = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn3 = types.KeyboardButton("Присутствующий")
          btn4 = types.KeyboardButton("Отсутствующий")
          btn5 = types.KeyboardButton("Выйти и сохранить")
          actions_on_participants.add(btn3, btn4, btn5)
          bot.send_message(message.chat.id, text="Выберите действие над участником", reply_markup=actions_on_participants)      
    participants_presence(message)
    absence_of_participante(message)
    
def create_json_is_public(message):
     f = open(message.text+".json", "x") 
     f.write("{}")
     f.close
     bot.send_message(message.chat.id, text="Группа под номером(названием) "+ message.text + " создана.")

def class_list_public(message):
     num_files = len(fnmatch.filter(os.listdir('.'),'*.json'))         
     menu_button_list = types.ReplyKeyboardMarkup(resize_keyboard=True)           
     menu_button_list.add(types.KeyboardButton("Выйти и сохранить"))

     if num_files <= 0:


        bot.send_message(message.chat.id, text="Список групп пуст")
     else: 
        for f in os.listdir(r"C:\Users\constVova\Desktop\PythonTelegramBotListUsers"):
         if fnmatch.fnmatch(f, '*.json'):
            replace_name = f.replace(".json", "")
            menu_button_list.add(types.KeyboardButton(replace_name))
            name_public.append(replace_name)
            bot.send_message(message.chat.id, text="Группа: " + replace_name, reply_markup=menu_button_list)
         continue     

@bot.message_handler(content_types=["text"])
def settings_json(message):
     with open(str(jsons)+".json", encoding='utf8') as s:
      json_decoded = json.load(s)
     json_decoded[message.text] = [] 

     with open(str(jsons)+".json", 'w') as json_file:
      json.dump(json_decoded, json_file, sort_keys=True, ensure_ascii=False, indent=4)
     bot.send_message(message.chat.id, text="Участник под именем " + message.text + " добавлен в группу: " + jsons+'. ' + "Нажмите кнопку <<Выйти и сохранить>> для  того, чтобы изменения применились")
 
@bot.message_handler(content_types=["text"])
def list_user_json(message):
    list_users_json = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    btn1 = types.KeyboardButton("Добавить участника")
    btn2 = types.KeyboardButton("Выйти и сохранить")
    list_users_json.add(btn1, btn2)

    with open(str(jsons)+".json", encoding='utf8') as s:
     json_decoded = json.load(s)         
    for name_array, n in json_decoded.items():
            list_users_json.add(types.KeyboardButton(name_array))
            name_users.append(name_array)
    bot.send_message(message.chat.id, text="Список участников открыт:", reply_markup=list_users_json)

@bot.message_handler(content_types=["text"])
def absence_of_participante(message):
     if message.text == "Отсутствующий":
        with open(str(jsons)+".json", encoding='utf8') as s:
         json_decoded = json.load(s)
         today = datetime.datetime.today()
         dataCreate = today.strftime("%d-%m-%Y")
         json_decoded[taskname].append(str(dataCreate)+":No")

         with open(str(jsons)+".json", 'w') as json_file:
          json.dump(json_decoded, json_file, sort_keys=True, ensure_ascii=False, indent=4)
         bot.send_message(message.chat.id, text="Участник " + '['+taskname+'] '+ "отмечен как - отсутствующий")

@bot.message_handler(content_types=["text"])
def participants_presence(message):
    if message.text == "Присутствующий":
        with open(str(jsons)+".json", encoding='utf8') as s:
         json_decoded = json.load(s)
         today = datetime.datetime.today()
         dataCreate = today.strftime("%d-%m-%Y")
         json_decoded[taskname].append(str(dataCreate)+":Yes")

        with open(str(jsons)+".json", 'w') as json_file:
         json.dump(json_decoded, json_file, sort_keys=True, ensure_ascii=False, indent=4)
         bot.send_message(message.chat.id, text="Участник "+ '['+taskname+'] '+ " отмечен как - присутствующий")

def clear_cash():
    name_users.clear()
    name_public.clear()

bot.infinity_polling()





