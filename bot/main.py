	# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# TODO добавить payeer https://payeercom.docs.apiary.io/#reference/0/creating-an-invoice-for-payment
import subprocess
import asyncio
import datetime
import checker as ckr
import shutil
import multiprocessing
import io
import traceback
import codecs
from telebot import formatting
import sys
from decimal import Decimal
from zipfile import ZipFile
from threading import Thread
import random
import time
import requests as r
import telebot
import os
from telebot import types
from pyCryptomusAPI import pyCryptomusAPI
import settings as s
import json
from bs4 import BeautifulSoup

print(s.token)
bot = telebot.TeleBot(s.token)
print(bot.get_me().username)
client = pyCryptomusAPI(merchant_uuid=s.merchant_uuid(), payment_api_key=s.payment_api())  # Merchand UUID

ref_list = []

msg_to_del = {}

back_capi_m = telebot.types.InlineKeyboardMarkup()
back_c_b = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["capi_button"])
back_capi_m.add(back_c_b)

back_adm_markup = telebot.types.InlineKeyboardMarkup()
back_adm1 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["admin_panel"])
back_adm_markup.add(back_adm1)

back_ref_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
back_ref_btn = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["ref_button"])
back_ref_markup.add(back_ref_btn)

ref_markup = telebot.types.InlineKeyboardMarkup()
ref_markup.row_width = 2
ref_btn1 = types.InlineKeyboardButton(s.language["ref_stats"], callback_data=s.language["ref_stats"])
ref_btn2 = types.InlineKeyboardButton(s.language["ref_withdraw"], callback_data=s.language["ref_withdraw"])
ref_btn3 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["menu_button"], row_width=2)
ref_markup.add(ref_btn1, ref_btn2, ref_btn3)

back_smm_markup = telebot.types.InlineKeyboardMarkup()
backbtn_1 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["smm_button"])
back_smm_markup.add(backbtn_1)

back_shop_markup = telebot.types.InlineKeyboardMarkup()
backbtn_1 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["shop_button"])
back_shop_markup.add(backbtn_1)

topup_markup = telebot.types.InlineKeyboardMarkup()
topupbtn_1 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
topup_markup.add(topupbtn_1)
currency_markup = telebot.types.InlineKeyboardMarkup()
currencybtn_1 = types.InlineKeyboardButton('🅱 BTC', callback_data='cryptoselect BTC')
currencybtn_2 = types.InlineKeyboardButton('💎 LTC', callback_data='cryptoselect LTC')
currencybtn_3 = types.InlineKeyboardButton('🔥USDT (TRC-20)🔥', callback_data='cryptoselect USDT TRON')
currencybtn_8 = types.InlineKeyboardButton('USDT (BEP-20)', callback_data='cryptoselect USDT BSC')
currencybtn_4 = types.InlineKeyboardButton('BNB BEP-20', callback_data='cryptoselect BNB')
currencybtn_5 = types.InlineKeyboardButton('USDT (ERC-20)', callback_data='cryptoselect USDT ETH')
currencybtn_6 = types.InlineKeyboardButton('💎TON', callback_data='cryptoselect TON')
currencybtn_7 = types.InlineKeyboardButton('TRX TRC-20', callback_data='cryptoselect TRX')
currencybtn_9 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
currency_markup.add(currencybtn_1, currencybtn_3, currencybtn_8, currencybtn_4, currencybtn_5, currencybtn_6, currencybtn_7, row_width=2)
currency_markup.add(currencybtn_9, row_width=1)

choose_api_markup = telebot.types.InlineKeyboardMarkup()
ca_btn1 = telebot.types.InlineKeyboardButton(s.language["smm_api"], callback_data=s.language["smm_api"])
ca_btn2 = telebot.types.InlineKeyboardButton(s.language["cryptomus_api"], callback_data=s.language["cryptomus_api"])
ca_btn3 = telebot.types.InlineKeyboardButton(s.language["e_channel"], callback_data=s.language["e_channel"])
ca_btn5 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["admin_panel"])
choose_api_markup.add(ca_btn1, ca_btn2, ca_btn3)
choose_api_markup.add(ca_btn5, row_width=1)

admin_markup = telebot.types.InlineKeyboardMarkup()
lite_admmarkup = telebot.types.InlineKeyboardMarkup()
adminbtn_1 = types.InlineKeyboardButton(s.language["give_b"], callback_data=s.language["give_b"])
adminbtn_2 = types.InlineKeyboardButton(s.language["look_orders"], callback_data=s.language["look_orders"])
adminbtn_3 = types.InlineKeyboardButton(s.language["get_payments"], callback_data=s.language["get_payments"])
adminbtn_4 = types.InlineKeyboardButton(s.language["manage_refs"], callback_data=s.language["manage_refs"])
adminbtn_5 = types.InlineKeyboardButton(s.language["manage_tokens"], callback_data=s.language["manage_tokens"])
adminbtn_8 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["menu_button"])
adminbtn_9 = types.InlineKeyboardButton(s.language["capi_button"], callback_data=s.language["capi_button"])
adminbtn_10 = types.InlineKeyboardButton(s.language["admin_enter_support"], callback_data=s.language["admin_enter_support"])
adminbtn_11 = types.InlineKeyboardButton(s.language["change_wm_button"], callback_data=s.language["change_wm_button"])
adminbtn_12 = types.InlineKeyboardButton(s.language["change_permissions"], callback_data=s.language["change_permissions"])
adminbtn_13 = types.InlineKeyboardButton(s.language["transfer_data"], callback_data=s.language["transfer_data"])
adminbtn_14 = telebot.types.InlineKeyboardButton(s.language["cbot_token"], callback_data=s.language["cbot_token"])
admin_markup.add(adminbtn_1, adminbtn_2, adminbtn_3, adminbtn_4, adminbtn_5, adminbtn_9, adminbtn_10, adminbtn_11, adminbtn_12, adminbtn_13, adminbtn_14)
admin_markup.add(adminbtn_8, row_width=1)
lite_admmarkup.add(adminbtn_1, adminbtn_2, adminbtn_3, adminbtn_4, adminbtn_9, adminbtn_10, adminbtn_11, adminbtn_12, adminbtn_13)
lite_admmarkup.add(adminbtn_8, row_width=1)

manage_t_markup = telebot.types.InlineKeyboardMarkup()
manage_t_btn1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["manage_tokens"])
manage_t_markup.add(manage_t_btn1)
change_p_markup = telebot.types.InlineKeyboardMarkup()
change_p_btn = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["change_permissions"])
change_p_markup.add(change_p_btn)

manage_r_markup = telebot.types.InlineKeyboardMarkup()
manage_r_btn1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["manage_refs"])
manage_r_markup.add(manage_r_btn1)

back_markup = telebot.types.InlineKeyboardMarkup()
back_btn = telebot.types.InlineKeyboardButton(s.language['back_to_directories'], callback_data=s.language['smm_button'])
back_markup.add(back_btn)

shop_markup = types.InlineKeyboardMarkup()
shopbtn_1 = types.InlineKeyboardButton(s.language['back_to_shop'], callback_data=s.language['back_to_shop'])
shop_markup.add(shopbtn_1)

choose_type_of_orders_markup = types.InlineKeyboardMarkup(row_width=2)
orders_button_1 = types.InlineKeyboardButton(s.language['shop_orders_button'], callback_data=s.language['shop_orders_button'])
orders_button_2 = types.InlineKeyboardButton(s.language['smm_orders_button'], callback_data=s.language['smm_orders_button'])
orders_button_3 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
choose_type_of_orders_markup.add(orders_button_2, orders_button_3)

enter_amount_markup = types.InlineKeyboardMarkup()
cryptobtn_1 = types.InlineKeyboardButton(s.language['back_to_crypto'], callback_data=s.language['back_to_crypto'])
enter_amount_markup.add(cryptobtn_1)

currency_dict = {}
topup_process_users = []
buying_process_users_q = {}
smm_buying_process = {}
admin_regime = ''
waiting_order = {}

def _init_bot():
    docs = ["ref_p.txt", "balance.json", "payments.json", "orders.json", "stats.json", "refferals.json", "ref_stats.json", "saved_smm.json", "networks.json", "smm_orders.json", "settings.json"]

    with open("start_smm", "w") as f:
        f.write("#!/bin/bash\n\n")

    tokens = []
    for tok_raw in _admin_get_tokens().values():
        [tokens.append(token) for token in tok_raw if token not in tokens]

    for token in tokens:
        try:
            os.mkdir(f"/home/ubuntu/{token}")
        except Exception as exc:
            print(exc.args)
    
        for document in docs:
            if document not in os.listdir(f"/home/ubuntu/{token}"):
                with open(f"/home/ubuntu/{token}/{document}", "w") as f:
                    if document == "networks.json":
                        f.write('{"telegram": [], "instagram": [], "tiktok": [], "youtube": [], "facebook": [], "twitter": []}')
                    elif document == "settings.json":
                       for uid, toks in _admin_get_tokens().items():
                           for tok in toks:
                               if tok == token and uid.isdigit(): 
                                   adms_dict = {"support": "setup in settings", "admins": [int(uid)], "cryptomus": ["123", "123"], "smm_api": "", "channel": ["-1001668180838", "https://t.me/+4wi38VIJbW4wOGEx"], "allowed": []}
                                   f.write(json.dumps(adms_dict))
                    elif document == "ref_p.txt":
                        f.write("0.07 0.04 0.02")
                    else:
                        f.write("{}")

        try:
            os.remove(f"home/ubuntu/{token}/main.py")
        except Exception as exc:
            pass   
     
        try:
            shutil.copy("/home/ubuntu/bot/main.py", f"/home/ubuntu/{token}/main.py")
        except:
            pass

        try:
            shutil.copy("/home/ubuntu/bot/checker.py", f"/home/ubuntu/{token}/checker.py")
        except Exception as exc:
            pass

        try:
            shutil.copy("/home/ubuntu/bot/welcome_settings.json", f"/home/ubuntu/{token}/welcome_settings.json")
        except Exception as exc:
            pass

        try:
            os.remove(f"/home/ubuntu/{token}/settings.py")
        except:
            pass

        try:
            shutil.copy("/home/ubuntu/bot/settings.py", f"/home/ubuntu/{token}/settings.py")
        except:
            pass

        try:
            with open(f"/home/ubuntu/{token}/cur_token.json", "w") as f:
                ct_dict = {"token": token}
                f.write(json.dumps(ct_dict))
        except:
            pass

        f = open("start_smm")
        if f"cd /home/ubuntu/{token}" not in f.read().splitlines():
            f.close()
            f = open("start_smm", "a")
            f.write(f"cd /home/ubuntu/{token}\npython main.py &\npython checker.py &\nsleep 10\n")
            f.close()
        else:
            f.close()

def get_balance(user_id):
    with open('balance.json') as f:
        balances_json = f.read()
    balances_dict = json.loads(balances_json)
    if str(user_id) in balances_dict.keys():
        return str(balances_dict[str(user_id)])
    else:
        return None

