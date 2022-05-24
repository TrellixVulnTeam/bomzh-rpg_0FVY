import os
import json
import requests
from datetime import datetime, date

from app_token import *
from app_dict import *
from app_image_compose import getBomzhPic, getBandaPic

from flask import Flask, request, send_file 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)

#------------------------------------------------------------------ Версия приложения
VERSIA = '0.0.a'

#------------------------------------------------------------------ Получение URL NGROK 
try:
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    with open('tunnels.json') as data_file:    
        ngrok_datajson = json.load(data_file)

    os.system('cls')
    NGROK_URL = ngrok_datajson['tunnels'][0]['public_url']
except:
    os.system('cls')
    print('='*16 + "ERORR" + '='*16)
    NGROK_URL = "NONE"

#------------------------------------------------------------------ Литералы для статусов 
STATE = {
    1 : 'Свободен',
    2 : 'На работе',
    3 : 'Отдыхает',
    4 : 'Тяжело ранен',
    5 : 'Закончил работу',
}


class Control():
    
    def __init__(self, react, func):
        self.react = react
        self.func = func


class Req():

    def __init__(self, r):

        def get_user(user_id, chat_id, username=None):
            user = User.query.filter_by(id = user_id).first()
            if user == None:
                print("Нет такого юзера ----------------------------------------- СОЗДАНИЕ НОВОГО")
                new_user = User(id=user_id, username = username, chat_id = chat_id)

                alpha_s = StatusAnable(user_id=new_user.id, status_id = 3)

                db.session.add(alpha_s)
                db.session.add(new_user)
                db.session.commit()

                user = User.query.filter_by(id = user_id).first()
                return user
            else:
                return user

        try:
            if 'message' in r.keys():
                self.type = 'msg'
                print("--------> - - REQ TYPE : msg")

                self.chat_id = r['message']['chat']['id']
                print("--------> - - CHAT ID :", self.chat_id)

                self.user_id = r['message']['from']['id']
                print("--------> - - USER ID :", self.user_id)

                self.date = r['message']['date']
                print("--------> - - MSG DATE :", datetime.fromtimestamp(self.date).strftime('%Y-%m-%d %H:%M:%S'))

                self.data = r['message']['text']
                print("--------> - - DATA :", self.data)

                data_keys = self.data.split()

                self.query = data_keys[0]
                print("--------> - - DATA QUERY :", self.query)

                self.keys = data_keys[1:]
                print("--------> - - DATA KEYS :", self.keys)

                if 'username' in r['message']['from'].keys():
                    self.username = r['message']['from']['username']
                    print("--------> - - USERNAME :", self.username)
                else:
                    self.username = None
                    print("--------> - - USERNAME :", self.username)

                self.user = get_user(self.user_id, self.chat_id, self.username)
                print("--------> - - USER OBJ :", self.user)

            elif 'callback_query' in r.keys():
                self.type = 'callback'
                print("--------> - - REQ TYPE : callback")

                self.chat_id = r['callback_query']['message']['chat']['id']
                print("--------> - - CHAT ID :", self.chat_id)

                self.user_id = r['callback_query']['from']['id']
                print("--------> - - USER ID :", self.user_id)

                self.date = r['callback_query']['message']['date']
                print("--------> - - MSG DATE :", datetime.fromtimestamp(self.date).strftime('%Y-%m-%d %H:%M:%S'))

                self.data = r['callback_query']['data']
                print("--------> - - DATA :", self.data)

                data_keys = self.data.split()

                self.query = data_keys[0]
                print("--------> - - DATA QUERY :", self.query)

                self.keys = data_keys[1:]
                print("--------> - - DATA KEYS :", self.keys)

                if 'username' in r['callback_query']['from'].keys():
                    self.username = r['callback_query']['from']['username']
                    print("--------> - - USERNAME :", self.username)
                else:
                    self.username = None
                    print("--------> - - USERNAME :", self.username)

                self.user = get_user(self.user_id, self.chat_id, self.username)
                print("--------> - - USER OBJ :", self.user)

            elif 'new_chat_participant' in r.keys():
                self.type = 'error'
                print("--------> - - REQ TYPE : add to chat")
                print(r['message']['chat']['id'])

            else:
                self.type = 'error'
                print("--------> - - REQ TYPE : not interacteble")
        except Exception as e: 
            print("="*32)
            print("ERROR : ", e)
            print('-'*32)
            print(r)

