import telebot 
import configure
from telebot import types 
from firebase_setting import ref
from PIL import Image
from sql.sqlConnect import *


bot = telebot.TeleBot(configure.config['token'])
 
@bot.message_handler(commands=['info'])
def get_info(message):
    name_= message.from_user.username
    id_ = message.from_user.id
    data = { str(name_ ): str(id_)}
    ref.push(data)
    
    
 
 
 
@bot.message_handler(commands=['start'])
def button(message):
    clean_data(message.from_user.id)
    name_= message.from_user.username
    id_ = message.from_user.id
    data = { str(name_ ): str(id_)}
    ref.push(data)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Да' , callback_data = 'yes_start')
    item2 = types.InlineKeyboardButton('Нет', callback_data = 'no_start')
    markup.add(item, item2)
 
    bot.send_message(message.chat.id, 'Ты готов приступить к подбору компьютера?', reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    
    
    
    
    insert_teleram_id(call.from_user.id)
    processor_img = Image.open(r'D:\projects\Diplom\images\intel-vs-amd_large.jpg')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    intel = types.InlineKeyboardButton('Intel')
    amd = types.InlineKeyboardButton('Amd')

    markup.add(intel, amd)
    
    msg = bot.send_photo(call.from_user.id, processor_img ,'Какой процессор предпочитаете ? ', reply_markup = markup)     
 

    if call.data == 'yes_start':
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')  
        bot.register_next_step_handler(msg, processor_brand) 
          
        # bot.send_message(call.chat.id, 'Хорошо, давай начнем')


    elif call.data == 'no_start':
        bot.send_message(call.message.chat.id, 'Ладно')
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

    


def processor_brand(message):

    insert_data(message.from_user.id, message.text, 'processor_brand')

     
    
    if message.text == "Intel":
        intel_img = Image.open(r'D:\projects\Diplom\images\intel.jpg')

        markup_intel = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_intel = types.InlineKeyboardButton('Core i5 (4 500 - 9 900)грн')
        medium_intel = types.InlineKeyboardButton('Core i7 (8 848 - 14 579)грн')
        good_intel = types.InlineKeyboardButton('Core i9 (12 253 - 22 522)грн')

        markup_intel.row(good_intel)
        markup_intel.add(bad_intel, medium_intel)
        msg_intel = bot.send_photo(message.from_user.id,intel_img ,'Какую модель процессора хотели бы ? ', reply_markup = markup_intel)

        bot.register_next_step_handler(msg_intel, processor_model)  
    elif message.text == "Amd":

        amd_img = Image.open(r'D:\projects\Diplom\images\amd.jpg')

        markup_amd = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_amd = types.InlineKeyboardButton('Ryzen 5 (6 200 - 9 400)')
        medium_amd = types.InlineKeyboardButton('Ryzen 7 (9 099 - 12 399)')
        good_amd = types.InlineKeyboardButton('Ryzen 9 (14 939 - 22 899)')

        markup_amd.row(good_amd)
        markup_amd.add(bad_amd, medium_amd)

        msg_amd = bot.send_photo(message.from_user.id, amd_img, 'Какую модель процессора хотели бы ? ', reply_markup = markup_amd)
        bot.register_next_step_handler(msg_amd, processor_model)  
    


def processor_model(message):
    bot.send_message(message.chat.id, 'Выберите процессор !')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)

    if "Core i5" in message.text :

 
        msg = bot.send_message(message.chat.id, ' 1.[Core i5-12600K](https://telemart.ua/products/intel-core-i5-12600k-3449ghz-s1700-tray/)\n 2.[Core i5-11400](https://telemart.ua/products/intel-core-i5-11400-26ghz-12mb-s1200-tray-cm8070804497015/)\n 3.[Core i5-10400F](https://telemart.ua/products/intel-core-i5-10400f-2943ghz-s1200-box/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)

    elif  "Core i7" in message.text :

#  
        msg = bot.send_message(message.chat.id, ' 1.[Core i7-12700K](https://telemart.ua/products/intel-core-i7-12700k-3650ghz-s1700-tray/)\n 2.[Core i7-11700F](https://telemart.ua/products/intel-core-i7-11700f-25ghz-16mb-s1200-box-bx8070811700f/)\n 3.[Core i7-9700K](https://telemart.ua/products/intel-core-i7-9700k-3649ghz-12mb-s1151-box-bx80684i79700k/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)
    elif "Core i9" in message.text :

 
        msg = bot.send_message(message.chat.id, ' 1.[Core i9-10920X](https://telemart.ua/products/intel-core-i9-10920x-3546ghz-1925mb-s2066-box-bx8069510920x/)\n 2.[Core i9-10850K](https://telemart.ua/products/intel-core-i9-10850k-3652ghz-20mb-s1200-box-bx8070110850k/)\n 3.[i9-10900F](https://telemart.ua/products/intel-core-i9-10900f-2851ghz-s1200-box/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)
    elif "Ryzen 5" in message.text:

 
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 5 5600X](https://telemart.ua/products/amd-ryzen-5-5600x-3746ghz-32mb-sam4-multipack-100-100000065mpk/)\n 2.[Ryzen 5 5600G](https://telemart.ua/products/amd-ryzen-5-5600g-3944ghz-16mb-sam4-box-100-100000252box/)\n 3.[Ryzen 5 3600 ](https://telemart.ua/products/amd-ryzen-5-3600-3642ghz-32mb-sam4-tray-100-000000031/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)
    elif  "Ryzen 7" in message.text:

 
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 7 5800X](https://telemart.ua/products/amd-ryzen-7-5800x-3847ghz-32mb-sam4-box-100-100000063wof/)\n 2.[Ryzen 7 5700G](https://telemart.ua/products/amd-ryzen-7-5700g-3846ghz-16mb-sam4-tray-100-000000263/)\n 3.[Ryzen 7 3700X](https://telemart.ua/products/amd-ryzen-7-3700x-3744ghz-32mb-sam4-box-100-100000071box/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)
    elif  "Ryzen 9" in message.text:

 
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 9 5950X](https://telemart.ua/products/amd-ryzen-9-5950x-3449ghz-64mb-sam4-box-100-100000059wof/)\n 2.[Ryzen 9 5900X](https://telemart.ua/products/amd-ryzen-9-5900x-3748ghz-64mb-sam4-box-100-100000061wof/)\n 3.[Ryzen 9 5900X](https://telemart.ua/products/utsenka-protsessor-amd-ryzen-9-5900x-3748ghz-64mb-sam4-tray-100-000000061/) ', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, processor_model_type)



    


    # bot.register_next_step_handler(msg, motherboard)    # bot.register_next_step_handler(msg, processor_model)    
    
    

def processor_model_type(message):
    


    card_img = Image.open(r'D:\projects\Diplom\images\motherboard.jpg') 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетная')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогая')

    markup.row(good)
    markup.add(bad, medium)

    msg = bot.send_photo(message.from_user.id, card_img ,'Что насчет материнской платы  ?'  , reply_markup = markup)


# тут
    insert_data(message.from_user.id, message.text, 'processor_model')
    bot.register_next_step_handler(msg, motherboard_model)
    
    

    


def motherboard_model(message):
    # bot.send_message(message.chat.id, 'Выберите материнскую плату !')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    
    processor = processor_check(message.from_user.id)
    print(processor)

    if  processor == 'Intel':
        
        if message.text == 'Дорогая':
        
            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        
        elif message.text == 'Что-то среднее':


            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif message.text == 'Бюджетная':
    

            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
    elif processor == 'Amd':
        
        if message.text == 'Дорогая':
        
            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        
        elif message.text == 'Что-то среднее':


            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif message.text == 'Бюджетная':
    

            msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)


def motherboard(message):
    
    card_img = Image.open(r'D:\projects\Diplom\images\RTX.jpg') 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетная')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогая')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, card_img ,'Что насчет видеокарты  ?'  , reply_markup = markup)
     

    # insert_data(message.from_user.id, message.text, 'motherboard')
    bot.register_next_step_handler(msg, graphic_card)