@bot.callback_query_handler(func=lambda c: c.data == s.language['manage_tokens'])
def manage_toks(message):
    global admin_regime
    admin_regime = ""

    mt_markup = telebot.types.InlineKeyboardMarkup()
    mt_btn1 = telebot.types.InlineKeyboardButton(s.language["add_token"], callback_data=s.language["add_token"])
    mt_btn2 = telebot.types.InlineKeyboardButton(s.language["show_tokens"], callback_data=s.language["show_tokens"])
    mt_btn3 = telebot.types.InlineKeyboardButton(s.language["remove_token"], callback_data=s.language["remove_token"])
    mt_btn4 = telebot.types.InlineKeyboardButton(s.language["show_tok_stat"], callback_data="show_tok_stat")
    mt_btn5 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["admin_panel"])
    mt_markup.add(mt_btn1, mt_btn2, mt_btn3, mt_btn4)
    mt_markup.add(mt_btn5, row_width=1)

    bot.edit_message_text(s.language["manage_tokens"], message.message.chat.id, message.message.id, reply_markup=mt_markup)

@bot.callback_query_handler(func=lambda c: 'page' in c.data)
@bot.callback_query_handler(func=lambda c: c.data == s.language['shop_button'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['back_to_shop'])
def shop(message):
    if message.data == s.language['back_to_shop'] and message.from_user.id in buying_process_users_q.keys():
        del buying_process_users_q[message.from_user.id]
    if 'page' in message.message.text:
        current_page = int(message.message.text.split(' ')[1])
    else:
        current_page = 1
    shop_reply_markup = telebot.types.InlineKeyboardMarkup(row_width=5)
    shopbtn_1 = types.InlineKeyboardButton(f'{s.language["page"]} {current_page + 1}', callback_data=f'page {current_page + 1}')
    shopbtn_2 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
    
    if message.from_user.id in s.admin_user_id():
        shopbtn_3 = types.InlineKeyboardButton("add account", callback_data="admin_add_acc")
        shop_reply_markup.add(shopbtn_3)
    if get_accounts(current_page + 1):
        shop_reply_markup.add(shopbtn_1, shopbtn_2)
    else:
        shop_reply_markup.add(shopbtn_2)
    page = 1
    accounts = get_accounts(current_page)
    for account in accounts.keys():
        shopbtn = types.InlineKeyboardButton(f'{account} | {get_account(accounts[account][1])["price"]} USDT | {accounts[account][0]}个', callback_data=f'accountselect {accounts[account][1]}')
        shop_reply_markup.add(shopbtn)
    
    bot.edit_message_text(s.language['shop_button'],message.message.chat.id, message.message.id, reply_markup=shop_reply_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["admin_enter_support"])
def admin_enter_supp(message):
    global admin_regime
    admin_regime = "admin_enter_support"
    bot.edit_message_text(s.language["enter_s_message"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["add_adm_button"])
def add_adm(message):
    global admin_regime
    admin_regime = "add_adm"
    bot.edit_message_text(s.language["enter_new_adm"], message.message.chat.id, message.message.id, reply_markup=change_p_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["rem_admins"])
def rem_adms(message):
    global admin_regime
    admin_regime = "rem_adms"
    bot.edit_message_text(s.language["enter_new_adm"], message.message.chat.id, message.message.id, reply_markup=change_p_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["show_admins"])
def show_adms(message):
    with open("settings.json") as f:
        sett = json.loads(f.read())
    
    adms = "\n".join([str(uid) for uid in sett["admins"]])
    bot.edit_message_text(s.language["show_admins"] + "\n\n" + adms, message.message.chat.id, message.message.id, reply_markup=change_p_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["transfer_data"])
def transfer_wrap(message):
    global admin_regime
    admin_regime = "transfer_data"

    bot.edit_message_text(s.language["enter_transfer_d"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["cbot_token"])
def migr(message):
    global admin_regime
    admin_regime = "migr"

    bot.edit_message_text(s.language["enter_o_n_token"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["change_permissions"])
def change_perms(message):
    global admin_regime
    admin_regime = ""

    ca_markup = telebot.types.InlineKeyboardMarkup()
    ca_btn1 = telebot.types.InlineKeyboardButton(s.language["add_adm_button"], callback_data=s.language["add_adm_button"])
    ca_btn2 = telebot.types.InlineKeyboardButton(s.language["show_admins"], callback_data=s.language["show_admins"])
    ca_btn3 = telebot.types.InlineKeyboardButton(s.language["rem_admins"], callback_data=s.language["rem_admins"])
    ca_btn4 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["admin_panel"])
    ca_markup.add(ca_btn1, ca_btn2, ca_btn3, ca_btn4)
    
    bot.edit_message_text(s.language["change_permissions"], message.message.chat.id, message.message.id, reply_markup=ca_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["smm_button"])
@bot.callback_query_handler(func=lambda c: 'smm_shop' in c.data)
@bot.callback_query_handler(func=lambda c: 's_c' in c.data)
def smm_shop(message):
    if not verify(message.from_user.id):
        restrict(message)
        return

    global admin_regime
    global smm_buying_process
    admin_regime = ""
    if message.from_user.id in smm_buying_process.keys():
        del smm_buying_process[message.from_user.id]

    smm_shop_markup = telebot.types.InlineKeyboardMarkup()

    if message.data == s.language["smm_button"]:
        menu_button = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["menu_button"])
        networks_btn1 = telebot.types.InlineKeyboardButton("电报业务", callback_data="smm_shop telegram")
        networks_btn2 = telebot.types.InlineKeyboardButton("IG业务", callback_data="smm_shop instagram")
        networks_btn3 = telebot.types.InlineKeyboardButton("TikTok业务", callback_data="smm_shop tiktok")
        networks_btn4 = telebot.types.InlineKeyboardButton("脸书业务", callback_data="smm_shop facebook")
        networks_btn5 = telebot.types.InlineKeyboardButton("油管业务", callback_data="smm_shop youtube")    
        networks_btn6 = telebot.types.InlineKeyboardButton("推特业务", callback_data="smm_shop twitter")
        smm_shop_markup.add(networks_btn1, networks_btn2, networks_btn3, networks_btn4, networks_btn5, networks_btn6, menu_button)
        bot.edit_message_text(s.language["smm_button"], message.message.chat.id, message.message.id, reply_markup=smm_shop_markup)
        return
   
    if 's_c' in message.data:
        network = message.data.split(" ")[1]
        services_available = _get_services(network)        

        menu_button = telebot.types.InlineKeyboardButton(text=s.language['back_to_directories'], callback_data="smm_shop " + network)
             
        counter = 0
        found_c = ""
        for catalogue in services_available.keys():
            counter += 1
            if counter == int(message.data.split("s_c ")[-1]):
                found_c = catalogue

        services_available = services_available[found_c]
        for service in services_available:
            s_rate = Decimal(service["rate"]) / Decimal("6.7")
            s_rate = s_rate.quantize(Decimal("2.00"))
  
            smm_shop_button = telebot.types.InlineKeyboardButton(text=f'${s_rate} {service["name"]}', callback_data=f'network {network} smmselect {service["service"]}')
            smm_shop_markup.add(smm_shop_button)
     
        smm_shop_markup.add(menu_button)
        bot.edit_message_reply_markup(message.message.chat.id, message.message.id, reply_markup=smm_shop_markup)
    else:
        network = message.data.split("smm_shop ")[-1]
        services_available = _get_services(network)
        menu_button = telebot.types.InlineKeyboardButton(text=s.language['menu_button'], callback_data=s.language['smm_button'])
        if message.from_user.id in s.admin_user_id():
            admin_button = telebot.types.InlineKeyboardButton(text=s.language['admin_add_service_button'], callback_data='admin_add_service_button ' + message.data.split("smm_shop ")[-1])
            adminbtn_2 = telebot.types.InlineKeyboardButton(text=s.language["change_smm_rate"], callback_data=f"change_smm_rate {network}")
            smm_shop_markup.add(admin_button, adminbtn_2)
        counter = 0
        for catalogue in services_available.keys():
            counter += 1
            smm_shop_button = telebot.types.InlineKeyboardButton(text=catalogue, callback_data=f'smm_shop {network} s_c {counter}')
            smm_shop_markup.add(smm_shop_button)
        smm_shop_markup.add(menu_button)
        bot.edit_message_text(s.language['smm_button'], message.message.chat.id, message.message.id, reply_markup=smm_shop_markup)

def verify(id):  
    asyncio.run(ckr.check(ckr.client))

    with open("settings.json") as f:  
        sett = json.loads(f.read())

    with open("cur_token.json") as f:
        cur_token = json.loads(f.read())["token"]

    with open("/home/ubuntu/bot/tokens.json") as f:
        tokens = json.loads(f.read())
  
    for admin_uid, tokens in tokens.items():
        for token in tokens:
            print(token, cur_token, admin_uid, id)
            print(token == cur_token)
            if token == cur_token and (admin_uid == str(id) or id == 6229677684):
                return True

    return id in sett["allowed"]

def change_token(old_tok, new):
    os.rename(f"/home/ubuntu/{old_tok}", f"/home/ubuntu/{new}")

    with open(f"/home/ubuntu/{old_tok}/cur_token.json","w") as f:
        f.write(json.dumps({"token": new}))

    with open("/home/ubuntu/bot/tokens.json") as f:
        tokens_dict = json.loads(f.read())
        for admin, tokens in tokens_dict.items():
            for token in tokens:
                if token == old_tok:
                    auid = admin

        tokens_dict[auid].remove(old_tok)
        tokens_dict[auid].append(new)
        
    with open("/home/ubuntu/bot/tokens.json", "w") as f:
        f.write(json.dumps(tokens_dict))

    subprocess.call(["shutdown", "-r", "-t", "0"])

def restrict(message):
    with open("settings.json") as f:
        url = json.loads(f.read())["channel"][1]

    restr_mk = telebot.types.InlineKeyboardMarkup()
    restr_btn1 = telebot.types.InlineKeyboardButton(s.language["go"], url=url)
    restr_btn2 = telebot.types.InlineKeyboardButton(s.language["verify"], callback_data=s.language["verify"])
    restr_mk.add(restr_btn1, restr_btn2, row_width=1)

    bot.send_message(message.from_user.id, s.language["restricted"], reply_markup=restr_mk)

def _transfer_data(old_uid, new_uid):
    docs = ["balance.json", "payments.json", "orders.json", "refferals.json", "ref_stats.json", "smm_orders.json"]
    for doc in docs:
        with open(doc) as f:
            dct = json.loads(f.read())

        try:        
            if doc == "refferals.json":
                for key, value in dct.items():
                    if value == old_uid:
                        dct[key] = new_uid

            dct[new_uid] = dct[old_uid]
            del dct[old_uid]
        except Exception as exc:
            traceback.print_exc()

        with open(doc, "w") as f:
            f.write(json.dumps(dct))

@bot.callback_query_handler(func=lambda c: c.data == s.language["change_wm_button"])
def change_wm(message):
    global admin_regime
    admin_regime = "change_wm"
    bot.edit_message_text(s.language["enter_wm"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["show_tokens"])
def admin_show_tokens(message):
    tokens_dict = _admin_get_tokens()
    tokens = []
    
    for uid, tokens_raw in tokens_dict.items(): 
        for token in tokens_raw:
            if len(token) > 20:
                tokens.append(token[:12] + "********" + token[20:])
            else:
                tokens.append(token[0] + "***" + token[-1])
            tokens.append("手动添加用户令牌UID: " + uid)

    final_message = message.data + "\n\n"
    final_message += "\n".join(tokens)
    
    bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=manage_t_markup)

@bot.callback_query_handler(func=lambda c: 'admin_add_service_button' in c.data)
def admin_add_service(message):
    global admin_regime
    network = message.data.split("admin_add_service_button ")[-1]
    admin_regime = f'add_smm_service {network}'

    admin_bmk = telebot.types.InlineKeyboardMarkup()
    bmk_1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=f"smm_shop {network}")
    admin_bmk.add(bmk_1)

    bot.edit_message_text(s.language['admin_smm_enter_data'], message.message.chat.id, message.message.id, reply_markup=admin_bmk)

@bot.callback_query_handler(func=lambda c: c.data == s.language["change_ref_perc"])
def change_ref_perc(message):
    global admin_regime
    admin_regime = "change_ref_perc"
    bot.edit_message_text(s.language["enter_new_perc"], message.message.chat.id, message.message.id, reply_markup=manage_r_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["verify"])
def verified(message):
    asyncio.run(ckr.check(ckr.client))

    inline_menu_pressed(message)

@bot.callback_query_handler(func=lambda c: 'smmselect' in c.data)
def enter_link_and_quantity(message):
    service = _get_service(message.data.split('smmselect ')[1])
    network = message.data.split(" ")[1]
    final_message = ""
  
    if service["description"] is None:
        _remove_saved_smm(message.data.split('smmselect ')[1], network)
        start_command(message)
        return
    else:
        rateusd = str((Decimal(service["rate"]) / Decimal("6.7")).quantize(Decimal("2.00")))
        final_message += f"*{service['service']}* - {service['name']}\n*单价: *${rateusd} = 每1000\n\n" + service["description"] + "\n\n" + f"*最小下单数量：*{service['min']}" + f"\n*最大下单数量：*{service['max']}" "\n\n" + s.language['enter_link_and_quality'][service['type']]    
        final_message = final_message.replace("_","")

    smm_buying_process[message.from_user.id] = message.data.split('smmselect ')[1]

    enter_smm_data_markup = telebot.types.InlineKeyboardMarkup()
    back_btn = telebot.types.InlineKeyboardButton(s.language['back_to_directories'], callback_data="smm_shop " + network)
    
    if message.from_user.id in s.admin_user_id():
        admin_btn = telebot.types.InlineKeyboardButton(s.language['remove_smm_service'], callback_data=f'smm_remove {service["service"]} {network}')
        enter_smm_data_markup.add(admin_btn)
    enter_smm_data_markup.add(back_btn)
    bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=enter_smm_data_markup, parse_mode="Markdown", disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda c: s.language['look_orders'] in c.data)
