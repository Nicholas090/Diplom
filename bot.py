from unittest import result
import telebot 
import configure
from telebot import types 
from firebase_setting import ref
from PIL import Image
from sql.sqlConnect import *
from data.data import *
from data.parse import parse_price

bot = telebot.TeleBot(configure.config['token'])
 
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
    


    if call.data == 'yes_start':
        msg = bot.send_photo(call.from_user.id, processor_img, 'Какой процессор предпочитаете ? ', reply_markup=markup)

        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')  
        bot.register_next_step_handler(msg, processor_brand)   
    elif call.data == 'no_start':
        bot.send_message(call.message.chat.id, 'Ладно')
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.message_id, reply_markup = '')

    


def processor_brand(message):

    insert_data(message.from_user.id, message.text, 'processor_brand')

     
    
    if message.text == "Intel":
        intel_img = Image.open(r'D:\projects\Diplom\images\intel.jpg')

        markup_intel = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_intel = types.InlineKeyboardButton(f'Core i5 ({parse_price(corei5_link[2],"4 000")} - {parse_price(corei5_link[0], "8 000")})грн')
        medium_intel = types.InlineKeyboardButton(f'Core i7 ({parse_price(corei7_link[2],"6 000")} - {parse_price(corei7_link[0], "12 000")})грн')
        good_intel = types.InlineKeyboardButton(f'Core i9 ({parse_price(corei9_link[2],"12 000")} - {parse_price(corei9_link[0], "22 000")})грн')

        markup_intel.row(good_intel)
        markup_intel.add(bad_intel, medium_intel)
        msg_intel = bot.send_photo(message.from_user.id,intel_img ,'Какую модель процессора хотели бы ? ', reply_markup = markup_intel)

        bot.register_next_step_handler(msg_intel, processor_model)  
    elif message.text == "Amd":

        amd_img = Image.open(r'D:\projects\Diplom\images\amd.jpg')

        markup_amd = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_amd = types.InlineKeyboardButton(f'Ryzen 5 ({parse_price(ryzen5_link[2],"4 000")} - {parse_price(ryzen5_link[0], "8 000")})грн')
        medium_amd = types.InlineKeyboardButton(f'Ryzen 7 ({parse_price(ryzen7_link[2],"6 000")} - {parse_price(ryzen7_link[0], "11 000")})грн')
        good_amd = types.InlineKeyboardButton(f'Ryzen 9 ({parse_price(ryzen9_link[2],"12 000")} - {parse_price(ryzen9_link[0], "22 000")})грн')

        markup_amd.row(good_amd)
        markup_amd.add(bad_amd, medium_amd)

        msg_amd = bot.send_photo(message.from_user.id, amd_img, 'Какую модель процессора хотели бы ? ', reply_markup = markup_amd)
        bot.register_next_step_handler(msg_amd, processor_model)  
    