def graphic_card(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    

    if message.text == 'Дорогая':
        
        msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model)
        
    elif message.text == 'Что-то среднее':


        msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model)
    elif message.text == 'Бюджетная':
    

        msg = bot.send_message(message.chat.id, '1.[]()\n 2.[]()\n 3.[]()', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model)

    

def graphic_card_model(message):
    ddr_img = Image.open(r'D:\projects\Diplom\images\ddr.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    small = types.InlineKeyboardButton('8')
    medium = types.InlineKeyboardButton('16')
    large = types.InlineKeyboardButton('Больше 16')

    markup.add(small, medium, large)
    
    msg = bot.send_photo(message.from_user.id, ddr_img,'Сколько ОЗУ предпочитаете ? ', reply_markup = markup)

    # insert_data(message.from_user.id, message.text, 'graphic_card')
    bot.register_next_step_handler(msg, ram)    


def ram(message):
    ssd_hdd_img = Image.open(r'D:\projects\Diplom\images\SSD-vs-HDD.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    hdd = types.InlineKeyboardButton('HDD')
    ssd = types.InlineKeyboardButton('SSD')

    markup.add(hdd, ssd)
    
    msg = bot.send_photo(message.from_user.id,ssd_hdd_img , 'HDD or SSD', reply_markup = markup)
     
    
  
    insert_data(message.from_user.id, message.text, 'ram')
    bot.register_next_step_handler(msg, start_5)  
    
  

def start_5(message):
    insert_data(message.from_user.id, message.text, 'memory_type')


    
    
    
    if message.text == "HDD":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        medium = types.InlineKeyboardButton('3 тб')
        good = types.InlineKeyboardButton('1 тб')

        markup.add(good, medium)
        hdd_img = Image.open(r'D:\projects\Diplom\images\hdd.jpg') 
        msg_hdd = bot.send_photo(message.from_user.id, hdd_img ,'Что насчет памяти ?', reply_markup = markup)
        bot.register_next_step_handler(msg_hdd, start_6_memory)
   
    elif message.text == "SSD":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad = types.InlineKeyboardButton('216 гб')
        medium = types.InlineKeyboardButton('512 гб')
        good = types.InlineKeyboardButton('1 тб')

        markup.row(good)
        markup.add(bad, medium)
        ssd_img = Image.open(r'D:\projects\Diplom\images\ssd.jpg') 
        msg_ssd = bot.send_photo(message.from_user.id, ssd_img ,'Что насчет памяти ?', reply_markup = markup)
        bot.register_next_step_handler(msg_ssd, start_6_memory)




def start_6_memory(message):
    insert_data(message.from_user.id, message.text, 'memory_size')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    good = types.InlineKeyboardButton('Высокая')
    medium = types.InlineKeyboardButton('Что-то среднее')
    bad = types.InlineKeyboardButton('Небольшая')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_message(message.from_user.id, 'Что насчет пропускной способности ?'  , reply_markup = markup)
     
    
    if message.text == "216 гб":
        pass
    elif message.text == "512 гб":
        pass
    elif message.text == "1 ТБ":
        pass
    
    bot.register_next_step_handler(msg, start_6_price)    

def start_6_price(message):
    insert_data(message.from_user.id, message.text, 'memory_price')

    block_img = Image.open(r'D:\projects\Diplom\images\block.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогой')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, block_img ,'Что насчет блока питания ?'  , reply_markup = markup)
     
    if message.text == "Бюджетная":
            pass
    elif message.text == "Дорогая":
        pass
    elif message.text == "Что-то средняя":
        pass
    
    bot.register_next_step_handler(msg, pc_power)        
    
    
    
    
def pc_power(message):
    insert_data(message.from_user.id, message.text, 'pc_power')

    pc_img = Image.open(r'D:\projects\Diplom\images\pc.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный')
    medium = types.InlineKeyboardButton('Что-то среднее')
    good = types.InlineKeyboardButton('Дорогой')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, pc_img, 'Что насчет  корпуса ?'  , reply_markup = markup)
     
    
    if message.text == "Бюджетный":
        pass
    elif message.text == "Дорогой":
        pass
    elif message.text == "Что-то среднее":
        pass
    
    bot.register_next_step_handler(msg, pc_case)    

def pc_case(message):
    insert_data(message.from_user.id, message.text, 'pc_case')

    
    if message.text == "Бюджетный":
            pass
    elif message.text == "Дорогой":
        pass
    elif message.text == "Что-то среднее":
        pass




bot.polling(none_stop = True, interval = 0)
# asyncio.run()