class GEN():

    def __init__(self):
        self.gen_str = ""
        self.gen = []

        for i in range(16):
            new_part = random.randint(0, 256)
            self.gen_str += str(new_part) + "-"
            self.gen.append(new_part)

        self.gen_str[:-1]

    def __str__(self):
        return self.gen_str

#---------------------------------------------------------
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<status #{} : {}>'.format(self.id, self.line)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    chat_id = db.Column(db.String(250), unique=False, nullable=False)
    money = db.Column(db.Integer, unique=False, nullable=False, default=300)
    gold = db.Column(db.Integer, unique=False, nullable=False, default=10)
    is_prime = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    prime_long = db.Column(db.Integer, unique=False, nullable=True, default=None)
    prime_start_date = db.Column(db.DateTime, unique=False, nullable=True)
    lvl = db.Column(db.Integer, unique=False, nullable=False, default=0)
    status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True, default=None)
    bomzhs_anable = db.Column(db.Integer, unique=False, nullable=False, default=2)
    invetory_size = db.Column(db.Integer, unique=False, nullable=False, default=500)
    last_update = db.Column(db.DateTime, unique=False, nullable=True)
    last_action = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return '<User #{}>'.format(self.id)

class StatusAnable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))


class Bomzh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), unique=False, nullable=False)
    gen = db.Column(db.String(250), unique=False, nullable=False)

    lvl = db.Column(db.Integer, unique=False, nullable=False, default=1)
    exp_next_lvl = db.Column(db.Integer, unique=False, nullable=False, default=500)
    exp = db.Column(db.Integer, unique=False, nullable=False, default=0)

    hp = db.Column(db.Integer, unique=False, nullable=False, default=30)
    hp_max = db.Column(db.Integer, unique=False, nullable=False, default=100)

    energy = db.Column(db.Integer, unique=False, nullable=False, default=3)
    energy_max = db.Column(db.Integer, unique=False, nullable=False, default=3)

    joy = db.Column(db.Integer, unique=False, nullable=False, default=50)
    joy_max = db.Column(db.Integer, unique=False, nullable=False, default=100)

    hungry = db.Column(db.Integer, unique=False, nullable=False, default=3)
    hungry_max = db.Column(db.Integer, unique=False, nullable=False, default=5)

    state = db.Column(db.Integer, unique=False, nullable=False, default=1)

    work_location = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=True)

    last_eate = db.Column(db.DateTime, unique=False, nullable=True)
    last_work = db.Column(db.DateTime, unique=False, nullable=True)
    last_update = db.Column(db.DateTime, unique=False, nullable=True)

    pic_url = db.Column(db.String(250), unique=False, nullable=False)
    pic_clean_url = db.Column(db.String(250), unique=False, nullable=False)
    pic_set_url = db.Column(db.String(250), unique=False, nullable=True)

    is_dead = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    
    def __repr__(self):
        return '<Bomzh #{} user#{}>'.format(self.id, self.user_id)

    def cheak_user(self, user):
        if self.user_id == user.id:
            return True
        else:
            return False

    def cheak_state(self):
        if self.state == 1:
            return True
        else:
            return False

    def cheak_energy(self, energy):
        if self.energy >= energy:
            return True
        else:
            return False

    def add_energy(self, energy):
        self.energy += energy

        if self.energy > self.energy_max:
            self.energy = self.energy_max
        elif self.energy < 0:
            self.energy = 0

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    disc = db.Column(db.String(250), unique=False, nullable=True)
    lvl_cup = db.Column(db.Integer, unique=False, nullable=False, default=1)
    is_pve = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    work_time = db.Column(db.Integer, unique=False, nullable=False, default=4)
    energy_lost = db.Column(db.Integer, unique=False, nullable=False, default=1)
    chance = db.Column(db.Integer, unique=False, nullable=False, default=50)
    chance_max = db.Column(db.Integer, unique=False, nullable=False, default=50)
    chance_extra = db.Column(db.Integer, unique=False, nullable=False, default=50)
    chance_extra_max = db.Column(db.Integer, unique=False, nullable=False, default=50)
    money_drop = db.Column(db.Integer, unique=False, nullable=False, default=0)
    gold_drop = db.Column(db.Integer, unique=False, nullable=False, default=0)
    exp_drop = db.Column(db.Integer, unique=False, nullable=False, default=0)
    joy_drop = db.Column(db.Integer, unique=False, nullable=False, default=0)
    joy_lost = db.Column(db.Integer, unique=False, nullable=False, default=0)
    hp_lost = db.Column(db.Integer, unique=False, nullable=False, default=0)

    def __repr__(self):
        return '<Location #{}>'.format(self.name)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)

