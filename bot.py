from unittest import result
import telebot 
import configure
from telebot import types 
from firebase_setting import ref
from PIL import Image
from sql.sqlConnect import *
from data.data import *

bot = telebot.TeleBot(configure.config['token'])
 
# @bot.message_handler(commands=['info'])
# def get_info(message):
#     name_= message.from_user.username
#     id_ = message.from_user.id
#     data = { str(name_ ): str(id_)}
#     ref.push(data)
    
 
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
        good_intel = types.InlineKeyboardButton('Core i9 (13 655 - 22 522)грн')

        markup_intel.row(good_intel)
        markup_intel.add(bad_intel, medium_intel)
        msg_intel = bot.send_photo(message.from_user.id,intel_img ,'Какую модель процессора хотели бы ? ', reply_markup = markup_intel)

        bot.register_next_step_handler(msg_intel, processor_model)  
    elif message.text == "Amd":

        amd_img = Image.open(r'D:\projects\Diplom\images\amd.jpg')

        markup_amd = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad_amd = types.InlineKeyboardButton('Ryzen 5 (6 200 - 9 400)')
        medium_amd = types.InlineKeyboardButton('Ryzen 7 (9 099 - 12 399)')
        good_amd = types.InlineKeyboardButton('Ryzen 9 (15 699 - 22 899)')

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

    if "Core i5" in message.text :
        msg = bot.send_message(message.chat.id, ' 1.[Core i5-12600K](https://telemart.ua/products/intel-core-i5-12600k-3449ghz-s1700-tray/)\n 2.[Core i5-11400](https://telemart.ua/products/intel-core-i5-11400-26ghz-12mb-s1200-tray-cm8070804497015/)\n 3.[Core i5-10400F](https://telemart.ua/products/intel-core-i5-10400f-2943ghz-s1200-box/) ', reply_markup=markup, parse_mode='Markdown')
    elif  "Core i7" in message.text :
        msg = bot.send_message(message.chat.id, ' 1.[Core i7-12700K](https://telemart.ua/products/intel-core-i7-12700k-3650ghz-s1700-tray/)\n 2.[Core i7-11700F](https://telemart.ua/products/intel-core-i7-11700f-25ghz-16mb-s1200-box-bx8070811700f/)\n 3.[Core i7-9700K](https://telemart.ua/products/intel-core-i7-9700k-3649ghz-12mb-s1151-box-bx80684i79700k/) ', reply_markup=markup, parse_mode='Markdown')
    elif "Core i9" in message.text :
        msg = bot.send_message(message.chat.id, ' 1.[Core i9-10920X](https://telemart.ua/products/intel-core-i9-10920x-3546ghz-1925mb-s2066-box-bx8069510920x/)\n 2.[Core i9-10850K](https://telemart.ua/products/intel-core-i9-10850k-3652ghz-20mb-s1200-box-bx8070110850k/)\n 3.[Core i9-10900F](https://telemart.ua/products/intel-core-i9-11900f-25ghz-16mb-s1200-box-bx8070811900f/) ', reply_markup=markup, parse_mode='Markdown')
    elif "Ryzen 5" in message.text:
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 5 5600X](https://telemart.ua/products/amd-ryzen-5-5600x-3746ghz-32mb-sam4-multipack-100-100000065mpk/)\n 2.[Ryzen 5 5600G](https://telemart.ua/products/amd-ryzen-5-5600g-3944ghz-16mb-sam4-box-100-100000252box/)\n 3.[Ryzen 5 3600](https://telemart.ua/products/amd-ryzen-5-3600-3642ghz-32mb-sam4-tray-100-000000031/) ', reply_markup=markup, parse_mode='Markdown')
    elif  "Ryzen 7" in message.text:
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 7 5800X](https://telemart.ua/products/amd-ryzen-7-5800x-3847ghz-32mb-sam4-box-100-100000063wof/)\n 2.[Ryzen 7 5700G](https://telemart.ua/products/amd-ryzen-7-5700g-3846ghz-16mb-sam4-tray-100-000000263/)\n 3.[Ryzen 7 3700X](https://telemart.ua/products/amd-ryzen-7-3700x-3744ghz-32mb-sam4-box-100-100000071box/) ', reply_markup=markup, parse_mode='Markdown')
    elif  "Ryzen 9" in message.text:
        msg = bot.send_message(message.chat.id, ' 1.[Ryzen 9 5950X](https://telemart.ua/products/amd-ryzen-9-5950x-3449ghz-64mb-sam4-box-100-100000059wof/)\n 2.[Ryzen 9 5900X](https://telemart.ua/products/amd-ryzen-9-5900x-3748ghz-64mb-sam4-box-100-100000061wof/)\n 3.[Ryzen 9 5900X](https://telemart.ua/products/utsenka-protsessor-amd-ryzen-9-5900x-3748ghz-64mb-sam4-tray-100-000000061/) ', reply_markup=markup, parse_mode='Markdown')
       
    bot.register_next_step_handler(msg, processor_model_type)


    


    
    

def processor_model_type(message):

    processor_chip = (state_check(message.from_user.id, 'processor_chip'))[0]

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
    
    if processor[0] == 'Intel':
        bad = types.InlineKeyboardButton('Бюджетная (1 999 - 3 849)')
        medium = types.InlineKeyboardButton('Что-то среднее (4 723 - 6 516)')
        good = types.InlineKeyboardButton('Дорогая (9 666 - 18 609)')
        markup.row(good)
        markup.add(bad, medium)
        
    elif processor[0] == 'Amd':
        bad = types.InlineKeyboardButton('Бюджетная (2 302 - 3 999)')
        medium = types.InlineKeyboardButton('Что-то среднее (6 248 - 8 305)')
        good = types.InlineKeyboardButton('Дорогая (10 920 - 18 457)')
        markup.row(good)
        markup.add(bad, medium)       

    msg = bot.send_photo(message.from_user.id, card_img ,'Что насчет материнской платы ?'  , reply_markup = markup)

    bot.register_next_step_handler(msg, motherboard_model)
    
    

    


def motherboard_model(message):
    insert_data(message.from_user.id, message.text, 'motherboard_price')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
    
    processor = (state_check(message.from_user.id, 'processor_brand'))[0]

    if  processor == 'Intel':
        if 'Дорогая' in message.text:
            msg = bot.send_message(message.chat.id, '1.[ASUS ROG MAXIMUS Z690](https://telemart.ua/products/asus-rog-maximus-z690-hero-s1700-intel-z690/)\n 2.[ASUS ROG STRIX Z690-F](https://telemart.ua/products/asus-rog-strix-z690-f-gaming-s1700-intel-z690/)\n 3.[ASUS ROG STRIX Z590-F](https://telemart.ua/products/asus-rog-strix-z590-f-gaming-wifi-s1200-intel-z590/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif  'Что-то среднее' in message.text:
            msg = bot.send_message(message.chat.id, '1.[ASUS PRIME Z690M-PLUS D4](https://telemart.ua/products/asus-prime-z690m-plus-d4-s1700-intel-z690/)\n 2.[MSI MPG Z490](https://telemart.ua/products/msi-mpg-z490-gaming-plus-s1200-intel-z490/)\n 3.[MSI MAG B560M](https://telemart.ua/products/msi-mag-b560m-mortar-wifi-s1200-intel-b560/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif 'Бюджетная' in message.text:
            msg = bot.send_message(message.chat.id, '1.[Asus PRIME B560-PLUS](https://telemart.ua/products/asus-prime-b560-plus-s1200-intel-b560/)\n 2.[Asus PRIME B460M-A](https://telemart.ua/products/asus-prime-b460m-a-r20-s1200-intel-h470/)\n 3.[MSI H510M PRO](https://telemart.ua/products/msi-h510m-pro-s1200-intel-h510/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
    elif processor == 'Amd':
        if  'Дорогая' in message.text:
            msg = bot.send_message(message.chat.id, '1.[Asus ROG CROSSHAIR VIII FORMULA](https://telemart.ua/products/asus-rog-crosshair-viii-formula-sam4-amd-x570/)\n 2.[Asus PRIME TRX40-Pro S](https://telemart.ua/products/asus-prime-trx40-pro-s-strx4-amd-trx40/)\n 3.[Asus Pro WS X570-ACE](https://telemart.ua/products/asus-pro-ws-x570-ace-sam4-amd-x570/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif 'Что-то среднее' in message.text:
            msg = bot.send_message(message.chat.id, '1.[Asus ProArt B550-CREATOR](https://telemart.ua/products/asus-proart-b550-creator-sam4-amd-b550/)\n 2.[Asus TUF GAMING X570-PLUS](https://telemart.ua/products/asus-tuf-gaming-x570-plus-wi-fi-sam4-amd-x570/)\n 3.[AsRock X570M](https://telemart.ua/products/asrock-x570m-pro4-sam4-amd-x570/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)
        elif  'Бюджетная' in message.text:
            msg = bot.send_message(message.chat.id, '1.[AsRock X570 Pro4](https://telemart.ua/products/asrock-x570-pro4-sam4-amd-x570/)\n 2.[Gigabyte B450 AORUS PRO](https://telemart.ua/products/gigabyte-b450-aorus-pro-sam4-amd-b450/)\n 3.[Asus PRIME A320M-E](https://telemart.ua/products/asus-prime-a320m-e-sam4-amd-a320/)', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(msg, motherboard)


def motherboard(message):

    processor = (state_check(message.from_user.id, 'processor_brand'))[0]
    motherboard_price = (state_check(message.from_user.id, 'motherboard_price'))[0]


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
    bad = types.InlineKeyboardButton('Бюджетная (10 899 - 15 999)')
    medium = types.InlineKeyboardButton('Что-то среднее (17 299 - 24 999)')
    good = types.InlineKeyboardButton('Дорогая (30 999 - 46 999)')

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
    

    if  'Дорогая' in message.text:
        msg = bot.send_message(message.chat.id, '1.[RTX 3070 Ti AORUS](https://telemart.ua/products/gigabyte-geforce-rtx-3070-ti-aorus-master-8192mb-gv-n307taorus-m-8gd/)\n 2.[RTX 3060 Ti](https://telemart.ua/products/gigabyte-geforce-rtx-3060-ti-gaming-oc-8192mb-gv-n306tgaming-oc-8gd-20/)\n 3.[RTX 2080](https://telemart.ua/products/asus-geforce-rtx-2080-super-dual-evo-8192mb-dual-rtx2080s-8g-evo-fr-factory-recertified/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model) 
    elif 'Что-то среднее' in message.text:
        msg = bot.send_message(message.chat.id, '1.[RTX 3060 StormX](https://telemart.ua/products/palit-geforce-rtx-3060-stormx-12288mb-ne63060019k9-190af/)\n 2.[RTX 2060 D6](https://telemart.ua/products/gigabyte-geforce-rtx-2060-d6-6144mb-gv-n2060d6-6gd/)\n 3.[GTX 1660 Ti](https://telemart.ua/products/gigabyte-gtx-1660-ti-oc-6144mb-gv-n166toc-6gd/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model)
    elif 'Бюджетная' in message.text:
        msg = bot.send_message(message.chat.id, '1.[GTX 1660](https://telemart.ua/products/gigabyte-geforce-gtx-1660-oc-6144mb-gv-n1660oc-6gd/)\n 2.[GTX 1650 Phoenix](https://telemart.ua/products/asus-geforce-gtx-1650-phoenix-oc-4096mb-ph-gtx1650-o4g/)\n 3.[GTX 1650 VENTUS XS](https://telemart.ua/products/msi-geforce-gtx-1650-ventus-xs-oc-4096mb-gtx-1650-ventus-xs-4g-oc/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, graphic_card_model)

    

def graphic_card_model(message):
    card = (state_check(message.from_user.id, 'graphic_card_price'))[0]
    
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
    
    ram_size = (state_check(message.from_user.id, 'ram_size'))[0]
    print(ram_size)
    
    if ram_size == '8':
        msg = bot.send_message(message.chat.id, '1.[Kingston DDR4 8G](https://telemart.ua/products/kingston-ddr4-8gb-3200mhz-fury-beast-black-kf432c16bb8/)\n 2.[GoodRAM DDR4 8GB](https://telemart.ua/products/goodram-ddr4-8gb-2400mhz-gr2400d464l17s8g/)\n 3.[Team DDR4 8GB](https://telemart.ua/products/team-ddr4-8gb-2400mhz-elite-ted48g2400c1601/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, ram_model)    
    elif ram_size == '16':
        msg = bot.send_message(message.chat.id, '1.[Patriot DDR4 16GB](https://telemart.ua/products/patriot-ddr4-16gb-2x8gb-4400mhz-viper-4-blackout-pvb416g440c8k/)\n 2.[G.Skill DDR4 16GB](https://telemart.ua/products/gskill-ddr4-16gb-2x8-3200mhz-ripjaws-v-black-f4-3200c15d-16gvk/)\n 3.[G.Skill DDR4 16GB](https://telemart.ua/products/gskill-ddr4-16gb-2x8gb-3200mhz-aegis-f4-3200c16d-16gis/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, ram_model)   
    elif ram_size == '32':
        msg = bot.send_message(message.chat.id, '1.[Kingston DDR5 32GB](https://telemart.ua/products/kingston-ddr5-32gb-2x16gb-5200mhz-fury-beast-black-kf552c40bbk2-32/)\n 2.[G.Skill DDR4 32GB](https://telemart.ua/products/gskill-ddr4-32gb-3200mhz-trident-z-rgb-f4-3200c15d-32gtzr/)\n 3.[Patriot DDR4 32GB](https://telemart.ua/products/patriot-ddr4-32gb-2x16gb-3000mhz-viper-4-blackout-pvb432g300c6k/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, ram_model)

    

    # bot.register_next_step_handler(msg, ram_model)



def ram_model(message):
    ram_size = (state_check(message.from_user.id, 'ram_size'))[0]
    
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
        medium = types.InlineKeyboardButton('2 тб (1 149 - 1 799)')
        good = types.InlineKeyboardButton('1 тб (1 149 - 1 799)')

        markup.add(good, medium)
        hdd_img = Image.open(r'D:\projects\Diplom\images\hdd.jpg') 
        msg = bot.send_photo(message.from_user.id, hdd_img ,'Что насчет памяти ?', reply_markup = markup)
        bot.register_next_step_handler(msg, memory_size)
   
   
    elif message.text == "SSD":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bad = types.InlineKeyboardButton('216 гб (819 - 929)')
        medium = types.InlineKeyboardButton('512 гб (1 584 - 3 879)')
        good = types.InlineKeyboardButton('1 тб (3 199 - 8 199)')

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

     
    memory = (state_check(message.from_user.id, 'memory_type'))[0]
    
    print(memory)
    
    if memory  == 'HDD':
        if "1 тб" in message.text:
            msg = bot.send_message(message.chat.id, '1.[Western Digital Blue 1TB](https://telemart.ua/products/western-digital-caviar-blue-1tb-64mb-7200rpm-35-wd10ezex/)\n 2.[Seagate BarraCuda 1TB](https://telemart.ua/products/seagate-barracuda-1tb-64mb-7200rpm-35-st1000dm010/)', reply_markup=markup, parse_mode='Markdown')
        elif "2 тб" in message.text:
            msg = bot.send_message(message.chat.id, '1.[Toshiba P300 2TB](https://telemart.ua/products/toshiba-p300-2tb-64mb-7200rpm-35-hdwd120uzsva/)\n 2.[Seagate BarraCuda 2TB](https://telemart.ua/products/seagate-barracuda-2tb-256mb-7200rpm-35-st2000dm008/)', reply_markup=markup, parse_mode='Markdown')
    elif memory == 'SSD':
        if "216 гб" in message.text:
            msg = bot.send_message(message.chat.id, '1.[Gigabyte 256GB 2.5](https://telemart.ua/products/gigabyte-256gb-25-gp-gstfs31256gtnd/)\n 2.[Patriot P210 256GB](https://telemart.ua/products/patriot-p210-256gb-25-p210s256g25/)\n 3.[Patriot Burst 240GB](https://telemart.ua/products/patriot-burst-tlc-120gb-25-pbu240gs25ssdr/)', reply_markup=markup, parse_mode='Markdown')
        elif "512 гб" in message.text:
            msg = bot.send_message(message.chat.id, '1.[Kingston FURY Renegade 3D](https://telemart.ua/products/kingston-fury-renegade-3d-nand-tlc-500gb-m2-2280-pci-e-nvme-x4-sfyrs500g/)\n 2.[Samsung 870 EVO V-NAND](https://telemart.ua/products/samsung-870-evo-v-nand-mlc-500gb-25-mz-77e500bw/)\n 3.[Patriot P300 512GB](https://telemart.ua/products/patriot-p300-512gb-m2-2280-pci-e-nvme-x4-p300p512gm28/)', reply_markup=markup, parse_mode='Markdown')
        elif "1 тб" in message.text:
            msg = bot.send_message(message.chat.id, '1.[Samsung 970 PRO V-NAND](https://telemart.ua/products/samsung-970-pro-v-nand-mlc-1tb-m2-2280-pci-e-mz-v7p1t0bw/)\n 2.[Corsair Force Series MP600](https://telemart.ua/products/corsair-force-series-mp600-gen4-3d-nand-tlc-1gb-m2-2280-pci-e-nvme-x4-cssd-f1000gbmp600/)\n 3.[Intel 660p 3D QLC 1TB](https://telemart.ua/products/intel-660p-3d-qlc-1tb-m2-2280-pci-e-nvme-x4-ssdpeknw010t8x1/)', reply_markup=markup, parse_mode='Markdown')
    
    bot.register_next_step_handler(msg, memory_model)    

def memory_model(message):
    insert_data(message.from_user.id, message.text, 'memory_model')

    block_img = Image.open(r'D:\projects\Diplom\images\block.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный (515 - 1 249)')
    medium = types.InlineKeyboardButton('Что-то среднее (1 499 - 2 199)')
    good = types.InlineKeyboardButton('Дорогой (2 639 - 5 549)')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, block_img ,'Что насчет блока питания ?'  , reply_markup = markup)
    
    bot.register_next_step_handler(msg, pc_power)        
    

def pc_power(message):
    insert_data(message.from_user.id, message.text, 'pc_power')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
 
    if  'Дорогой' in message.text:
        
        msg = bot.send_message(message.chat.id, '1.[CHIEFTEC Polaris 1050W](https://telemart.ua/products/chieftec-polaris-1050w-pps-1050fc/)\n 2.[Corsair RM750x 750W](https://telemart.ua/products/corsair-rm750x-750w-cp-9020179-eu/)\n 3.[Seasonic CORE GC 650W Gold](https://telemart.ua/products/seasonic-core-gc-650w-gold-ssr-650lc/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_power_model)
        
    elif 'Что-то среднее' in message.text:

        msg = bot.send_message(message.chat.id, '1.[Be Quiet! System Power 9 700W](https://telemart.ua/products/be-quiet-system-power-9-700w-bn248/)\n 2.[Gigabyte P750GM 750W](https://telemart.ua/products/gigabyte-p750gm-750w-gp-p750gm/)\n 3.[GAMEMAX RGB-550 550W](https://telemart.ua/products/gamemax-rgb-550-550w-rgb-550/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_power_model)
    elif 'Бюджетный' in message.text:

        msg = bot.send_message(message.chat.id, '1.[CHIEFTEC Force 500W](https://telemart.ua/products/chieftec-force-500w-cps-500s/)\n 2.[CHIEFTEC VALUE SERIES 400W OEM](https://telemart.ua/products/chieftec-value-series-400w-apb-400b8/)\n 3.[GAMEMAX 400W 120mm FAN](https://telemart.ua/products/gamemax-400w-120mm-fan-gm-400w-pfc/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_power_model)

    
def pc_power_model(message):
    insert_data(message.from_user.id, message.text, 'pc_power_model')

    pc_img = Image.open(r'D:\projects\Diplom\images\pc.jpg') 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bad = types.InlineKeyboardButton('Бюджетный (861 - 1 219)')
    medium = types.InlineKeyboardButton('Что-то среднее (1 356 - 2 537)')
    good = types.InlineKeyboardButton('Дорогой (3 076 - 5 606)')

    markup.row(good)
    markup.add(bad, medium)
    
    msg = bot.send_photo(message.from_user.id, pc_img, 'Что насчет корпуса ?'  , reply_markup = markup)
     
    

    
    bot.register_next_step_handler(msg, pc_case)    



def pc_case(message):
    insert_data(message.from_user.id, message.text, 'pc_case')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item = types.InlineKeyboardButton('1')
    item2 = types.InlineKeyboardButton('2')
    item3 = types.InlineKeyboardButton('3')
    markup.add(item, item2, item3)
 
    if  'Дорогой' in message.text:
        
        msg = bot.send_message(message.chat.id, '1.[Asus TUF Gaming GT501 ](https://telemart.ua/products/asus-tuf-gaming-gt501-rgb-bez-bp-90dc0012-b49000-black/)\n 2.[Fractal Design Define 7](https://telemart.ua/products/fractal-design-define-7-compact-light-tempered-glass-bez-bp-fd-c-def7c-04-white/)\n 3.[Thermaltake V250](https://telemart.ua/products/thermaltake-v250-argb-tempered-glass-bez-bp-ca-1q5-00m1wn-00-black/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_case_model)
        
    elif 'Что-то среднее' in message.text:

        msg = bot.send_message(message.chat.id, '1.[Thermaltake V200](https://telemart.ua/products/thermaltake-v200-rgb-tempered-glass-bez-bp-ca-1k8-00m1wn-01-black/)\n 2.[2E Gaming Hexagon](https://telemart.ua/products/2e-gaming-hexagon-2e-g338-black/)\n 3.[GAMEMAX Diamond ARGB](https://telemart.ua/products/gamemax-diamond-argb-tempered-glass-bez-bp-white/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_case_model)
    elif 'Бюджетный' in message.text:

        msg = bot.send_message(message.chat.id, '1.[1stPlayer V3-A-4G6](https://telemart.ua/products/1stplayer-v3-a-4g6-bez-bp-black/)\n 2.[1stPlayer F4-3R1](https://telemart.ua/products/1stplayer-f4-3r1-color-led-bez-bp-black/)\n 3.[GAMEMAX MT520-NP](https://telemart.ua/products/gamemax-mt520-np-bez-bp-gmmc683667-black/)', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(msg, pc_case_model)

def pc_case_model(message):
    insert_data(message.from_user.id, message.text, 'pc_case_model')
    
    processor_model = (state_check(message.from_user.id, 'processor_model'))[0]
    processor_link = (state_check(message.from_user.id, 'processor_link'))[0]
    motherboard_model = (state_check(message.from_user.id, 'motherboard_model'))[0]
    motherboard_model_link = (state_check(message.from_user.id, 'motherboard_link'))[0]
    graphic_card_model = (state_check(message.from_user.id, 'graphic_card_model'))[0]
    graphic_card_model_link = (state_check(message.from_user.id, 'graphic_card_link'))[0]
    ram_model = (state_check(message.from_user.id, 'ram_model'))[0]
    ram_link = (state_check(message.from_user.id, 'ram_link'))[0]
    memory_model = (state_check(message.from_user.id, 'memory_model'))[0]
    memory_link = (state_check(message.from_user.id, 'memory_link'))[0]

    pc_power_model = (state_check(message.from_user.id, 'pc_power_model'))[0]
    pc_case_model = (state_check(message.from_user.id, 'pc_case_model'))[0]



    
    
    results = f'''Ваша сборка :
Процессор: [{processor_model}]({processor_link})
Материнская плата: [{motherboard_model}]({motherboard_model_link})
Видеокарта: [{graphic_card_model}]({graphic_card_model_link})
ОЗУ: [{ram_model}]({ram_link})



    '''
    
    bot.send_message(message.from_user.id, results, parse_mode='Markdown')
    





bot.polling(none_stop = True, interval = 0)