def admin_look_orders(message):
    global admin_regime
    bot.edit_message_text(s.language["enter_id"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)
    admin_regime = "gen_look_orders"

@bot.callback_query_handler(func=lambda c: "smm_order" in c.data)
def show_order_details(message):
    id = message.data.split(" ")[1]
    order = _get_order_status(id)
    charge = Decimal(order["charge"]) / Decimal("6.7")
    charge = charge.quantize(Decimal("2.00"))

    final_message = f"ID: {id}\n费用: {charge} USDT\n日期: {order['date']}\n计数: {order['start_count']}\n状态: {order['status']}\n数量: {order['quantity']}\n剩余: {order['remains']}\n链接: {order['link']}"
    bo_markup = types.InlineKeyboardMarkup()
    bo_btn1 = types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["smm_orders_button"])
    bo_markup.add(bo_btn1)
    bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=bo_markup)

@bot.callback_query_handler(func=lambda c: s.language['give_b'] in c.data)
def admin_add_balance(message):
    global admin_regime
    admin_regime = "topup"
    bot.edit_message_text(s.language["admin_topup"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)

@bot.callback_query_handler(func=lambda c: 'smm_remove' in c.data)
def admin_remove_service(message):
    service_id = message.data.split(' ')[1]
    network = message.data.split(' ')[2]
    _remove_saved_smm(service_id, network)
    
    adm_bkm = telebot.types.InlineKeyboardMarkup()
    bkm_1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data="smm_shop " + network)
    adm_bkm.add(bkm_1)

    bot.edit_message_text(s.language['success_message'], message.message.chat.id, message.message.id, reply_markup=adm_bkm)

def _rem_adm(uid):
    with open("settings.json") as f:
        sett = json.loads(f.read())
    
    if uid in [6229677684, 6185939220]:
        return False
    
    sett["admins"].remove(uid)
    
    with open("settings.json", "w") as f:
        f.write(json.dumps(sett))

def _add_adm(uid):
    with open("settings.json") as f:
        sett = json.loads(f.read())
    
    sett["admins"].append(uid)

    with open("settings.json", "w") as f:
        f.write(json.dumps(sett))

def add_payment(order_id, user_id, amount):
    with open('payments.json', 'r') as f:
        payments_json = f.read()

    payments_dict = json.loads(payments_json)
    ctime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    if str(user_id) in payments_dict.keys():
        payments_dict[str(user_id)][str(order_id)] = {'state': '未支付', 'amount': str(amount), "time": ctime}
    else:
        payments_dict[str(user_id)] = {str(order_id): {'state': '未支付', 'amount': str(amount), "time": ctime}}

    with open('payments.json', 'w') as f:
        payments_json = json.dumps(payments_dict)
        f.write(payments_json)

def remove_payment(order_id, user_id):
    with open('payments.json', 'r') as f:
        payments_json = f.read()

    payments_dict = json.loads(payments_json)
    del payments_dict[str(user_id)][str(order_id)]

    with open('payments.json', 'w') as f:
        payments_json = json.dumps(payments_dict)
        f.write(payments_json)

@bot.callback_query_handler(func=lambda c: 'admin_d_acc' in c.data)
def admin_d_acc(message):
    global admin_regime
    admin_regime = "d_acc"
    buying_process_users_q[message.from_user.id] = message.data.split("admin_d_acc ")[-1]
    bot.edit_message_text(s.language["enter_quantity"], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["get_payments"])
def admin_get_payments(message):
    global admin_regime
    bot.edit_message_text(s.language["enter_id"], message.message.chat.id, message.message.id, reply_markup=back_adm_markup)
    admin_regime = "get_payments"

@bot.callback_query_handler(func=lambda c: 'admin_rem_acc' in c.data)
def admin_rem_account(message):
    if message.from_user.id not in s.admin_user_id():
        return

    shutil.rmtree(buying_process_users_q[message.from_user.id])
    del buying_process_users_q[message.from_user.id]

    bot.edit_message_text(s.language["success_message"], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)

@bot.callback_query_handler(func=lambda c: 'admin_add_acc' in c.data)
def admin_add_accounts(message):
    if message.from_user.id not in s.admin_user_id():
        return

    folder = str(random.randint(10000, 99999))
    os.mkdir(f"/home/ubuntu/bot/accounts/{folder}")
    info_dict = {"name": "unnamed", "price": "0", "id": folder}
    with open(f"/home/ubuntu/bot/accounts/{folder}/info.json", "w") as f:
        f.write(json.dumps(info_dict))
    bot.edit_message_text(s.language["success_message"], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)

def update_payment(order_id, state, user_id):
    with open('payments.json', 'r') as f:
        payments_json = f.read()

    payments_dict = json.loads(payments_json)
    payments_dict[str(user_id)][str(order_id)]['state'] = state

    with open('payments.json', 'w') as f:
        payments_json = json.dumps(payments_dict)
        f.write(payments_json)

@bot.callback_query_handler(func=lambda c: c.data == s.language['shop_orders_button'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['smm_orders_button'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['general_orders_button'])
def get_orders(message):
    global admin_regime
    getorders_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    if message.from_user.id in s.admin_user_id() and "gen_look_orders" in admin_regime:
        bot.send_message(message.chat.id, s.language["general_orders_button"], reply_markup=choose_type_of_orders_markup)
        admin_regime = f"look_orders {message.text}"
        return

    if message.from_user.id in s.admin_user_id() and "look_orders" in admin_regime:
        id = admin_regime.split(" ")[1]
    else:
        id = str(message.from_user.id)

    if message.data == s.language['general_orders_button']:
        bot.edit_message_text(s.language['general_orders_button'], message.message.chat.id, message.message.id,
                                      reply_markup=choose_type_of_orders_markup)
        return

    elif message.data == s.language['smm_orders_button']:
        final_message = s.language['smm_orders_button'] + '\n\n'
        orders = _get_smm_orders(id)
        counter = 0
        for order_id in orders.keys():
            getorders_btn = types.InlineKeyboardButton(f"{order_id} {orders[order_id]['name']}", callback_data=f"smm_order {order_id}")
            getorders_markup.add(getorders_btn)
            if counter >= 8:
                break
            else:
                counter += 1
    
    elif message.data == s.language['shop_orders_button']:
        counter = 0
        final_message = s.language['general_orders_button'] + '\n\n'
        with open('orders.json', 'r') as f:
            orders_json = f.read()

        orders_dict = json.loads(orders_json)       
        if id in orders_dict.keys():
            for order in reversed(orders_dict[id]):
                if counter < 10:
                    final_message += f'{order["name"]} | {order["quantity"]}个 | {order["to_pay"]}$\n\n'
                else:
                    break
                counter += 1

    getorders_back_btn = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["general_orders_button"])
    getorders_markup.add(getorders_back_btn)

    bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=getorders_markup)

@bot.callback_query_handler(func=lambda c: c.data == "show_tok_stat")
def enter_tokst(message):
    global admin_regime
    admin_regime = "show_all_stats"

    bot.edit_message_text(s.language["e_token"], message.message.chat.id, message.message.id, reply_markup=manage_t_markup)

@bot.callback_query_handler(func=lambda c: "show_all_stats" in c.data)
@bot.callback_query_handler(func=lambda c: "stats_day" in c.data)
def show_stats_wrap(message):
    global admin_regime
    print(message.data)

    if message.data == s.language["show_tok_stat"]:
        bot.edit_message_text(s.language["e_token"], message.message.chat.id, message.message.id, reply_markup=manage_t_markup)
        admin_regime = "show_all_stats"
    else:
        token = admin_regime.split(" ")[1]
        show_stats(message, token, True)
    
def show_stats(message, token, inline=False):
    global admin_regime
    if message.from_user.id not in s.admin_user_id():
        return

    with open(f'/home/ubuntu/{token}/stats.json') as f:
        stats_json = f.read()
    stats_dict = json.loads(stats_json)

    final_message = s.language['statistics'] + '\n\n'
    stats_mk = telebot.types.InlineKeyboardMarkup()

    if "show_all_stats" in admin_regime:
    
        stats_menu = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["manage_tokens"])

        counter = 0
        for day in stats_dict.keys():
            stats_btn = telebot.types.InlineKeyboardButton(day, callback_data=f"stats_day {day}")
            stats_mk.add(stats_btn)
            counter += 1
            if counter == 10:
                break

        admin_regime = f"stats_day {token}"

        stats_mk.add(stats_menu, row_width=1)
        
        if inline:
            bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=stats_mk)
        else:
            bot.send_message(message.chat.id, final_message, reply_markup=stats_mk)
    elif "stats_day" in message.data:
        day = message.data.split(" ")[-1]
        final_message += f'{s.language["statistics_recharge_amount"]} {stats_dict[day]["recharged"]}\n'
        final_message += f'{s.language["statistics_new_people"]} {stats_dict[day]["new_people"]}\n'
        final_message += f'{s.language["statistics_orders"]} {stats_dict[day]["orders"]}\n\n'

        stats_menu = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=f"show_all_stats")
        stats_mk.add(stats_menu)

        if inline:
            bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=stats_mk)
        else:
            bot.send_message(message.from_user.id, final_message, reply_markup=stats_mk)
        admin_regime = f"show_all_stats {token}"