class SubType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    disc = db.Column(db.String(250), unique=False, nullable=True)
    t = db.Column(db.Integer, db.ForeignKey('type.id'), unique=False, nullable=False)
    sub_t = db.Column(db.Integer, db.ForeignKey('sub_type.id'), unique=False, nullable=True)
    tir = db.Column(db.Integer, unique=False, nullable=True, default=1)
    # -------
    wep_dmg = db.Column(db.Integer, unique=False, nullable=True, default=1)
    wep_ac = db.Column(db.Integer, unique=False, nullable=True, default=1)
    wep_crit_s = db.Column(db.Integer, unique=False, nullable=True, default=1)
    wep_crit_c = db.Column(db.Integer, unique=False, nullable=True, default=1)
    # wep_mod = 

    armor_dmg = db.Column(db.Integer, unique=False, nullable=True, default=1)
    # armor_mod = 

    food_eat = db.Column(db.Integer, unique=False, nullable=True, default=1)
    food_joi = db.Column(db.Integer, unique=False, nullable=True, default=1)

    # -------
    is_seteble = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_useble = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_sell = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    price = db.Column(db.Integer, unique=False, nullable=False, default=0)
    price_gold = db.Column(db.Integer, unique=False, nullable=False, default=0)

    def __repr__(self):
        return '<Item #{} - {}>'.format(self.id, self.name)

class LocDrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc_finish = db.Column(db.Integer, db.ForeignKey('location.id'), unique=False, nullable=False)
    item = db.Column(db.Integer, db.ForeignKey('item.id'), unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False, default=10)
    count_rnd = db.Column(db.Integer, unique=False, nullable=False, default=10)
    item_drop_chance = db.Column(db.Integer, unique=False, nullable=False, default=10)
    is_extra = db.Column(db.Boolean, unique=False, nullable=False, default=False)

#-------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def set_web_hook(): # Функция установки веб хука
    method = "setWebhook"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = {
        "url": NGROK_URL
    }
    print("............................................")
    print(NGROK_URL)
    print("............................................")
    requests.post(url, data=data)

