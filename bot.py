import telebot 
import configure
from telebot import types 
from firebase_setting import ref
bot = telebot.TeleBot(configure.config['token'])
 
@bot.message_handler(commands=['info'])
def get_info(message):
    name_= message.from_user.username
    id_ = message.from_user.id
    data = { str(name_ ): str(id_)}
    ref.push(data)
    
    

 
 
 
@bot.message_handler(commands=['start'])
def button(message):
    
    name_= message.from_user.username
    id_ = message.from_user.id
    data = { str(name_ ): str(id_)}
    ref.push(data)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Да' , callback_data = 'yes_start')
    item2 = types.InlineKeyboardButton('Нет', callback_data = 'no_start')
    markup.add(item, item2)
 
    bot.send_message(message.chat.id, 'Ты готов приступить к подбору ноутбука?', reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    small = types.InlineKeyboardButton('300$ - 500$', callback_data='small_price')
    medium = types.InlineKeyboardButton('500$ - 1000$', callback_data='medium_price')
    large = types.InlineKeyboardButton('1000$ - no limit$', callback_data='medium_price')
        
    markup.row(large)
    markup.add(small, medium)
    
    msg = bot.send_message(call.message.chat.id, 'Какой у тебя бюджет ?', reply_markup=markup)
    
    
    

    if call.data == 'yes_start':
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')            
        bot.send_message(call.message.chat.id, 'Хорошо, давай начнем')
        bot.register_next_step_handler(msg, budget) 

    elif call.data == 'no_start':
        bot.send_message(call.message.chat.id, 'Ладно')
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

    
    

def budget(message):
 
    # results: dict = {
    # 'budget': '',
    # 'processor' : '',
    # 'graphics_card_price' : '',
    # 'graphics_card_brand' : '',
    # 'board' : '',
    # 'memory' : '',
    # 'power_unit' : '',
    # 'ssd' : '',
    # 'hdd' : '',
    # 'frame' : ''
    # }   
 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    intel = types.InlineKeyboardButton('Intel')
    amd = types.InlineKeyboardButton('Amd')

    markup.add(intel, amd)
    
    msg = bot.send_message(message.from_user.id, 'Какой процессор предпочитаете ? ', reply_markup = markup)    
    
         
    if message.text == '300$ - 500$' :
        bot.send_message(message.chat.id, 'GOOD')
    elif message.text == '500$ - 1000$' :
        bot.send_message(message.chat.id, 'GOOD 2')
    elif message.text == '1000$ - no limit$' :
        bot.send_message(message.chat.id, 'GOOD 3')
        
    bot.register_next_step_handler(msg, processor_brand) 

    

     

def processor_brand(message):


     
    
    if message.text == "Intel":
        markup_intel = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_intel = types.InlineKeyboardButton('Core i5')
        medium_intel = types.InlineKeyboardButton('Core i7')
        good_intel = types.InlineKeyboardButton('Core i9')

        markup_intel.row(good_intel)
        markup_intel.add(bad_intel, medium_intel)
        msg_intel = bot.send_message(message.from_user.id, 'Какую модель процессора хотели бы ? ', reply_markup = markup_intel)

        bot.register_next_step_handler(msg_intel, processor_model)  
    elif message.text == "Amd":

        markup_amd = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_amd = types.InlineKeyboardButton('Ryzen 5')
        medium_amd = types.InlineKeyboardButton('Ryzen 7')
        good_amd = types.InlineKeyboardButton('Ryzen 9')

        markup_amd.row(good_amd)
        markup_amd.add(bad_amd, medium_amd)

        msg_amd = bot.send_message(message.from_user.id, 'Какую модель процессора хотели бы ? ', reply_markup = markup_amd)
        bot.register_next_step_handler(msg_amd, processor_model)  
    

    
def processor_model(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетная')
    medium = types.InlineKeyboardButton('Что-то средняя')
    good = types.InlineKeyboardButton('Дорогая')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, 'Что насчет видеокарты  ?'  , reply_markup = markup)
     
    
    if message.text == "Core i5":
        pass
    elif message.text == "Core i7":
        pass
    elif message.text == "Core i9":
        pass
    elif message.text == "Ryzen 5":
            pass
    elif message.text == "Ryzen 7":
        pass
    elif message.text == "Ryzen 9":
        pass
    
    bot.register_next_step_handler(msg, graphics_card)    


def graphics_card(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    small = types.InlineKeyboardButton('8')
    medium = types.InlineKeyboardButton('16')
    large = types.InlineKeyboardButton('Больше 16')

    markup.add(small, medium, large)
    
    msg = bot.send_message(message.from_user.id, 'Сколько ОЗУ предпочитаете ? ', reply_markup = markup)

    if message.text == "Бюджетная":
            pass
    elif message.text == "Дорогая":
        pass
    elif message.text == "Что-то средняя":
        pass

    bot.register_next_step_handler(msg, ram)    


def ram(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    hdd = types.InlineKeyboardButton('HHD')
    ssd = types.InlineKeyboardButton('SSD')

    markup.add(hdd, ssd)
    
    msg = bot.send_message(message.from_user.id, 'HDD or SSD', reply_markup = markup)
     
    
    if message.text == "8":
        pass
    elif message.text == "16":
        pass
    elif message.text == "Больше 16":
        pass

    bot.register_next_step_handler(msg, start_5)  
    
  

def start_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('216 гб')
    medium = types.InlineKeyboardButton('512 гб')
    good = types.InlineKeyboardButton('1 тб')

    markup.row(good)
    markup.add(bad, medium)
    
    
    msg = bot.send_message(message.from_user.id, 'Что насчет памяти ?', reply_markup = markup)
     
    
    if message.text == "HDD":
        pass
    elif message.text == "SSD":
        pass

    bot.register_next_step_handler(msg, start_6_memory)

def start_6_memory(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогой')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, 'Что насчет цены ssd or hdd ?'  , reply_markup = markup)
     
    
    if message.text == "216 гб":
        pass
    elif message.text == "512 гб":
        pass
    elif message.text == "1 ТБ":
        pass
    
    bot.register_next_step_handler(msg, start_6_price)    

def start_6_price(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогой')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, 'Что насчет блока питания ?'  , reply_markup = markup)
     
    if message.text == "Бюджетная":
            pass
    elif message.text == "Дорогая":
        pass
    elif message.text == "Что-то средняя":
        pass
    
    bot.register_next_step_handler(msg, pc_power)        
    
    
    
    
def pc_power(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогой')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, 'Что насчет  корпуса ?'  , reply_markup = markup)
     
    
    if message.text == "Бюджетный":
        pass
    elif message.text == "Дорогой":
        pass
    elif message.text == "Что-то среднее":
        pass
    
    bot.register_next_step_handler(msg, pc_case)    
    bot.send_message(message.chat.id, 'Владик пидрила')

def pc_case(message):
    pass
# Корпус






bot.polling(none_stop = True, interval = 0)