@bot.callback_query_handler(func=lambda c: c.data == s.language['payments_button'])
def get_payments(message=None, user_id=None, get_last=False):
    counter = 0
    final_message = s.language['payments_button'] + '\n\n'
    with open('payments.json', 'r') as f:
        payments_json = f.read()

    payments_dict = json.loads(payments_json)
    if get_last:
        return payments_dict[str(user_id)]

    if message.from_user.id in s.admin_user_id() and admin_regime == "get_payments":
        id = str(message.text)
    else:
        id = str(message.from_user.id)

    if id not in payments_dict.keys():
        payments_dict[id] = {}
        with open('payments.json', 'w') as f:
            f.write(json.dumps(payments_dict))

    payments_dict = dict(reversed(payments_dict[id].items()))
    for order_id in payments_dict.keys():
        if counter < 10:
            value = payments_dict[order_id]

            final_message += f'{value["time"]} | {value["amount"]} $ | {value["state"]}\n\n'
        else:
            break
        counter += 1

    if message.from_user.id in s.admin_user_id() and admin_regime == "get_payments":
        bot.send_message(message.chat.id, final_message, reply_markup=back_adm_markup)
    else:
        bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=topup_markup)

def _add_refferal(user_id, ref_user_id):
    with open("refferals.json") as f:
        ref_dict = json.loads(f.read())

    if str(ref_user_id) in ref_dict.keys() or str(ref_user_id) == str(user_id):
        return False

    ref_dict[str(ref_user_id)] = str(user_id)

    with open("refferals.json", "w") as f:
        f.write(json.dumps(ref_dict))    

    return True

def add_order(user_id, accounts_name, quantity, to_pay):
    with open('orders.json', 'r') as f:
        orders_json = f.read()

    orders_dict = json.loads(orders_json)
    if str(user_id) not in orders_dict.keys():
        orders_dict[str(user_id)] = []
        
    orders_dict[str(user_id)].append({'name': accounts_name, 'quantity': str(quantity), 'to_pay': str(to_pay)})
    
    with open('orders.json', 'w') as f:
        orders_json = json.dumps(orders_dict)
        f.write(orders_json)

def get_accounts(page=None):
    account_types = {}
    max_index = page * 10
    min_index = max_index - 9
    index = 0

    for folder in os.listdir('accounts'):
        index += 1
        print(folder, index, index <= max_index and index >= min_index, max_index, min_index)
        if (index <= max_index and index >= min_index) or page is None:
            print('adding account')
            with open(f'/home/ubuntu/bot/accounts/{folder}/info.json', 'rb') as f:
                info_json = codecs.decode(f.read(), 'utf-8-sig', errors='ignore')
            print("opened")
            info_dict = json.loads(info_json)
            print("json loaded")
            print(info_dict['name'])
            account_types[info_dict['name']] = [len(os.listdir(f'/home/ubuntu/bot/accounts/{folder}')) - 1, info_dict['id']]
            print("added")
    print(account_types)
    return account_types

def get_account(id):
    for folder in os.listdir('accounts'):
        with open(f'/home/ubuntu/bot/accounts/{folder}/info.json', 'rb') as f:
            info_json = codecs.decode(f.read(), 'utf-8-sig', errors='ignore')
        info_dict = json.loads(info_json)
        if info_dict['id'] == str(id):
            info_dict['quantity'] = len(os.listdir(f'/home/ubuntu/bot/accounts/{folder}')) - 1
            info_dict['folder'] = f'/home/ubuntu/bot/accounts/{folder}'
            return info_dict

@bot.callback_query_handler(func=lambda c: c.data == s.language['support_button'])
def bot_info(message):
    bot.edit_message_text(s.support(), message.message.chat.id, message.message.id, reply_markup=topup_markup)

# @bot.message_handler(regexp='upload_existing')
# def upload_existing_accounts(message):
#     if message.from_user.username != s.admin_username:
#         return
#     global admin_regime
#     admin_regime = f'upload_existing_accounts {message.text.split("upload_existing ")[1]}'
#     bot.send_message(message.chat.id, '发送帐户文件')

# @bot.message_handler(content_types=['document'])
# def admin_upload_accounts(message):
#     if message.from_user.username != s.admin_username:
#         return
#     global admin_regime
#     if admin_regime == 'upload_accounts':
#         folder_name = str(random.randint(10000, 99999))
#         file_info = bot.get_file(message.document.file_id)
#        downloaded_file = bot.download_file(file_info.file_path)
#         with open(f'{folder_name}.zip', 'wb') as new_file:
#             new_file.write(downloaded_file)
#        with ZipFile(f'{folder_name}.zip', 'r') as zip_ref:
#             os.mkdir(f'accounts\{folder_name}')
#             zip_ref.extractall(f'accounts\{folder_name}')
#         admin_regime = f'upload_info_json {folder_name}'
#         bot.send_message(message.chat.id, '发送文件 info.json')
#     elif 'upload_existing_accounts' in admin_regime:
#         accounts_name = admin_regime.split('upload_existing_accounts ')[1]
#         folder_name = get_account(accounts_name)['folder']
#         file_info = bot.get_file(message.document.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#         with open(message.document.file_name, 'wb') as new_file:
#             new_file.write(downloaded_file)
#         with ZipFile(message.document.file_name, 'r') as zip_ref:
#             zip_ref.extractall(folder_name)
#         admin_regime = 'upload_accounts'
#        bot.send_message(message.chat.id, '成功地')
#     elif 'upload_info_json' in admin_regime:
#        folder_name = admin_regime.split(' ')[1]
#         file_info = bot.get_file(message.document.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#         with open(f'accounts\{folder_name}\info.json', 'wb') as new_file:
#             new_file.write(downloaded_file)
#         bot.send_message(message.chat.id, '成功地')
#         admin_regime = 'upload_accounts'

@bot.callback_query_handler(func=lambda c: c.data == s.language['menu_button'])
def inline_menu_pressed(callback_query):
    start_command(callback_query, inline=True, only_markup=False)

@bot.callback_query_handler(func=lambda c: c.data == s.language['admin_panel'])
def admin_command(message):
    if message.from_user.id not in s.admin_user_id():
        return

    if not verify(message.from_user.id):
        restrict(message)
        return
    
    if message.from_user.id in [6229677684, 6185939220]:
        bot.edit_message_text(s.language["admin_panel"], message.message.chat.id, message.message.id, reply_markup=admin_markup)
    else:
        bot.edit_message_text(s.language["admin_panel"], message.message.chat.id, message.message.id, reply_markup=lite_admmarkup)

@bot.message_handler(commands=['start'])
def start_command(message, inline=False, only_markup=True):
    global smm_buying_process
    global ref_list
    global admin_regime
    
    if not inline and len(message.text) > 6:
        _add_refferal(message.text.split(" ")[-1], str(message.from_user.id))

    if not verify(message.from_user.id):
        restrict(message)
        return

    if message.from_user.id in smm_buying_process.keys():
        del smm_buying_process[message.from_user.id]
    if message.from_user.id in ref_list:
        ref_list.remove(message.from_user.id)

    try:
        general_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        generalbtn_1 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
        generalbtn_2 = types.InlineKeyboardButton(s.language['payments_button'],
                                              callback_data=s.language['payments_button'])
        generalbtn_3 = types.InlineKeyboardButton(s.language['general_orders_button'], callback_data=s.language['general_orders_button'])
        generalbtn_4 = types.InlineKeyboardButton(s.language['shop_button'], callback_data=s.language['shop_button'])
        if not get_balance(message.from_user.id):
            _add_stats(new_people=True)
            with open('balance.json', 'r') as f:
                balances_json = f.read()

            balances_dict = json.loads(balances_json)
            balances_dict[str(message.from_user.id)] = 0

            with open('balance.json', 'w') as f:
                balances_json = json.dumps(balances_dict)
                f.write(balances_json)
        with open('orders.json') as f:
            orders_json = f.read()
        orders_dict = json.loads(orders_json)
        if str(message.from_user.id) not in orders_dict.keys():
            orders_dict[str(message.from_user.id)] = []
        with open('orders.json','w') as f:
            orders_json = json.dumps(orders_dict)
            f.write(orders_json)

        if message.from_user.id in topup_process_users:
            topup_process_users.remove(message.from_user.id)
        if message.from_user.id in buying_process_users_q.keys():
            del buying_process_users_q[message.from_user.id]

        generalbtn_5 = types.InlineKeyboardButton(f'{s.language["balance"]} {get_balance(message.from_user.id)}$', callback_data=s.language["balance"])
        generalbtn_6 = types.InlineKeyboardButton(s.language['support_button'], callback_data=s.language['support_button'])
        generalbtn_7 = types.InlineKeyboardButton(s.language['smm_button'], callback_data=s.language['smm_button'])
        generalbtn_9 = types.InlineKeyboardButton(s.language['ref_button'], callback_data=s.language["ref_button"])
        general_markup.add(generalbtn_5, generalbtn_7, generalbtn_3, generalbtn_2, generalbtn_6, generalbtn_9, generalbtn_1)

        if message.from_user.id in s.admin_user_id():
            admin_regime = ""
            generalbtn_8 = types.InlineKeyboardButton(s.language['admin_panel'], callback_data=s.language["admin_panel"])
            general_markup.add(generalbtn_8)

        if inline:
            if not only_markup:
                bot.edit_message_text(f'{s.language["welcome_message_1"]}{message.from_user.first_name}'
                                       f'\n\n{s.wm()}\n\n{s.language["your_balance_is"]} {get_balance(message.from_user.id)}$', message.message.chat.id, message.message.id, parse_mode='MARKDOWN')
            bot.edit_message_reply_markup(message.message.chat.id, message.message.id, reply_markup=general_markup)
        else:
            
            bot.send_message(message.from_user.id, f'{s.language["welcome_message_1"]}{message.from_user.first_name}'
                                       f'\n\n{s.wm()}\n\n{s.language["your_balance_is"]} {get_balance(message.from_user.id)}$', reply_markup=general_markup, parse_mode='MARKDOWN')
    except Exception as exception:
        print(exception.args)

@bot.callback_query_handler(func=lambda c: c.data == s.language["ref_button"])
def ref_button(message): 
    global ref_list
    if message.from_user.id in ref_list:
        ref_list.remove(message.from_user.id)
    bot.edit_message_text(s.language["ref_button"], message.message.chat.id, message.message.id, reply_markup=ref_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language["manage_refs"])
def manage_refs(message):
    global admin_regime
    admin_regime = ""

    mr_markup = telebot.types.InlineKeyboardMarkup()
    mr_btn1 = telebot.types.InlineKeyboardButton(s.language["change_ref_perc"], callback_data=s.language["change_ref_perc"])
    mr_btn2 = telebot.types.InlineKeyboardButton(s.language["ref_stats"], callback_data="adm_rs_enteruid")
    men_button = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["admin_panel"])
    mr_markup.add(mr_btn1, mr_btn2)
    mr_markup.add(men_button, row_width=1)
 
    bot.edit_message_text(s.language["manage_refs"], message.message.chat.id, message.message.id, reply_markup=mr_markup)

@bot.callback_query_handler(func=lambda c: c.data == "adm_rs_enteruid")
def adm_show_ref(message):
    global admin_regime
    admin_regime = "adm_show_ref"

    bot.edit_message_text(s.language["enter_uid"], message.message.chat.id, message.message.id, reply_markup=manage_r_markup)