def send_msg(chat_id, text=None, photo=None, buttons=None): # Функция отправки сообщения
    if photo == None:
        method = "sendMessage"
    else:
        method = "sendPhoto"

    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    
    if buttons!=None:
        buttons_array = []
        lines_c = 0
        for lines in buttons:
            buttons_array.append([])
            for button in lines:
                buttons_array[lines_c].append({
                    "text":button[0],
                    "callback_data":button[1]
                })
            lines_c +=1  

        b = {
            "inline_keyboard": []
        }

        b["inline_keyboard"] = buttons_array

    if photo!=None:
        pic_url = NGROK_URL + '/get_image/' + photo

    if photo == None:
        data = {
            "chat_id": chat_id,
            "text": text, 
            "parse_mode":'HTML',
            "reply_markup": json.dumps(b, separators=(',', ':'))
        }
    else:
        data = {
            "chat_id": chat_id,
            "photo": pic_url,
            "caption": text, 
            "parse_mode":'HTML',
            "reply_markup": json.dumps(b, separators=(',', ':'))
        }
        
    requests.post(url, data=data)

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
def func_info(req): # ОКНО ИНФОРМАЦИИ
    send_msg(
        chat_id = req.chat_id, 
        text = MSG_INFO.format(VERSIA),
        buttons=[
            [
                ["📋 Меню","/menu"],["🔎 Список команд","/help"]
            ],
            [
                ["⚙️ Тех. поддержка","/support"]
            ]
        ]
    )

def func_menu(req): # ОКНО МЕНЮ

    if req.user.is_prime : # если пользователь имеет прийм статус 
        status = 'Премиум' # устанавливает основой индификатор
        add_text = '' # устанавливаем вспомогательный текст
    else:
        status = 'Бомж' # устанавливает основой индификатор
        add_text = "(Узнать что дает ПРЕМИУМ --> /prime_info)" # устанавливаем вспомогательный текст

    if req.user.status: # установка звания
        u_status = Status.query.filter_by(id = req.user.status).first().line # звание из БД
    else:
        u_status = "Обычный" # если звание еще не установлено
    
    bomzh_obj_list = Bomzh.query.filter_by(user_id=req.user.id) # список бомжей пользователя
    bomzh_obj_list_c = Bomzh.query.filter_by(user_id=req.user.id).count() # количество бомжей в списке

    if req.user.username == None: # Форматируем сообщение. Если нет username' ставаим надпись "Пользователь #ID"
        MSG = MSG_MENU.format("Пользователь #" + str(req.user.id), u_status , req.user.lvl, status, add_text, req.user.money, req.user.gold, bomzh_obj_list_c)
    else:
        MSG = MSG_MENU.format(req.user.username, u_status , req.user.lvl, status, add_text, req.user.money, req.user.gold, bomzh_obj_list_c)
    
    for bomzh in bomzh_obj_list: # добавляем строчки с именами бомжей в сообщение 
        MSG += "\t\t - {}\n".format(bomzh.name)


    send_msg(
        chat_id = req.chat_id, 
        text = MSG,
        buttons=[
            [["🎖 Сменить звание","/status"], ["👑  Сменить статус","/prime"]],
            [["💸  Пополнить баланс","/balans"]],
            [["📦  Инвентарь","/inventory"]],
            [["👥  Банда","/banda"]],
            [["⚙️  Настройки","/settings"],["🛠️  DEVLOG","/dev"]],
        ]
    )

def func_support(req): #ХУЙ
    send_msg(
        chat_id = req.chat_id, 
        text = "SOON",
        buttons=[
        ]
    )

def func_dev(req): #ХУЙ
    send_msg(
        chat_id = req.chat_id, 
        text = "DEVLOG ----> https://t.me/plodovo_yagodniu",
        buttons=[
        ]
    )

def func_banda(req):
    bomzh_obj_list = Bomzh.query.filter_by(user_id=req.user.id)

    buttons=[]
    banda_power = 0

    for bomzh in bomzh_obj_list:
        buttons.append([[bomzh.name + f" [{STATE[bomzh.state]}]", "/bomzh "+ str(bomzh.id)]])
        banda_power += bomzh.lvl

    if req.user.bomzhs_anable >= 1:
        buttons.append([["▶️  Получить нового бомжа", "/get_bomzh"]])
    buttons.append([["📋 Меню","/menu"]])

    send_msg(
        chat_id = req.chat_id, 
        photo = getBandaPic(req.user.id, bomzh_obj_list [:5])+"?v={}".format(random.randint(1, 1000000)),
        text = MSG_BANDA.format(req.user.id, banda_power, req.user.bomzhs_anable),
        buttons=buttons
    )