def processor_model(message):
    insert_data(message.from_user.id, message.text[0:7], 'processor_chip')

    bot.send_message(message.chat.id, 'Выберите процессор !')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)

    if "Core i5" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Core i5-12600K]({corei5_link[0]}) \n 2.[Core i5-11400]({corei5_link[1]})\n 3.[Core i5-10400F]({corei5_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
    elif  "Core i7" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Core i7-12700K]({corei7_link[0]})\n 2.[Core i7-11700F]({corei7_link[1]})\n 3.[Core i7-9700K]({corei7_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
    elif "Core i9" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Core i9-10920X]({corei9_link[0]})\n 2.[Core i9-10850K]({corei9_link[1]})\n 3.[Core i9-10900F]({corei9_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
    elif "Ryzen 5" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Ryzen 5 5600X]({ryzen5_link[0]})\n 2.[Ryzen 5 5600G]({ryzen5_link[1]})\n 3.[Ryzen 5 3600]({ryzen5_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
    elif "Ryzen 7" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Ryzen 7 5800X]({ryzen7_link[0]})\n 2.[Ryzen 7 5700G]({ryzen7_link[1]})\n 3.[Ryzen 7 3700X]({ryzen7_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
    elif "Ryzen 9" in message.text:
        msg = bot.send_message(message.chat.id, f' 1.[Ryzen 9 5950X]({ryzen9_link[0]})\n 2.[Ryzen 9 5900X]({ryzen9_link[1]})\n 3.[Ryzen 9 5900X]({ryzen9_link[2]}) ', reply_markup=markup, parse_mode='Markdown')
       
    bot.register_next_step_handler(msg, processor_model_type)


    


    
    

def processor_model_type(message):

    processor_chip = state_check(message.from_user.id, 'processor_chip')

    if  'Core i9' in processor_chip:
        res = corei9[(int(message.text) - 1)]
        res_link = corei9_link[(int(message.text) - 1)]
    elif 'Core i7' in processor_chip:
        res = corei7[(int(message.text) - 1)]
        res_link = corei7_link[(int(message.text) - 1)]
    elif 'Core i5' in processor_chip:
        res = corei5[(int(message.text) - 1)]
        res_link = corei5_link[(int(message.text) - 1)]
    elif  'Ryzen 9' in processor_chip:
        res = ryzen9[(int(message.text) - 1)]
        res_link = ryzen9_link[(int(message.text) - 1)]
    elif 'Ryzen 7' in processor_chip:
        res = ryzen7[(int(message.text) - 1)]
        res_link = ryzen7_link[(int(message.text) - 1)]
    elif 'Ryzen 5' in processor_chip:
        res = ryzen5[(int(message.text) - 1)]
        res_link = ryzen5_link[(int(message.text) - 1)]

    processor = state_check(message.from_user.id, 'processor_brand')

    insert_data(message.from_user.id, res , 'processor_model')
    insert_data(message.from_user.id, res_link , 'processor_link')

    
    card_img = Image.open(r'D:\projects\Diplom\images\motherboard.jpg') 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    if processor == 'Intel':
        bad = types.InlineKeyboardButton(f'Бюджетная ({parse_price(motherboard_intel_b_link[2],"1 500")} - {parse_price(motherboard_intel_b_link[0],"4 000")})')
        medium = types.InlineKeyboardButton(f'Что-то среднее ({parse_price(motherboard_intel_m_link[2],"4 500")} - {parse_price(motherboard_intel_m_link[0],"8 000")})')
        good = types.InlineKeyboardButton(f'Дорогая ({parse_price(motherboard_intel_g_link[2],"8 000")} - {parse_price(motherboard_intel_g_link[0],"14 000")})')
        markup.row(good)
        markup.add(bad, medium)

    elif processor == 'Amd':
        bad = types.InlineKeyboardButton(f'Бюджетная ({parse_price(motherboard_amd_b_link[2],"1 500")} - {parse_price(motherboard_amd_b_link[0],"4 000")})')
        medium = types.InlineKeyboardButton(f'Что-то среднее ({parse_price(motherboard_amd_m_link[2],"4 000")} - {parse_price(motherboard_amd_m_link[0],"8 000")})')
        good = types.InlineKeyboardButton(f'Дорогая ({parse_price(motherboard_amd_g_link[2],"8 000")} - {parse_price(motherboard_amd_g_link[0],"14 000")})')
        markup.row(good)
        markup.add(bad, medium)       

    msg = bot.send_photo(message.from_user.id, card_img,'Что насчет материнской платы ?', reply_markup = markup)

    bot.register_next_step_handler(msg, motherboard_model)
    
    

    


def motherboard_model(message):
    insert_data(message.from_user.id, message.text, 'motherboard_price')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    
    processor = state_check(message.from_user.id, 'processor_brand')

    if processor == 'Intel':
        if 'Дорогая' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[ASUS ROG MAXIMUS Z690]({motherboard_intel_g_link[0]})\n 2.[ASUS ROG STRIX Z690-F]({motherboard_intel_g_link[1]})\n 3.[ASUS ROG STRIX Z590-F]({motherboard_intel_g_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif  'Что-то среднее' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[ASUS PRIME Z690M-PLUS D4]({motherboard_intel_m_link[0]})\n 2.[MSI MPG Z490]({motherboard_intel_m_link[1]})\n 3.[MSI MAG B560M]({motherboard_intel_m_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif 'Бюджетная' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Asus PRIME B560-PLUS]({motherboard_intel_b_link[0]})\n 2.[Asus PRIME B460M-A]({motherboard_intel_b_link[1]})\n 3.[MSI H510M PRO]({motherboard_intel_b_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif processor == 'Amd':
        if 'Дорогая' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Asus ROG CROSSHAIR VIII FORMULA]({motherboard_amd_g_link[0]})\n 2.[Asus PRIME TRX40-Pro S]({motherboard_amd_g_link[1]})\n 3.[Asus Pro WS X570-ACE]({motherboard_amd_g_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif 'Что-то среднее' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Asus ProArt B550-CREATOR]({motherboard_amd_m_link[0]})\n 2.[Asus TUF GAMING X570-PLUS]({motherboard_amd_m_link[1]})\n 3.[AsRock X570M]({motherboard_amd_m_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif 'Бюджетная' in message.text:
            msg = bot.send_message(message.chat.id, f'1.[AsRock X570 Pro4]({motherboard_amd_b_link[0]})\n 2.[Gigabyte B450 AORUS PRO]({motherboard_amd_b_link[1]})\n 3.[Asus PRIME A320M-E]({motherboard_amd_b_link[2]})', reply_markup=markup, parse_mode='Markdown')
        
    bot.register_next_step_handler(msg, motherboard)


def motherboard(message):

    processor = state_check(message.from_user.id, 'processor_brand')
    motherboard_price = state_check(message.from_user.id, 'motherboard_price')


    if processor == 'Intel':
        if 'Бюджетная' in motherboard_price:
            res = motherboard_intel_b[(int(message.text) - 1)]
            res_link = motherboard_intel_b_link[(int(message.text) - 1)]
        elif 'Что-то среднее' in motherboard_price:
            res = motherboard_intel_m[(int(message.text) - 1)]
            res_link = motherboard_intel_m_link[(int(message.text) - 1)]
        elif 'Дорогая' in motherboard_price:
            res = motherboard_intel_g[(int(message.text) - 1)]
            res_link = motherboard_intel_g_link[(int(message.text) - 1)]

    elif processor == 'Amd':
        if 'Бюджетная' in motherboard_price:
            res = motherboard_amd_b[(int(message.text) - 1)]
            res_link = motherboard_amd_b_link[(int(message.text) - 1)]
        elif 'Что-то среднее' in motherboard_price:
            res = motherboard_amd_m[(int(message.text) - 1)]
            res_link = motherboard_amd_m_link[(int(message.text) - 1)]
        elif 'Дорогая' in motherboard_price:
            res = motherboard_amd_g[(int(message.text) - 1)]
            res_link = motherboard_amd_g_link[(int(message.text) - 1)]


    insert_data(message.from_user.id, res, 'motherboard_model')
    insert_data(message.from_user.id, res_link, 'motherboard_link')


    card_img = Image.open(r'D:\projects\Diplom\images\RTX.jpg') 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton(f'Бюджетная  ({parse_price(graphic_card_b_link[2],"8 000")} - {parse_price(graphic_card_b_link[0],"14 000")})')
    medium = types.InlineKeyboardButton(f'Что-то среднее ({parse_price(graphic_card_m_link[2],"18 000")} - {parse_price(graphic_card_m_link[0],"25 000")})')
    good = types.InlineKeyboardButton(f'Дорогая ({parse_price(graphic_card_g_link[2],"30 000")} - {parse_price(graphic_card_g_link[0],"47 000")})')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, card_img ,'Что насчет видеокарты ?'  , reply_markup = markup)
     
    bot.register_next_step_handler(msg, graphic_card)

def graphic_card(message):
    insert_data(message.from_user.id, message.text, 'graphic_card_price')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    

    if 'Дорогая' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[RTX 3070 Ti AORUS]({graphic_card_g_link[0]})\n 2.[RTX 3060 Ti]({graphic_card_g_link[1]})\n 3.[RTX 2080]({graphic_card_g_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Что-то среднее' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[RTX 3060 StormX]({graphic_card_m_link[0]})\n 2.[RTX 2060 D6]({graphic_card_m_link[1]})\n 3.[GTX 1660 Ti]({graphic_card_m_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Бюджетная' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[GTX 1660]({graphic_card_b_link[0]})\n 2.[GTX 1650 Phoenix]({graphic_card_b_link[0]})\n 3.[GTX 1650 VENTUS XS]({graphic_card_b_link[0]})', reply_markup=markup, parse_mode='Markdown')
        
    bot.register_next_step_handler(msg, graphic_card_model)

    

def graphic_card_model(message):
    card = state_check(message.from_user.id, 'graphic_card_price')
    
    if 'Бюджетная' in card:
        res = graphic_card_b[(int(message.text) - 1)]
        res_link = graphic_card_b_link[(int(message.text) - 1)]
    elif 'Что-то среднее' in card:
        res = graphic_card_m[(int(message.text) - 1)]
        res_link = graphic_card_m_link[(int(message.text) - 1)]
    elif 'Дорогая' in card:
        res = graphic_card_g[(int(message.text) - 1)]
        res_link = graphic_card_g_link[(int(message.text) - 1)]


    insert_data(message.from_user.id, res , 'graphic_card_model')
    insert_data(message.from_user.id, res_link , 'graphic_card_link')

    ddr_img = Image.open(r'D:\projects\Diplom\images\ddr.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    small = types.InlineKeyboardButton('8')
    medium = types.InlineKeyboardButton('16')
    large = types.InlineKeyboardButton('32')

    markup.add(small, medium, large)
    
    msg = bot.send_photo(message.from_user.id, ddr_img,'Сколько ОЗУ предпочитаете ? ', reply_markup = markup)

    bot.register_next_step_handler(msg, ram_size)    



def ram_size(message):
    
    insert_data(message.from_user.id, message.text, 'ram_size')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    
    ram_size = state_check(message.from_user.id, 'ram_size')
    print(ram_size)
    
    if ram_size == '8':
        msg = bot.send_message(message.chat.id, f'1.[Kingston DDR4 8G]({ram8_link[0]})\n 2.[GoodRAM DDR4 8GB]({ram8_link[1]})\n 3.[Team DDR4 8GB]({ram8_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif ram_size == '16':
        msg = bot.send_message(message.chat.id, f'1.[Patriot DDR4 16GB]({ram16_link[0]})\n 2.[G.Skill DDR4 16GB]({ram16_link[1]})\n 3.[G.Skill DDR4 16GB]({ram16_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif ram_size == '32':
        msg = bot.send_message(message.chat.id, f'1.[Kingston DDR5 32GB]({ram32_link[0]})\n 2.[G.Skill DDR4 32GB]({ram32_link[1]})\n 3.[Patriot DDR4 32GB]({ram32_link[2]})', reply_markup=markup, parse_mode='Markdown')
    
    bot.register_next_step_handler(msg, ram_model)

    

    # bot.register_next_step_handler(msg, ram_model)



def ram_model(message):
    ram_size = state_check(message.from_user.id, 'ram_size')
    
    if ram_size == '8':
        res = ram8[(int(message.text) - 1)]
        res_link = ram8_link[(int(message.text) - 1)]
    elif ram_size == '16':
        res = ram16[(int(message.text) - 1)]
        res_link = ram16_link[(int(message.text) - 1)]
    elif ram_size == '32':
        res = ram32[(int(message.text) - 1)]
        res_link = ram32_link[(int(message.text) - 1)]


    insert_data(message.from_user.id, res, 'ram_model')
    insert_data(message.from_user.id, res_link, 'ram_link')

    ssd_hdd_img = Image.open(r'D:\projects\Diplom\images\SSD-vs-HDD.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    hdd = types.InlineKeyboardButton('HDD')
    ssd = types.InlineKeyboardButton('SSD')

    markup.add(hdd, ssd)
    
    msg = bot.send_photo(message.from_user.id,  ssd_hdd_img , 'HDD or SSD', reply_markup = markup)
     
    
  
    bot.register_next_step_handler(msg, start_5)  
    
  

def start_5(message):
    insert_data(message.from_user.id, message.text, 'memory_type')
    
    if message.text == "HDD":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        medium = types.InlineKeyboardButton(f'2 тб ({parse_price(hdd_2tb_link[1],"1 500")} - {parse_price(hdd_2tb_link[0],"2 000")})')
        good = types.InlineKeyboardButton(f'1 тб ({parse_price(hdd_1tb_link[1],"1 000")} - {parse_price(hdd_1tb_link[0],"1 400")})')

        markup.add(good, medium)
        hdd_img = Image.open(r'D:\projects\Diplom\images\hdd.jpg') 
        msg = bot.send_photo(message.from_user.id, hdd_img ,'Что насчет памяти ?', reply_markup = markup)
        bot.register_next_step_handler(msg, memory_size)
   
   
    elif message.text == "SSD":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad = types.InlineKeyboardButton(f'216 гб ({parse_price(ssd_216_link[2],"2 000")} - {parse_price(ssd_216_link[0],"4 000")})')
        medium = types.InlineKeyboardButton(f'512 гб ({parse_price(ssd_512_link[2],"3 000")} - {parse_price(ssd_512_link[0],"7 000")})')
        good = types.InlineKeyboardButton(f'1 тб ({parse_price(ssd_1_link[2],"8 000")} - {parse_price(ssd_1_link[0],"14 000")})')

        markup.row(good)
        markup.add(bad, medium)
        ssd_img = Image.open(r'D:\projects\Diplom\images\ssd.jpg') 
        msg = bot.send_photo(message.from_user.id, ssd_img ,'Что насчет памяти ?', reply_markup = markup)
        bot.register_next_step_handler(msg, memory_size)






def memory_size(message):
    insert_data(message.from_user.id, message.text, 'memory_size')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)

     
    memory = state_check(message.from_user.id, 'memory_type')
    
    print(memory)
    
    if memory  == 'HDD':
        if "1 тб" in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Western Digital Blue 1TB]({hdd_1tb_link[0]})\n 2.[Seagate BarraCuda 1TB]({hdd_1tb_link[1]})', reply_markup=markup, parse_mode='Markdown')
        elif "2 тб" in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Toshiba P300 2TB]({hdd_2tb_link[0]})\n 2.[Seagate BarraCuda 2TB]({hdd_2tb_link[1]})', reply_markup=markup, parse_mode='Markdown')
    elif memory == 'SSD':
        if "216 гб" in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Gigabyte 256GB 2.5]({ssd_216_link[0]})\n 2.[Patriot P210 256GB]({ssd_216_link[1]})\n 3.[Patriot Burst 240GB]({ssd_216_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif "512 гб" in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Kingston FURY Renegade 3D]({ssd_512_link[0]})\n 2.[Samsung 870 EVO V-NAND]({ssd_512_link[1]})\n 3.[Patriot P300 512GB]({ssd_512_link[2]})', reply_markup=markup, parse_mode='Markdown')
        elif "1 тб" in message.text:
            msg = bot.send_message(message.chat.id, f'1.[Samsung 970 PRO V-NAND]({ssd_1_link[0]})\n 2.[Corsair Force Series MP600]({ssd_1_link[1]})\n 3.[Intel 660p 3D QLC 1TB]({ssd_1_link[2]})', reply_markup=markup, parse_mode='Markdown')
    
    bot.register_next_step_handler(msg, memory_model)    

def memory_model(message):
    memory_type = state_check(message.from_user.id, 'memory_type')
    memory_size = state_check(message.from_user.id, 'memory_size')

    if memory_type == 'SSD':
        if '216' in memory_size:
            res = ssd_216[(int(message.text) - 1)]
            res_link = ssd_216_link[(int(message.text) - 1)]
        elif '512' in memory_size:
            res = ssd_512[(int(message.text) - 1)]
            res_link = ssd_512_link[(int(message.text) - 1)]
        elif '1 тб' in memory_size:
            res = ssd_1[(int(message.text) - 1)]
            res_link = ssd_1_link[(int(message.text) - 1)]
    elif memory_type == 'HDD':
        if '1 тб' in memory_size:
            res = hdd_1tb[(int(message.text) - 1)]
            res_link = hdd_1tb_link[(int(message.text) - 1)]
        elif '2 тб' in memory_size:
            res = hdd_2tb[(int(message.text) - 1)]
            res_link = hdd_2tb_link[(int(message.text) - 1)]


    insert_data(message.from_user.id, res, 'memory_model')
    insert_data(message.from_user.id, res_link, 'memory_link')


    block_img = Image.open(r'D:\projects\Diplom\images\block.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton(f'Бюджетный ({parse_price(pc_power_b_link[2],"500")} - {parse_price(pc_power_b_link[0],"1 200")})')
    medium = types.InlineKeyboardButton(f'Что-то среднее ({parse_price(pc_power_m_link[2],"1 500")} - {parse_price(pc_power_m_link[0],"2 200")})')
    good = types.InlineKeyboardButton(f'Дорогой ({parse_price(pc_power_g_link[2],"2 500")} - {parse_price(pc_power_g_link[0],"4 200")})')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, block_img ,'Что насчет блока питания ?'  , reply_markup = markup)
    
    bot.register_next_step_handler(msg, pc_power)        
    

def pc_power(message):
    insert_data(message.from_user.id, message.text, 'pc_power_price')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
 
    if 'Дорогой' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[CHIEFTEC Polaris 1050W]({pc_power_g_link[0]})\n 2.[Corsair RM750x 750W]({pc_power_g_link[1]})\n 3.[Seasonic CORE GC 650W Gold]({pc_power_g_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Что-то среднее' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[Be Quiet! System Power 9 700W]({pc_power_m_link[0]})\n 2.[Gigabyte P750GM 750W]({pc_power_m_link[1]})\n 3.[GAMEMAX RGB-550 550W]({pc_power_m_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Бюджетный' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[CHIEFTEC Force 500W]({pc_power_b_link[0]})\n 2.[CHIEFTEC VALUE SERIES 400W OEM]({pc_power_b_link[1]})\n 3.[GAMEMAX 400W 120mm FAN]({pc_power_b_link[2]})', reply_markup=markup, parse_mode='Markdown')
    
    bot.register_next_step_handler(msg, pc_power_model)

    
def pc_power_model(message):

    pc_price = state_check(message.from_user.id, 'pc_power_price')

    if 'Бюджетный' in pc_price:
        res = pc_power_b[(int(message.text) - 1)]
        res_link = pc_power_b_link[(int(message.text) - 1)]
    elif 'Что-то среднее' in pc_price:
        res = pc_power_m[(int(message.text) - 1)]
        res_link = pc_power_m_link[(int(message.text) - 1)]
    elif 'Дорогой' in pc_price:
        res = pc_power_g[(int(message.text) - 1)]
        res_link = pc_power_g_link[(int(message.text) - 1)]

    insert_data(message.from_user.id, res, 'pc_power_model')
    insert_data(message.from_user.id, res_link, 'pc_power_link')

    pc_img = Image.open(r'D:\projects\Diplom\images\pc.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton(f'Бюджетный  ({parse_price(pc_case_b_link[2],"800")} - {parse_price(pc_case_b_link[0],"1 200")})')
    medium = types.InlineKeyboardButton(f'Что-то среднее ({parse_price(pc_case_m_link[2],"1 300")} - {parse_price(pc_case_m_link[0],"2 500")})')
    good = types.InlineKeyboardButton(f'Дорогой ({parse_price(pc_case_m_link[2],"3 000")} - {parse_price(pc_case_m_link[0],"5 500")})')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, pc_img, 'Что насчет корпуса ?', reply_markup = markup)

    bot.register_next_step_handler(msg, pc_case)    



def pc_case(message):
    insert_data(message.from_user.id, message.text, 'pc_case_price')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
 
    if 'Дорогой' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[Asus TUF Gaming GT501]({pc_case_g_link[0]})\n 2.[Fractal Design Define 7]({pc_case_g_link[1]})\n 3.[Thermaltake V250]({pc_case_g_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Что-то среднее' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[Thermaltake V200]({pc_case_m_link[0]})\n 2.[2E Gaming Hexagon]({pc_case_m_link[1]})\n 3.[GAMEMAX Diamond ARGB]({pc_case_m_link[2]})', reply_markup=markup, parse_mode='Markdown')
    elif 'Бюджетный' in message.text:
        msg = bot.send_message(message.chat.id, f'1.[1stPlayer V3-A-4G6]({pc_case_b_link[0]})\n 2.[1stPlayer F4-3R1]({pc_case_b_link[1]})\n 3.[GAMEMAX MT520-NP]({pc_case_b_link[2]})', reply_markup=markup, parse_mode='Markdown')

    bot.register_next_step_handler(msg, pc_case_model)
        
        

def pc_case_model(message):

    pc_price = state_check(message.from_user.id, 'pc_case_price')

    if 'Бюджетный' in pc_price:
        res = pc_case_b[(int(message.text) - 1)]
        res_link = pc_case_b_link[(int(message.text) - 1)]
    elif 'Что-то среднее' in pc_price:
        res = pc_case_m[(int(message.text) - 1)]
        res_link = pc_case_m_link[(int(message.text) - 1)]
    elif 'Дорогой' in pc_price:
        res = pc_case_g[(int(message.text) - 1)]
        res_link = pc_case_g_link[(int(message.text) - 1)]


    insert_data(message.from_user.id, res, 'pc_case_model')
    insert_data(message.from_user.id, res_link, 'pc_case_link')

    
    processor_model = state_check(message.from_user.id, 'processor_model')
    processor_link = state_check(message.from_user.id, 'processor_link')
    motherboard_model = state_check(message.from_user.id, 'motherboard_model')
    motherboard_link = state_check(message.from_user.id, 'motherboard_link')
    graphic_card_model = state_check(message.from_user.id, 'graphic_card_model')
    graphic_card_link = state_check(message.from_user.id, 'graphic_card_link')
    ram_model = state_check(message.from_user.id, 'ram_model')
    ram_link = state_check(message.from_user.id, 'ram_link')
    memory_model = state_check(message.from_user.id, 'memory_model')
    memory_link = state_check(message.from_user.id, 'memory_link')
    pc_power_model = state_check(message.from_user.id, 'pc_power_model')
    pc_power_link = state_check(message.from_user.id, 'pc_power_link')

    pc_case_model = state_check(message.from_user.id, 'pc_case_model')
    pc_case_link = state_check(message.from_user.id, 'pc_case_link')

    def result_sum(*links):
        res = 0
        for el in links:
          res += int((parse_price(el)).replace(' ', ''))
        print(type(res))
        print(res)
        return res

    results = f'''Ваша сборка :
Процессор: [{processor_model}]({processor_link})
Материнская плата: [{motherboard_model}]({motherboard_link})
Видеокарта: [{graphic_card_model}]({graphic_card_link})
ОЗУ: [{ram_model}]({ram_link})
Память: [{memory_model}]({memory_link})
Блок питания: [{pc_power_model}]({pc_power_link})
Корпус: [{pc_case_model}]({pc_case_link})

Сумма: {result_sum(processor_link, motherboard_link, graphic_card_link, ram_link, memory_link, pc_power_link, pc_case_link)}



    '''
    
    bot.send_message(message.from_user.id, results, parse_mode='Markdown')
    





bot.polling(none_stop = True, interval = 0)