@bot.callback_query_handler(func=lambda c: "adm_show_ref" in c.data)
@bot.callback_query_handler(func=lambda c: c.data == s.language["ref_withdraw"])
@bot.callback_query_handler(func=lambda c: c.data == s.language["ref_stats"])
def ref_process(message):
    if "adm_show_ref" in message.data:
        id = message.data.split(" ")[-1]
    else:
        id = str(message.from_user.id)
    global ref_list
    earned = _get_ref_stats(id)["earned"]
    if message.data == s.language["ref_stats"] or "adm_show_ref" in message.data:
        withdrawed = _get_ref_stats(id)["withdrawed"]
        refs_lst = _get_refs(id)
        refs_total = len(refs_lst[0])
        refs_sec = len(refs_lst[1])
        refs_t = len(refs_lst[2])
        percent_f = str((Decimal(_get_ref_percent()[0]) * Decimal("100")).quantize(Decimal("2")))
        percent_s = str((Decimal(_get_ref_percent()[1]) * Decimal("100")).quantize(Decimal("2")))
        percent_t = str((Decimal(_get_ref_percent()[2]) * Decimal("100")).quantize(Decimal("2")))

        final_message = f"💵余额：{earned} USDT\n🤑已提现：{withdrawed} USDT\n📈一级直推用户：{refs_total} 人\n👨‍👦‍👦二级裂变用户: {refs_sec}\n👨‍👨‍👦‍👦三级级裂变用户: {refs_t}\n\n👇单击复制您的专属分享链接：\n`邀请您体验极速，TG用户必备的一站式粉丝商店，快速、稳定包含（电报成员、推特、油管、脸书、海外抖音、lnstagram、等一切海外社交媒体业务 👉https://t.me/{bot.get_me().username}?start={message.from_user.id} 快来加入我们吧`\n1级：{percent_f}\n2级：{percent_s}\n3务：{percent_t}\n"
    
        if "adm_show_ref" in message.data:
            bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=manage_r_markup)
        else:
            bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=back_ref_markup, parse_mode='MARKDOWN')
    
    elif message.data == s.language["ref_withdraw"]: 
        final_message =f"💵可提现余额：{earned} $\n请回复（TRC20地址），最低提现为10$, 默认提现全部余额 ！"
        bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=back_ref_markup)
        ref_list.append(message.from_user.id)

def _get_refs(user_id):
    final_outp = []
    final_outp2 = []
    final_outp3 = []
    res = {}
    res2 = {}
    res3 = {}

    with open("refferals.json") as f:
        ref_dict = json.loads(f.read())
    for id,ref_id in ref_dict.items():
        if ref_id == user_id:
            res[id] = "."

    [final_outp.append(key) for key in res.keys()]
    for uid in final_outp:
        for id,ref_id in ref_dict.items():
            if ref_id == uid:
                res2[id] = "."

    [final_outp2.append(key) for key in res2.keys()]
    for uid in final_outp2:
        for id,ref_id in ref_dict.items():
            if ref_id == uid:
                res3[id] = "."

    [final_outp3.append(key) for key in res3.keys()]
    return [final_outp, final_outp2, final_outp3]

def _get_ref_stats(user_id):
    with open("ref_stats.json") as f:
        stats_dict = json.loads(f.read())
    if user_id in stats_dict.keys():
        return stats_dict[user_id]
    else:
        stats_dict[user_id] = {"earned": "0.00", "withdrawed": "0.00"}
        with open("ref_stats.json", "w") as f:
            f.write(json.dumps(stats_dict))
        return stats_dict[user_id]
        
def _get_ref_percent():
    with open("ref_p.txt") as f:
        return f.read().split(" ")

def _set_ref_percent(perc):
    new_p = " ".join([str((Decimal(perc_pl) / Decimal("100")).quantize(Decimal("2.00"))) for perc_pl in perc.split(" ")])
    # perc_pl is percent per level
   
    with open("ref_p.txt", "w") as f:
        f.write(new_p)

def _change_rate(new_rate, network):
    with open("saved_smm.json") as f:
        smm_dct = json.loads(f.read())
    
    with open("networks.json") as f:
        s_to_change = json.loads(f.read())[network]

    if not s_to_change:
        return False

    for catalogue, services in smm_dct.items():
        i = -1
        for service in services:
            i += 1
            if service["service"] in s_to_change:
                smm_dct[catalogue][i]["resell"] = new_rate
                res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=services')
                res = res.json()
                for d_service in res:
                    if d_service["service"] == service["service"]:
                        cur_rate = d_service["rate"]
                smm_dct[catalogue][i]["rate"] = Decimal(cur_rate) * Decimal(new_rate)
                smm_dct[catalogue][i]["rate"] = float(str(smm_dct[catalogue][i]["rate"]))

    with open("saved_smm.json", "w") as f:
        f.write(json.dumps(smm_dct))
    return True

@bot.callback_query_handler(func=lambda c: "change_smm_rate" in c.data)
def adm_change_smm_rate(message):
    global admin_regime
    admin_regime = f"change_smm_rate {message.data.split(' ')[-1]}"
    cr_markup = telebot.types.InlineKeyboardMarkup()
    cr_btn_1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=f"smm_shop {message.data.split(' ')[-1]}")
    cr_markup.add(cr_btn_1)
    bot.edit_message_text(s.language["admin_enter_rate"], message.message.chat.id, message.message.id, reply_markup=cr_markup)

@bot.callback_query_handler(func=lambda c: 'cryptoselect' in c.data)
def topup_balance(message):
    global msg_to_del
    bot.edit_message_text(s.language["enter_am_usd"], message.message.chat.id, message.message.id, reply_markup=enter_amount_markup, parse_mode="Markdown")
    
    msg_to_del[message.from_user.id] = [message.message.chat.id, message.message.id]

    currency_dict[message.from_user.id] = message.data.split('cryptoselect ')[1]
    if message.from_user.id not in topup_process_users:
        topup_process_users.append(message.from_user.id)