def func_get_bomzh(req):
    user = req.user
    anable = req.user.bomzhs_anable
    if anable >= 1:
        new_bomzh_name = genName()
        gen = GEN()
        print(gen)
        bomzh_pics = getBomzhPic(gen.gen, new_bomzh_name)
        new_bomzh = Bomzh(user_id=user.id, name=new_bomzh_name, gen=gen.gen_str, pic_url=bomzh_pics[1], pic_clean_url=bomzh_pics[0])
        user.bomzhs_anable -= 1
        db.session.add(new_bomzh)
        db.session.commit()
        send_msg(
            chat_id = req.chat_id, 
            photo = new_bomzh.pic_url, 
            text = MSG_BOMZH_GET.format(new_bomzh.gen),
            buttons = [
                [["🔍 Подробнее",f"/bomzh {new_bomzh.id}"]],
                [["👥  Банда","/banda"]],
                [["📋  Меню","/menu"]]
            ]
        )
    else:
        send_msg(
            chat_id = req.chat_id, 
            text = MSG_BANDA_ERROR_GET,
            buttons = [
                [["👥  Банда","/banda"]],
                [["📋  Меню","/menu"]]
            ]
        )

def func_bomzh(req):
    bomzh_id = int(req.keys[0])

    bomzh = Bomzh.query.filter_by(id=bomzh_id).first()

    buttons = []

    if bomzh.state == 1:
        buttons.append([["🍖 Покормить",f"/feed {bomzh_id}"] , ["🛏 Одыхать",f"/rest {bomzh_id}"]])
        if bomzh.energy > 0:
            buttons.append([["🧰 Отправить на работу",f"/work {bomzh_id}"]])
    buttons.append([["🎱 Класс",f"/class {bomzh_id}"],["💫 Умения",f"/skills {bomzh_id}"]])
    buttons.append([["📦 Снаряжение",f"/items {bomzh_id}"]])
    buttons.append([["💳 Продать бомжа",f"/sell {bomzh_id}"]])
    buttons.append([["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]])

    send_msg(
        chat_id = req.chat_id, 
        photo = bomzh.pic_url,
        text = MSG_BOMZH.format(
            bomzh.name, 
            bomzh_id, 
            STATE[bomzh.state],
            bomzh.gen,
            bomzh.lvl, 
            bomzh.exp,
            bomzh.exp_next_lvl, 
            bomzh.hp,
            bomzh.hp_max,
            bomzh.joy,
            bomzh.joy_max,
            bomzh.hungry, 
            bomzh.hungry_max,
            bomzh.energy,
            bomzh.energy_max,
        ),
        buttons = buttons
    )

def func_inventory(req):
    send_msg(
        chat_id = req.chat_id, 
        text = MSG_INVENTORY,
        buttons=[
            [["📋 Меню","/menu"]]
        ]
    )

def func_prime(req):
    send_msg(
        chat_id = req.chat_id, 
        text = MSG_PRIME,
        buttons=[
            [["📋 Меню","/menu"]]
        ]
    )

def func_status(req): # Выбор статуса
    anable_status_list = StatusAnable.query.filter_by(user_id=req.user.id)
    
    buttons = []

    for anable_status in anable_status_list:
        status = Status.query.filter_by(id=anable_status.status_id).first()
        buttons.append([[status.line,"/setstatus " + str(status.id)]])

    buttons.append([["📋 Назад в меню","/menu"]])

    send_msg(
        chat_id = req.chat_id, 
        text = MSG_STATUS,
        buttons=buttons
    )

def func_setstatus(req): # Установка статуса
    if StatusAnable.query.filter_by(user_id=req.user.id, status_id=req.keys[0]).first():
        req.user.status = req.keys[0]
        db.session.commit()
        send_msg(
            chat_id = req.chat_id, 
            text = "✅ Звание установлено",
            buttons=[
                [["📋 Меню","/menu"]]
            ]
        )
    else:
        send_msg(
            chat_id = req.chat_id, 
            text = "🆘 Звание не установлено, у вас нет прав на его установку",
            buttons=[
                [["📋 Меню","/menu"]]
            ]
        )

#========================== Отправка на работу бомжа
def func_work(req):
    if len(req.keys) == 0: # --- Скрытая функция /work
        bomzh_free_obj_list = Bomzh.query.filter_by(user_id=req.user.id, state=1)

        buttons = []
        for bomzh in bomzh_free_obj_list:
            buttons.append([[bomzh.name,"/work "+str(bomzh.id)]])

        buttons.append([["📋 Меню","/menu"]])

        send_msg(
            chat_id = req.chat_id, 
            text = "<b>Какого бомжа отправим на работу ?</b>",
            buttons=buttons
        )

    if len(req.keys) == 1: # --- /work [bomzh_id]
        bomzh = Bomzh.query.filter_by(id=req.keys[0]).first()

        if bomzh.user_id == req.user_id:

            buttons=[]
            msg = MSG_WORK

            if bomzh.state == 1:

                location_obj_list = Location.query.all()

                for location in location_obj_list:
                    if location.lvl_cup <= bomzh.lvl:
                        ht = location.work_time // 60
                        mt = location.work_time % 60

                        control_path = "/work " + str(bomzh.id) + " " + str(location.id)

                        if location.is_pve == True:
                            btn_text = location.name + " [PVE]"
                        else:
                            btn_text = location.name + " [PVP]"

                        if ht > 0 :
                            btn_text += " [ {}ч. {}м. ]".format(ht,mt)
                        else:
                            btn_text += " [ {}м. ]".format(mt)

                        buttons.append([[btn_text,control_path]])

                send_msg(
                    chat_id = req.chat_id, 
                    text = msg ,
                    buttons=buttons
                )
            else:
                send_msg(
                    chat_id = req.chat_id, 
                    text = f"Вы не можете отправить этого бомжа на работу. Он {STATE[bomzh.state]}",
                    buttons=[
                        [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                    ]
                )
        else:
            send_msg(
                chat_id = req.chat_id, 
                text = "Этот бомж не состоит в твоей банде",
                buttons=[
                    [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                ]
            )

    # ----------------------------------------------------
    if len(req.keys) == 2: # --- /work [bomzh_id] [loc_id]

        bomzh = Bomzh.query.filter_by(id=req.keys[0]).first() # Получаем бомжа по id из аргумента запроса

        if bomzh.cheak_user(req.user): # Пренадлижит ли бомж пользователю
            if bomzh.cheak_state: # Если бомж свободен

                location = Location.query.filter_by(id=req.keys[1]).first() # Получаем локацию по id из аргумента запроса

                if location.lvl_cup <= bomzh.lvl: # Если лвл кап локации меньше уровня бомжа
                    if bomzh.cheak_energy(location.energy_lost): # Если бомжу хватает энергии на данную локацию

                        bomzh.state = 2 
                        bomzh.work_location = location.id
                        bomzh.last_work = datetime.now()
                        bomzh.add_energy(-location.energy_lost)
                        db.session.commit()
                        
                        send_msg(
                            chat_id = req.chat_id, 
                            text = "✅ Бомж отправлен на работу",
                            buttons=[
                                [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                            ]
                        )

                    else:
                        send_msg(
                            chat_id = req.chat_id, 
                            text = f"Вы не можете отправить этого бомжа на работу. У него закончилась энергия",
                            buttons=[
                                [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                            ]
                        )
                else:
                    send_msg(
                        chat_id = req.chat_id, 
                        text = f"Вы не можете отправить этого бомжа на работу. У вашего бомжа слишком низкий уровень",
                        buttons=[
                            [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                        ]
                    )
            else:
                send_msg(
                    chat_id = req.chat_id, 
                    text = f"Вы не можете отправить этого бомжа на работу. Он {STATE[bomzh.state]}",
                    buttons=[
                        [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                    ]
                )
        else:
            send_msg(
                chat_id = req.chat_id, 
                text = "Этот бомж не состоит в твоей банде",
                buttons=[
                    [["⏪  Назад к банде","/banda"],["📋 Меню","/menu"]]
                ]
            )

#========================== Кормёжка бомжа
def func_feed(req):
    if len(req.keys) == 1:
        bomzh = Bomzh.query.filter_by(id=req.keys[0]).first()

        send_msg(
            chat_id = req.chat_id, 
            text = MSG_FEED,
            buttons=[
                [["⏪  Назад к банде","/banda"]],
                [["📋 Меню","/menu"]]
            ]
        )

def func_endwork(req):
    if len(req.keys) == 1:
        bomzh = Bomzh.query.filter_by(id=req.keys[0]).first()

        if bomzh.state == 5:
            location = Location.query.filter_by(id=bomzh.work_location).first()

            if random.randint(1, location.chance_max) <= location.chance:
                bomzh.exp += 120
                bomzh.state = 1
                bomzh.is_work= False

                db.session.commit()

                send_msg(
                    chat_id = req.chat_id, 
                    text = MSG_WORK_OK,
                    buttons=[
                        [["⏪  Назад к банде","/banda"]],
                        [["📋 Меню","/menu"]]
                    ]
                )
                
            else:
                bomzh.hp -= 10
                bomzh.state = 1
                bomzh.is_work= False

                db.session.commit()

                send_msg(
                    chat_id = req.chat_id, 
                    text = MSG_WORK_ERROR,
                    buttons=[
                        [["⏪  Назад к банде","/banda"]],
                        [["📋 Меню","/menu"]]
                    ]
                )


            
        else:
            send_msg(
                chat_id = req.chat_id, 
                text = "божм еще не закончил работу",
                buttons=[
                    [["⏪  Назад к банде","/banda"]],
                    [["📋 Меню","/menu"]]
                ]
            )


#-----------------------------------------------------------------------------------------------------------------------------
#
CONTROL_SET = [
    Control(
        react="/info",
        func = func_info
    ),

    Control(
        react="/start",
        func = func_info
    ),

    Control(
        react="/menu",
        func = func_menu
    ),

    Control(
        react="/support",
        func = func_support
    ),

    Control(
        react="/dev",
        func = func_dev
    ),

    Control(
        react="/banda",
        func = func_banda
    ),

    Control(
        react="/get_bomzh",
        func = func_get_bomzh
    ),

    Control(
        react="/bomzh",
        func = func_bomzh
    ),

    Control(
        react="/inventory",
        func = func_inventory
    ),

    Control(
        react="/prime",
        func = func_prime
    ),

    Control(
        react="/status",
        func = func_status
    ),

    Control(
        react="/setstatus",
        func = func_setstatus
    ),

    Control(
        react="/work",
        func = func_work
    ),

    Control(
        react="/feed",
        func = func_feed
    ),
    
    Control(
        react="/endwork",
        func = func_endwork
    ),
]

#Выбор функции обработки команды
def logicControler(req):# req - <Req> объект
    if req.type != 'error':# Если сообщение правильного типа
        for control in CONTROL_SET:
            if req.query == control.react:# Выбор управляющего обекта
                try:
                    control.func(req)# Передача обработки
                except Exception as e:
                    print("--------> - - ERROR : \n\t\t\t", e)

#Оброботка веб-хука с бота
@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":# Проверка на метод
        print("====================================================")

        new_req = Req(request.json)# Создание объект запроса
        logicControler(new_req)# Передача запроса на обработку  

        return {"ok": True}# Ответ для Telegram
    else:
        return {"ok": False}# Ответ для Telegram
    
#Организация доступа к картинкам через URL (потому побитовая отправка картинок какого то х** не работает)
#работа с версиями 
@app.route('/get_image/<path:pic>')
def get_image(pic):
    filename = pic
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    set_web_hook() # Для работы NGROK устанавливаем web hook
    print(' * WEBHOOK SET')
    app.run(debug=True)