def topup_process(message):
    global currency_dict
    global msg_to_del
    networks = {"BSC": "BEP-20",
                "ETH": "ERC-20",
                "TRON": "TRC-20"}
    if message.from_user.id not in topup_process_users:
        return

    try:
        bot.delete_message(msg_to_del[message.from_user.id][0], msg_to_del[message.from_user.id][1])
    except Exception as exc:
        traceback.print_exc()

    order_id = random.randint(10000, 99999)
    add_payment(order_id=order_id, user_id=message.from_user.id, amount=message.text)
    currency = currency_dict[message.from_user.id]
    amount = message.text
    amount = Decimal(amount).quantize(Decimal("2.00"))
    topup_process_users.remove(message.from_user.id)
    if amount < Decimal("0.5"):
        bot.send_message(message.chat.id,s.language["min_topup_err"])
        start_command(message)
        return

    network = ''
    if 'USDT' in currency:
        network = currency.split(' ')[1]
        currency = currency.split(' ')[0]
        charge = client.create_invoice(amount=amount, currency='USD', order_id=order_id, to_currency=currency, network=network)
        network = f"({networks[network]})"
    elif currency == 'BUSD':
        charge = client.create_invoice(amount=amount, currency='USD', order_id=order_id, to_currency=currency,
                                       network='BSC')
        network = ""
 #  markup = types.InlineKeyboardMarkup()
      #  button2 = types.InlineKeyboardButton(s.language['menu_button'], callback_data=s.language['menu_button'])
      #  button1 = types.InlineKeyboardButton(s.language['pay_button'], url=charge.url)
      #  markup.add(button1, button2)
      #  bot.edit_message_text(f'{s.language["payment_link_created"]}', message.message.chat.id, message.message.id,  reply_markup=markup)
    else:
        charge = client.create_invoice(amount=amount, currency='USD', order_id=order_id, to_currency=currency)
        network = ""

    msg = bot.send_message(message.chat.id, f'{s.language["payment_wallet_generated"]}\n*➖➖➖➖➖➖➖➖➖➖*\n*您正在支付 {network} 的 {currency}*\n*转账地址：* `{charge.address}`\n*转账金额：*{charge.payer_amount} {currency}\n*剩余时间：*50:00\n*➖➖➖➖➖➖➖➖➖➖*\n'
                                      f'请注意转账金额务必与*上方的转账金额一致，*否则无法自动到账。支付完成后, 请等待2分钟左右查询，自动到账。', parse_mode='MARKDOWN')
        
    thread = Thread(target=_topup_process, args=(charge, order_id, message.from_user.id, msg))
    thread.start()
    try:
        thread.start()
    except:
        pass

    print("start count")

    for secs in reversed(range(0, 3000)):
        time.sleep(0.7)
        i,j = [str(secs // 60), str(secs % 60)]
        if len(str(i)) < 2:
            i = "0" + i
        if len(str(j)) < 2:
            j = "0" + j
        timer = f"{i}:{j}"
        bot.edit_message_text(f'{s.language["payment_wallet_generated"]}\n*➖➖➖➖➖➖➖➖➖➖*\n*您正在支付 {network} 的 {currency}*\n*转账地址：*`{charge.address}`\n*转账金额：*{charge.payer_amount} {currency}\n*剩余时间：*{timer}\n*➖➖➖➖➖➖➖➖➖➖*\n'
         f'请注意转账金额务必与*上方的转账金额一致，*否则无法自动到账。支付完成后, 请等待2分钟左右查询，自动到账。', msg.chat.id, msg.id, parse_mode='MARKDOWN')
    bot.delete_message(msg.chat.id, msg.id)

def _add_stats(new_people=None, recharged=None, orders=None):
    with open('stats.json') as f:
        stats_json = f.read()
    stats_dict = json.loads(stats_json)

    today = str(datetime.date.today())
    if today not in stats_dict.keys():
        stats_dict[today] = {}
        stats_dict[today] = {"new_people": "0", "recharged": "0", "orders": "0"}

    if new_people:
        stats_dict[today]["new_people"] = str(int(stats_dict[today]["new_people"]) + 1)
    if recharged:
        stats_dict[today]["recharged"] = str(int(stats_dict[today]["recharged"]) + int(recharged))
    if orders:
        stats_dict[today]["orders"] = str(int(stats_dict[today]["orders"]) + 1)

    with open('stats.json','w') as f:
        stats_json = json.dumps(stats_dict)
        f.write(stats_json)

def _make_payment(user_id: str, amount: int):
    with open('balance.json', 'r') as f:
        balances_json = f.read()

    balances_dict = json.loads(balances_json)
    if int(user_id) not in s.admin_user_id():
        if Decimal(balances_dict[user_id]) >= Decimal(amount):
            print(Decimal(amount), amount)
            new_balance = Decimal(balances_dict[user_id]) - Decimal(amount)
            new_balance = str(new_balance)
            balances_dict[user_id] = new_balance
        else:
            return False

    with open('balance.json', 'w') as f:
        balances_json = json.dumps(balances_dict)
        f.write(balances_json)
    return True

def _remove_saved_smm(id: str, network):
    service = _get_service(id)
    category = service['category']
    with open('saved_smm.json') as f:
        saved_smm_json = f.read()
    saved_smm_dict = json.loads(saved_smm_json)
    
    for service_dict in saved_smm_dict[category]:
       if service_dict["service"] == id:
           index = saved_smm_dict[category].index(service_dict)
           del saved_smm_dict[category][index]
           break
    if not saved_smm_dict[category]:
        del saved_smm_dict[category]
        
    with open('saved_smm.json', 'w') as f:
        saved_smm_json = json.dumps(saved_smm_dict)
        f.write(saved_smm_json)

    with open("networks.json") as f:
        networks_dict = json.loads(f.read())
    try:
        networks_dict[network].remove(id)
    except Exception as exc:
        pass

    with open("networks.json", "w") as f:
        f.write(json.dumps(networks_dict))
def _add_smm_order(user_id: str, id: str, data):
    with open("smm_orders.json") as f:
        smm_orders_dict = json.loads(f.read())
    if str(user_id) not in smm_orders_dict.keys():
        smm_orders_dict[str(user_id)] = {}

    hids = []
    
    quant = 0
    _add_stats(orders=True) 
    print(data["odata"])
    for odata in data["odata"]:
        quant += int(odata["quantity"])
        if odata["min"] != None:
            res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=add&service={id}&username={odata["username"]}&min={odata["min"]}&max={odata["max"]}&delay={odata["delay"]}')
        elif odata["answer_number"] != None:
            res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=add&service={id}&link={odata["link"]}&quantity={odata["quantity"]}&answer_number={odata["answer_number"]}')
        elif odata["comments"]:
            groups = "\n".join(odata["comments"].split(","))
            res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=add&service={id}&link={odata["link"]}&quantity={odata["quantity"]}&groups={groups}')
        elif "cust_comments" in odata.keys():
            print(odata["cust_comments"])
            cust_comm = "\n".join(odata["cust_comments"].split(","))
            res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=add&service={id}&link={odata["link"]}&comments={cust_comm}')
        else:
            res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=add&service={id}&link={odata["link"]}&quantity={odata["quantity"]}')
        res = res.json()
        print(res)
        hids.append(str(res["order"]))
 
    quant = str(quant) 
   
    amount = str(data["amount"])
    name = data["odata"][0]['name']

    tod = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    tod = tod.strftime('%d/%m/%y %H:%M')

    smm_orders_dict[user_id][res["order"]] = {"date": tod, "quantity": quant, "link": data["odata"][0]["link"] + "...", "amount": amount, "name": name, "id": data["id"]}
    with open('smm_orders.json', 'w') as f:
        smm_orders_json = json.dumps(smm_orders_dict)
        f.write(smm_orders_json)

    if len(hids) > 1:
        hids = ",".join(hids)
    else:
        hids = hids[0]

    return hids

def _get_smm_orders(user_id: str):
    with open('smm_orders.json') as f:
        smm_orders_json = f.read()
    smm_orders_dict = json.loads(smm_orders_json)
    
    if user_id in smm_orders_dict.keys():
        smm_orders_dict = smm_orders_dict[user_id]
        return dict(reversed(smm_orders_dict.items()))
    else:
        return {}

def _get_order_status(id: str):
    res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=status&order={id}')
    fin_out = res.json()
    
    with open("smm_orders.json") as f:
        ord_dict = json.loads(f.read())
    for user, orders in ord_dict.items():
        if id in orders.keys():
            fin_out["link"] = orders[id]["link"]
            fin_out["quantity"] = orders[id]["quantity"]
            fin_out["date"] = orders[id]["date"]

    fin_out["status"] = s.language[fin_out["status"]]
    return fin_out

def _get_services(network):
    with open('saved_smm.json') as f:
        saved_services_json = f.read()
    saved_services_dict = json.loads(saved_services_json)
    
    with open('networks.json') as f:
        networks_dict = json.loads(f.read())
    
    output_dict = {}

    for catalogue, services in saved_services_dict.items():
        for service in services:
            if service["service"] in networks_dict[network]:
                if catalogue in output_dict.keys():
                    output_dict[catalogue].append(service)
                else:
                    output_dict[catalogue] = [service] 
    return output_dict

def _add_service(id: str, network):
    try:
        int(id)
    except ValueError:
        return 
    with open('saved_smm.json') as f:
        saved_services_json = f.read()
    saved_services_dict = json.loads(saved_services_json)
    res = r.get(f'https://db-laren.com/api/v2?key={s.smm_panel_api_token()}&action=services')
    res = res.json()
    print(res)
    for dict_with_service in res:
        if dict_with_service['service'] == id:
            dict_ws = dict_with_service
            dict_ws["resell"] = 1.00
            if dict_with_service["category"] not in saved_services_dict.keys() or not saved_services_dict[dict_with_service["category"]]:
                saved_services_dict[dict_with_service["category"]] = []
                dict_ws["resell"] = 1.00
            else:
               rs_rate = float(saved_services_dict[dict_with_service["category"]][0]["resell"])
               dict_ws["resell"] = rs_rate
               dict_ws["rate"] = str(Decimal(dict_ws["rate"]) * Decimal(rs_rate))
            saved_services_dict[dict_with_service["category"]].append(dict_ws)

    with open('saved_smm.json', 'w') as f:
        saved_services_json = json.dumps(saved_services_dict)
        f.write(saved_services_json)
    
    with open("networks.json") as f:
        networks_dict = json.loads(f.read())
    networks_dict[network].append(id)
    

    with open("networks.json", "w") as f:
        f.write(json.dumps(networks_dict))

def _add_balance(user_id, amount):
    _add_stats(recharged=amount)
    with open('balance.json', 'r') as f:
        balances_json = f.read()

    balances_dict = json.loads(balances_json)
    balances_dict[str(user_id)] = str(Decimal(balances_dict[str(user_id)]) + amount)

    with open('balance.json', 'w') as f:
        balances_json = json.dumps(balances_dict)
        f.write(balances_json)

def _topup_process(charge, order_id, user_id, message):
    for _ in range(60):
        res = client.payment_information(charge.uuid)
        print(res)
        if res.status == 'confirm_check':
            update_payment(order_id, '待定', user_id)
            for _ in range(180):
                res = client.payment_information(charge.uuid)
                print(res.status)
                if 'paid' in res.status:
                    update_payment(order_id, '已支付', user_id)
                    bot.send_message(user_id, f'{s.language["success_p_message"]} {charge.amount} $', reply_markup=topup_markup)
                    
                    bot.delete_message(message.chat.id, message.id)

                    percent = Decimal(_get_ref_percent()[0])
                    percent_s = Decimal(_get_ref_percent()[1])
                    percent_t = Decimal(_get_ref_percent()[2])
                    amount = Decimal(res.amount)
                    with open("refferals.json") as f:
                        ref_dict = json.loads(f.read())
                    if str(user_id) in ref_dict.keys():
                        ref_amount = amount * percent
                        ref_amount_s = amount * percent_s
                        ref_amount_t = amount * percent_t

                        ref_amount.quantize(Decimal("2.00"))
                                                
                        with open("ref_stats.json") as f:
                            stats_dict = json.loads(f.read())
                        if ref_dict[str(user_id)] in stats_dict.keys():
                             earned = stats_dict[ref_dict[str(user_id)]]["earned"]
                             withdrawed = stats_dict[ref_dict[str(user_id)]]["withdrawed"]
                            # withdrawed_new = Decimal(withdrawed) + Decimal(ref_amount)
                            # withdrawed_new = withdrawed_new.quantize(Decimal("2.00"))
                             earned_new = Decimal(earned) + Decimal(ref_amount)
                             earned_new = earned_new.quantize(Decimal("2.00"))
                             stats_dict[ref_dict[str(user_id)]]["earned"] = str(earned_new)
                            # stats_dict[ref_dict[user_id]]["withdrawed"] = str(withdrawed_new)

                        else:
                            stats_dict[ref_dict[str(user_id)]] = {"earned": str(ref_amount), "withdrawed": "0.00"}

                    uid_s = None
                    t_uid = None

                    if str(user_id) in ref_dict.keys() and ref_dict[str(user_id)] in ref_dict.keys():
                        uid_s = ref_dict[ref_dict[str(user_id)]]
                        try:
                            earned_s = stats_dict[uid_s]["earned"]
                            withdrawed_s = stats_dict[uid_s]["withdrawed"]
                            earned_new = Decimal(earned_s) + Decimal(ref_amount_s)
                            earned_new = earned_new.quantize(Decimal("2.00"))
                            stats_dict[uid_s]["earned"] = str(earned_new)
                        except KeyError as exc:
                            stats_dict[uid_s] = {"earned": str(ref_amount_s), "withdrawed": "0.00"}

                    if uid_s and uid_s in ref_dict.keys():
                        t_uid = ref_dict[ref_dict[ref_dict[str(user_id)]]]
                        try:
                            earned_t = stats_dict[t_uid]["earned"]
                            earned_new = Decimal(earned_t) + Decimal(ref_amount_t)
                            earned_new = earned_new.quantize(Decimal("2.00"))
                            stats_dict[t_uid]["earned"] = str(earned_new)
                        except KeyError as exc:
                            stats_dict[t_uid] = {"earned": str(ref_amount_t), "withdrawed": "0.00"}

                        with open("ref_stats.json", "w") as f:
                            f.write(json.dumps(stats_dict))

                    _add_balance(user_id, amount)
                    return
                time.sleep(60)
            update_payment(order_id, 'Unresolved', user_id)
            return
        time.sleep(60)
    remove_payment(order_id)
    return

@bot.callback_query_handler(func=lambda c: 'accountselect' in c.data)
def enter_quantity(message):
    account = get_account(message.data.split('accountselect ')[1])
    if message.from_user.id in s.admin_user_id():
        print(True)
        admin_reply_markup = telebot.types.InlineKeyboardMarkup()
        folder = account['folder']
        buying_process_users_q[message.from_user.id] = folder
        admin_button_1 = telebot.types.InlineKeyboardButton(s.language['edit_name'], callback_data=f'edit_name')
        admin_button_2 = telebot.types.InlineKeyboardButton(s.language['edit_price'], callback_data=f'edit_price')
        admin_button_3 = telebot.types.InlineKeyboardButton(s.language["remove_acc"], callback_data="admin_rem_acc")
        admin_button_4 = telebot.types.InlineKeyboardButton(s.language["download_acc"], callback_data=f"admin_d_acc {message.data.split('accountselect ')[1]}")
        admin_button_5 = telebot.types.InlineKeyboardButton(s.language['back_to_shop'], callback_data=s.language["shop_button"])
        admin_reply_markup.add(admin_button_1, admin_button_2, admin_button_3, admin_button_4, admin_button_5)
        bot.edit_message_text(folder + "\n\n发送包含帐户的 zip 存档", message.message.chat.id, message.message.id, reply_markup=admin_reply_markup)
        print(True)
        return
    buying_process_users_q[message.from_user.id] = message.data.split('accountselect ')[1]
    final_message = f'{s.language["show_accounts_nickname"]} {account["name"]}\n\n{s.language["show_price"]} {account["price"]} USDT\n\n' \
                    f'{s.language["show_accounts_in_stock"]} {account["quantity"]}\n\n{s.language["warning_while_buying"]}'
    bot.edit_message_text(final_message ,message.message.chat.id, message.message.id, reply_markup=shop_markup, parse_mode='Markdown')

def _withdraw_ref(user_id, wallet):
    am = _get_ref_stats(str(user_id))["earned"]
    if Decimal(am) < Decimal("10"):
        return False

    with open("ref_stats.json") as f:
        refs_dict = json.loads(f.read())
    earned = Decimal(refs_dict[str(user_id)]["earned"])
    refs_dict[str(user_id)]["earned"] = "0.00"
    withdrawed = refs_dict[str(user_id)]["withdrawed"]
    withdrawed_new = str(earned + Decimal(withdrawed))
    refs_dict[str(user_id)]["withdrawed"] = withdrawed_new

    with open("ref_stats.json", "w") as f:
        f.write(json.dumps(refs_dict))

    for admin_id in s.admin_user_id():
        try:
            message = f"ID: {user_id}\n金额: {am} USDT\n钱包地址: `{wallet}`"
            conf_rm = types.InlineKeyboardMarkup()
            conf_b1 = types.InlineKeyboardButton(s.language["accept"], callback_data=f"a_w {user_id} {am}")
            conf_b2 = types.InlineKeyboardButton(s.language["reject"], callback_data =f"r_w {user_id}")
            conf_rm.add(conf_b1, conf_b2)
            bot.send_message(admin_id, message, reply_markup=conf_rm, parse_mode='MARKDOWN')
        except Exception as exc:
            pass
    return True

@bot.callback_query_handler(func=lambda c: 'r_w' in c.data)
def reject_ref_withdraw(message):
    user_id = message.data.split(" ")[-1]
    bot.send_message(user_id, f"您的提现已被拒绝，请联系客服 ！")
    bot.edit_message_text(message.message.text, message.message.chat.id, message.message.id)

@bot.callback_query_handler(func=lambda c: 'a_w' in c.data)
def accept_ref_withdraw(message):
    user_id = message.data.split(" ")[1]
    am = message.data.split(" ")[-1]
    bot.send_message(user_id, f"{am}$ 提现成功✅")
    bot.edit_message_text(message.message.text, message.message.chat.id, message.message.id)

@bot.callback_query_handler(func=lambda c: 'edit_price' in c.data)
def enter_new_price(message):
    global admin_regime
    bot.edit_message_text(s.language['enter_new_price'], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)
    admin_regime = 'edit_price'

@bot.callback_query_handler(func=lambda c: c.data == 'edit_name')
def enter_new_name(message):
    global admin_regime
    bot.edit_message_text(s.language['enter_new_name'], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)
    admin_regime = 'edit_name'

@bot.message_handler(content_types=['document'])
def upload_accounts(message):
    if message.from_user.id not in s.admin_user_id():
        return
    folder = buying_process_users_q[message.from_user.id]
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    with ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(folder)
    del buying_process_users_q[message.from_user.id]
    bot.send_message(message.chat.id, s.language['success_message'], reply_markup=back_shop_markup)

@bot.message_handler(regexp='')
def got_message(message):
    global admin_regime
    global client
    if message.from_user.id in s.admin_user_id() and (admin_regime == "edit_price" or admin_regime == "edit_name"):
        update_account_info(new_info=message.text, folder=buying_process_users_q[message.from_user.id])
        del buying_process_users_q[message.from_user.id]
        bot.send_message(message.chat.id, s.language['success_message'], reply_markup=back_shop_markup)
        return
    if message.from_user.id in topup_process_users:
        topup_process(message)
        return
    elif message.from_user.id in s.admin_user_id() and admin_regime == "migr":
        change_token(message.text.split(" ")[0], message.text.split(" ")[1])

    elif message.from_user.id in s.admin_user_id() and admin_regime == "transfer_data":
        _transfer_data(*message.text.split(" "))
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)

    elif message.from_user.id in s.admin_user_id() and admin_regime == "e_channel":
        with open("settings.json") as f:
            sett = json.loads(f.read())
    
        if "/" not in message.text:
            bot.send_message(message.chat.id, s.language["not_a_link"], reply_markup=back_capi_m)
        else:
            sett["channel"] = message.text.split(" ")
    
            with open("settings.json", "w") as f:
                f.write(json.dumps(sett))

            bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_capi_m)

    elif message.from_user.id in s.admin_user_id() and admin_regime == "show_all_stats":
        show_stats(message, message.text)
    elif message.from_user.id in s.admin_user_id() and admin_regime == "adm_show_ref":
        sr_markup = telebot.types.InlineKeyboardMarkup()
        sr_btn1 = telebot.types.InlineKeyboardButton(s.language["confirm"], callback_data="adm_show_ref " + message.text)
        sr_btn2 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["manage_refs"])
        sr_markup.add(sr_btn1, sr_btn2)

        bot.send_message(message.chat.id, "UID: " + message.text, reply_markup=sr_markup)

    elif message.from_user.id in s.admin_user_id() and admin_regime == "rem_adms":
        try:
            if not _rem_adm(int(message.text)):
                bot.send_message(message.chat.id, s.language["rem_adms_err"], reply_markup=change_p_markup)
                return
        except Exception as exc:
            print(exc.args)

        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=change_p_markup)
    elif message.from_user.id in s.admin_user_id() and admin_regime == "add_adm":
        try:
            uid = int(message.text)
            _add_adm(uid)
            bot.send_message(message.chat.id, s.language["success_message"], reply_markup=change_p_markup)
        except Exception as exc:
            bot.send_message(message.chat.id, s.language["add_adm_error"], reply_markup=change_p_markup)
    elif message.from_user.id in s.admin_user_id() and "change_smm_rate" in admin_regime:
        network = admin_regime.split(" ")[-1]
        print(network)
        rate = str(Decimal("1") + (Decimal(message.text) / Decimal(100)))
        rate = float(rate)
        cr_markup = telebot.types.InlineKeyboardMarkup()
        cr_btn1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=f"smm_shop {network}")
        cr_markup.add(cr_btn1)
        if _change_rate(rate, network):
            bot.send_message(message.chat.id, s.language["success_message"], reply_markup=cr_markup)
        else:
            bot.send_message(message.chat.id, s.language["change_rate_error"], reply_markup=cr_markup)
    elif message.from_user.id in s.admin_user_id() and admin_regime == 'change_wm':
        with open("welcome_settings.json") as f:
            sett = json.loads(f.read())
        sett["welcome_message"] = message.text
        with open("welcome_settings.json", "w") as f:
            f.write(json.dumps(sett))
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)

    elif message.from_user.id in s.admin_user_id() and admin_regime == 'smm_api_e':
        with open("settings.json") as f:
            sett = json.loads(f.read())
        sett["smm_api"] = message.text
        with open("settings.json", "w") as f:
            f.write(json.dumps(sett))
        
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)
    elif message.from_user.id in s.admin_user_id() and admin_regime == 'admin_enter_support':
        with open("settings.json") as f:
            sett = json.loads(f.read())
        sett["support"] = message.text
        
        with open("settings.json", "w") as f:
            f.write(json.dumps(sett))

        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)

    elif message.from_user.id in s.admin_user_id() and admin_regime == 'cryptomus_api_e':
        with open("settings.json") as f:
            sett = json.loads(f.read())
        sett["cryptomus"] = message.text.split(" ")
        with open("settings.json", "w") as f:
            f.write(json.dumps(sett))
        
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)
        client = pyCryptomusAPI(merchant_uuid=s.merchant_uuid(), payment_api_key=s.payment_api())
    elif message.from_user.id in s.admin_user_id() and admin_regime == 'topup':
        id = message.text.split(" ")[0]
        amount = Decimal(message.text.split(" ")[1])
       
        _add_balance(id, amount)
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_adm_markup)

    elif message.from_user.id in s.admin_user_id() and admin_regime == 'adm_add_token':
        _admin_add_token(message.text.split(" ")[0], message.text.split(" ")[1])
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=manage_t_markup)
        subprocess.call(["shutdown", "-r", "-t", "0"])

    elif message.from_user.id in s.admin_user_id() and admin_regime == 'adm_rm_token':
        _admin_remove_token(message.text)
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=manage_t_markup)

    elif message.from_user.id in s.admin_user_id() and 'add_smm_service' in admin_regime:
        _add_service(message.text, admin_regime.split(" ")[-1])

        admin_bkm = telebot.types.InlineKeyboardMarkup()
        bkm_1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data="smm_shop " + admin_regime.split(" ")[-1])
        admin_bkm.add(bkm_1)
        admin_regime = ''
        bot.send_message(message.from_user.id, s.language['success_message'], reply_markup=admin_bkm)
        return 
    elif message.from_user.id in s.admin_user_id() and admin_regime == "get_payments":
        get_payments(message)
        return
    elif message.from_user.id in s.admin_user_id() and "change_ref_perc" in admin_regime:
        _set_ref_percent(message.text)
        bot.send_message(message.chat.id, s.language["success_message"], reply_markup=manage_r_markup)
    elif message.from_user.id in s.admin_user_id() and "look_orders" in admin_regime:
        get_orders(message)
        return
    elif message.from_user.id in s.admin_user_id() and admin_regime == "d_acc":
        admin_regime = ''
        _send_accounts(buying_process_users_q[message.from_user.id], int(message.text), message.chat.id, True)
        del buying_process_users_q[message.from_user.id]
        bot.send_message(message.from_user.id, s.language['success_message'], reply_markup=back_shop_markup)
        return
    elif message.from_user.id in ref_list:
        ref_list.remove(message.from_user.id)
        if _withdraw_ref(message.from_user.id, message.text):
            bot.send_message(message.chat.id, s.language["success_message"], reply_markup=back_ref_markup)
        else:   
            bot.send_message(message.chat.id, s.language["money_error"], reply_markup=back_ref_markup)

    elif message.from_user.id not in buying_process_users_q.keys():
        if len(message.text.split(' ')) >= 2 or len(message.text.split('|')) >= 2:
            confirmation_process(message, smm=True)
        return
    else:
        confirmation_process(message, smm=False)

def confirmation_process(message, smm):
        global waiting_order
        final_message = '阅读条款和条件并确认购买\n\n'
        data_lst = {"odata": [], "quantity": 0, "amount": 0.00, "id": str(random.randint(10000, 99999))}
        if smm:
            msgt = message.text
            service_id = smm_buying_process[message.from_user.id]
            service = _get_service(service_id)
            if "\n" not in message.text:
                msgt += "\n"
            for msg in msgt.split("\n"):
                if not msg:
                    break
                data = {"link": None,"quantity": None, "answer_number": None, "username": None, "min": None, "max": None, "delay": None, "service_id": None, "smm": smm, "comments": "", "user_id": message.from_user.id, "id": str(random.randint(10000, 99999))}

                data["service_id"] = service_id
                type = service["type"]
                if type == 'Poll':
                    if "|" in msg:
                        data["link"] = msg.split('|')[0]
                        data["answer_number"] = msg.split(' ')[2]
                        data["quantity"] = msg.split(' ')[1]
                    else:
                        data["link"] = msg.split(' ')[0]
                        data["answer_number"] = msg.split(' ')[2]
                        data["quantity"] = msg.split(' ')[1]
                elif type == 'Default':
                    if "|" in msg:
                        data["link"] = msg.split('|')[0]
                        data["quantity"] = msg.split('|')[1]                
                    else:
                        print(msg)
                        data["link"] = msg.split(' ')[0]
                        data["quantity"] = msg.split(' ')[1]
                elif type == 'Subscriptions':
                    if "|" in msg:
                        data["username"] = msg.split('|')[0]
                        data["min"] = msg.split('|')[1]
                        data["max"] = msg.split('|')[2]
                        data["delay"] = msg.split('|')[3]
                    else:
                        data["username"] = msg.split(' ')[0]
                        data["min"] = msg.split(' ')[1]
                        data["max"] = msg.split(' ')[2]
                        data["delay"] = msg.split(' ')[3]
                elif type == "Invites from Groups":
                    if "|" in msg:
                        data["link"] = msg.split("|")[0]
                        data["quantity"] = msg.split("|")[1]
                        data["comments"] = msg.split("|")[2]
                    else:
                        data["link"] = msg.split(" ")[0]
                        data["quantity"] = msg.split(" ")[1]
                        data["comments"] = msg.split(" ")[2]
                elif type == "Custom Comments":
                    if "|" in msg:
                        data["link"] = msg.split("|")[0]
                        data["cust_comments"] = msg.split("|")[1]
                    else:
                        data["link"] = msg.split(" ")[0]
                        data["cust_comments"] = msg.split(" ")[1]
                    data["quantity"] = len(data["cust_comments"].split(","))

                rate = Decimal(service["rate"]) / Decimal("6.7")
                rate = Decimal(rate) / Decimal("1000")
                data["rate"] = rate.quantize(Decimal("2.00"))
                

                if data["quantity"] != None:
                    
                    backtoservice = telebot.types.InlineKeyboardMarkup()
                    b_btn1 = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=f"network {service['network']} smmselect {service['service']}")
                    backtoservice.add(b_btn1)

                    amount = Decimal(rate) * Decimal(data["quantity"])
                    data_lst["quantity"] += int(data["quantity"])
                
                    if int(data["quantity"]) > int(service["max"]):
                        bot.send_message(message.chat.id, s.language["max_quant"] + "(" + service["max"] + ")", reply_markup=backtoservice)
                        return
                    elif int(data["quantity"]) < int(service["min"]):
                        bot.send_message(message.chat.id, s.language["min_quant"] + "(" + service["min"] + ")", reply_markup=backtoservice)
                        return

                else:
                    amount = Decimal(rate) * Decimal(data["max"])
                amount = Decimal(amount) * Decimal(service["resell"])
                data["amount"] = round(amount, 2)
                data_lst["amount"] = Decimal(data_lst["amount"]) + Decimal(data["amount"])
                data["name"] = service["name"]
                data_lst["odata"].append(data)

            if data_lst["quantity"] == 0:
                data_lst["quantity"] = "None"
            else:
                data_lst["quantity"] = str(data_lst["quantity"])

            final_message += f'*服务:* {data["name"]}\n\n*单价:*  {round(Decimal(service["rate"]) / Decimal("6.7"),2)} $ = 每 (1000)\n\n'
            menu_btn = types.InlineKeyboardButton(s.language['back_to_shop'], callback_data=s.language["smm_button"])
        else:
            data["id"] = buying_process_users_q[message.from_user.id]
            data["quantity"] = Decimal(message.text)
            data["name"] = get_account(data['id'])["name"]
            if get_account(data["id"])['quantity'] < data["quantity"]:
                bot.send_message(message.chat.id,s.language["amount_error"], reply_markup=back_shop_markup)
                return
            del buying_process_users_q[message.from_user.id]
            data["rate"] = Decimal(get_account(data["id"])['price'])
            amount = Decimal(data["rate"]) * Decimal(data["quantity"])
            data["amount"] = amount.quantize(Decimal("2.00"))
            final_message += f'金 额:  {data["rate"]} $\n\n'
            menu_btn = types.InlineKeyboardButton(s.language['back_to_shop'], callback_data=s.language["shop_button"])

        data_lst["amount"] = str(data_lst["amount"].quantize(Decimal("2.00")))             
        final_message += f'*费用:*  {data_lst["amount"]} $\n\n*余额:*  {get_balance(message.from_user.id)}'
        confirmation_markup = types.InlineKeyboardMarkup()
        confirmation_btn = types.InlineKeyboardButton(s.language['confirm_button'], callback_data=f'order {data_lst["id"]}')
        confirmation_markup.add(confirmation_btn, menu_btn)
        waiting_order[data_lst["id"]] = multiprocessing.Queue()
        waiting_order[data_lst["id"]].put(data_lst)

        bot.send_message(message.chat.id, final_message, reply_markup=confirmation_markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data == s.language['add_token'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['remove_token'])
def admin_change_tokens(message):
    global admin_regime
    if message.data == s.language["add_token"]:
        admin_regime = "adm_add_token"
        bot.edit_message_text(s.language["e_token_a_uid"], message.message.chat.id, message.message.id, reply_markup=manage_t_markup)
    else:
        admin_regime = "adm_rm_token"
        bot.edit_message_text(s.language["e_token"], message.message.chat.id, message.message.id, reply_markup=manage_t_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language['capi_button'])
def capi_btn(message):
    bot.edit_message_text(s.language["capi_text"], message.message.chat.id, message.message.id, reply_markup=choose_api_markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data == s.language['e_channel'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['cryptomus_api'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['smm_api'])
def admin_enter_api(message):
    with open("settings.json") as f:
        sett = json.loads(f.read())
    
    csmm_api = sett["smm_api"]
    ccrypto_api = " ".join(sett["cryptomus"])

    global admin_regime
    r_markup = telebot.types.InlineKeyboardMarkup()
    r_btn = telebot.types.InlineKeyboardButton(s.language["menu_button"], callback_data=s.language["capi_button"])
    r_markup.add(r_btn)
    if message.data == s.language["smm_api"]:
        bot.edit_message_text(f"当前网站API: {csmm_api}\n\n" + s.language["smm_api_e"], message.message.chat.id, message.message.id, reply_markup=r_markup)
        admin_regime = "smm_api_e"
    elif message.data == s.language["cryptomus_api"]:
        bot.edit_message_text(f"当前支付API: {ccrypto_api}\n\n" + s.language["cryptomus_api_e"], message.message.chat.id, message.message.id, reply_markup=r_markup)
        admin_regime = "cryptomus_api_e"
    elif message.data == s.language["e_channel"]:
        admin_regime = "e_channel"
        bot.edit_message_text(s.language["e_uid_a_link"], message.message.chat.id, message.message.id, reply_markup=r_markup)

def _admin_add_token(u_id, token):
    with open("/home/ubuntu/bot/tokens.json") as f:
        tokens = json.loads(f.read())
    
    try:
        tokens[u_id].append(token)
    except KeyError:
        tokens[u_id] = [token]

    with open("/home/ubuntu/bot/tokens.json", "w") as f:
        f.write(json.dumps(tokens))

def _admin_remove_token(token):
    with open("/home/ubuntu/bot/tokens.json") as f:
        tokens = json.loads(f.read())
    
    [tokens[uid].remove(token) for uid, toks in tokens.items() if token in toks]

    with open("/home/ubuntu/bot/tokens.json", "w") as f:
        f.write(json.dumps(tokens))

def _admin_get_tokens():
    with open("/home/ubuntu/bot/tokens.json") as f:
        return json.loads(f.read())

@bot.callback_query_handler(func=lambda c: 'order' in c.data)
def buying_process(message):
    global waiting_order
    order_id = message.data.split(" ")[-1]
    order_data = waiting_order[order_id].get(timeout=5)
    name = order_data["odata"][0]["name"]
    rate = Decimal(order_data["odata"][0]["rate"])

    if order_data["odata"][0]["smm"]:
        service_id = order_data["odata"][0]["service_id"]
        amount = order_data["amount"]
        print(amount)

        if _make_payment(str(message.from_user.id), amount):
            hid = _add_smm_order(str(message.from_user.id), service_id, order_data)
            if "_" in order_data["odata"][0]["link"]:
                final_message = f"您的订单已收到\n\nID: {hid}\n服务: {order_data['odata'][0]['name']}\n链接: {order_data['odata'][0]['link']}...\n数量: {order_data['quantity']}\n费用: {order_data['amount']}$\n"   
                bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=back_smm_markup)
            else:
                final_message = f"*您的订单已收到*\n\n*ID:* {hid}\n*服务:* {order_data['odata'][0]['name']}\n*链接:* {order_data['odata'][0]['link']}...\n*数量:* {order_data['quantity']}\n*费用:* {order_data['amount']}$\n"
                print(final_message)
            bot.edit_message_text(final_message, message.message.chat.id, message.message.id, reply_markup=back_smm_markup, parse_mode="Markdown")
        else:
            bot.edit_message_text(s.language['money_error'], message.message.chat.id, message.message.id, reply_markup=back_smm_markup)

    else:
        if get_account(order_data["id"])['quantity'] < quantity:
            bot.edit_message_text(s.language['amount_error'], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)
            return
        amount = order_data["amount"]
        print(amount)

        if _make_payment(str(message.from_user.id), amount):
            add_order(order_data["user_id"], name, quantity, amount)
            _send_accounts(order_data["id"], quantity, message.message.chat.id)
            bot.edit_message_text(s.language['success_message'], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)
        else:
            bot.edit_message_text(s.language['money_error'], message.message.chat.id, message.message.id, reply_markup=back_shop_markup)

@bot.callback_query_handler(func=lambda c: c.data == s.language['back_to_crypto'])
@bot.callback_query_handler(func=lambda c: c.data == s.language['balance'])
def crypto_selecter(message):
    if not verify(message.from_user.id):
        restrict(message)
        return

    bot.edit_message_text(s.language['select_currency'],message.message.chat.id, message.message.id, reply_markup=currency_markup)
    if message.from_user.id in topup_process_users:
        topup_process_users.remove(message.from_user.id)

def update_account_info(new_info, folder):
    with open(f'{folder}/info.json', 'rb') as f:
        info_json = codecs.decode(f.read(), 'utf-8-sig', errors='ignore')
    info_dict = json.loads(info_json)
    if admin_regime == 'edit_price':
        info_dict['price'] = new_info
    elif admin_regime == 'edit_name':
        info_dict['name'] = new_info
    with open(f'{folder}/info.json', 'w') as f:
        info_json = json.dumps(info_dict)
        f.write(info_json)

def _get_service(id: str):
    with open('saved_smm.json') as f:
        saved_smm_json = f.read()
    saved_smm_dict = json.loads(saved_smm_json)
    for category in saved_smm_dict.keys():
        for service in saved_smm_dict[category]:
            if service["service"] == id:
                service_output = service

                with open("networks.json") as f:
                    netwks = json.loads(f.read())
                for net, services in netwks.items():
                    for service in services:
                        if str(service_output["service"]) == str(service):
                            service_output["network"] = net

                sdata = r.get('https://db-laren.com/services')
                sdata = sdata.text
                soup = BeautifulSoup(sdata, features="html.parser")
                for each_div in soup.findAll('div',{'class':'d-none'}):
                    if each_div["id"] == f'service-description-id-31-{id}':
                        service_output["description"] = str(each_div.contents).replace('<br/>', '\n')
                        service_output["description"] = service_output["description"].replace('\\n', '').replace(',', '').replace('[', '').replace(']', '').replace("'", "")
                        service_output["description"] = service_output["description"].replace("                               ", "")
                        return service_output
    service_output["description"] = None

    return service_output

def _send_accounts(id, amount, chat_id, admin=False):
    if not admin:
        _add_stats(orders=True)
    account = get_account(id)
    order_id = random.randint(10000, 99999)
    counter = 0
    with ZipFile(f'{order_id}.zip', 'w') as f:
        for filename in os.listdir(account['folder']):
            if filename != 'info.json' and counter < amount:
                f.write(f'{account["folder"]}/{filename}', arcname=f'/{filename}')
                counter += 1
            elif counter >= amount:
                break
    counter = 0
    for filename in os.listdir(account['folder']):
        if filename != 'info.json' and counter < amount:
            if os.path.isdir(f'{account["folder"]}/{filename}'):
                shutil.rmtree(f'{account["folder"]}/{filename}')
            else:
                os.remove(f'{account["folder"]}/{filename}')
            counter += 1
        elif counter >= amount:
            break

    with open(f'{order_id}.zip', 'rb') as f:
        bot.send_document(chat_id, f)

try:
    check = open("tokens.json")
    check.close()
    _init_bot()
except Exception as exc:
    print(f'Error occured: {traceback.format_exc()}')

print("started polling")

while True:
    try:
        bot.polling()
    except Exception as exception:
        print(f'Error occured: {traceback.format_exc()}')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
