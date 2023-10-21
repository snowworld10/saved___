# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random
import threading
import time
import traceback
import telebot
import settings as s
import markups
import smm_orders_processing


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(exception):
        print(exception)
        return True
# logger.error(exception)

old_bot = telebot.TeleBot(s.token[0], exception_handler=ExceptionHandler)
new_bot = telebot.TeleBot(s.token[1], exception_handler=ExceptionHandler)

def threading_exceptions_hook(args):
    print(f'Error occured: {args.exc_type} {args.exc_value}')
    new_thread = None
    targets = {'start_working function': start_working, 'smm_orders_processing function': smm_orders_processing.orders_checking, 'bot_admin_panel_thread': old_bot.polling}     
    if args.thread.name in ['start_working function', 'smm_orders_processing function', 'bot_admin_panel thread']:
        print(args.thread.name)
        new_thread = threading.Thread(target=targets[args.thread.name], name=args.thread.name)
    if new_thread:
        new_thread.start()

@old_bot.message_handler(commands=['receive'])
@new_bot.message_handler(commands=['receive'])
def receive_done_orders(message):
    if message.from_user.username not in os.listdir('ready_orders'):
        os.mkdir(f'/home/ubuntu/notifications_bot/ready_orders/{message.from_user.username}')

    if len(os.listdir(f'ready_orders/{message.from_user.username}')) == 0:

# It is not a solution! Remove this after new bot won't be demanded!
        try:
            new_bot.send_message(message.from_user.id, '抱歉，您没有任何已完成的订单')
        except Exception as exc:
            pass
        try:
            old_bot.send_message(message.from_user.id, '抱歉，您没有任何已完成的订单')
        except Exception as exc:
            pass

    else:
        for order in os.listdir(f'/home/ubuntu/notifications_bot/ready_orders/{message.from_user.username}'):

            with open(f'/home/ubuntu/notifications_bot/ready_orders/{message.from_user.username}/{order}','rb') as f:
                try:
                    new_bot.send_document(message.from_user.id, f.read(), visible_file_name=f'{order}.txt')
                except Exception as exc:
                    pass
            with open(f'/home/ubuntu/notifications_bot/ready_orders/{message.from_user.username}/{order}', 'rb') as f:
                try:
                    old_bot.send_document(message.from_user.id, f.read(), visible_file_name=f'{order}.txt')
                except Exception as exc:
                    pass

            os.remove(f'/home/ubuntu/notifications_bot/ready_orders/{message.from_user.username}/{order}')

@new_bot.message_handler(commands=['admin'])
@old_bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.from_user.id != s.admin_user_id:
        return
    old_bot.send_message(message.from_user.id, '输入控制面板密码')
    new_bot.send_message(message.from_user.id, '输入控制面板密码')

@new_bot.message_handler(regexp=s.get_password())
@old_bot.message_handler(regexp=s.get_password())
def admin_control(message):
    if message.from_user.id != s.admin_user_id:
        return
    old_bot.send_message(message.from_user.id, '选择一个动作', reply_markup=markups.admin_markup)
    new_bot.send_message(message.from_user.id, '选择一个动作', reply_markup=markups.admin_markup)

#@new_bot.message_handler(content_types=['new_chat_members', 'left_chat_members', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'pinned_message'])
@old_bot.message_handler(content_types=['new_chat_members', 'left_chat_members', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'pinned_message'])
def welcome_message(message):
    if message.new_chat_members:
        for chat_member in message.new_chat_members:
            if chat_member.id == old_bot.get_me().id:
               old_bot.send_message(message.chat.id, s.wlcm_message)
               new_bot.send_message(message.chat.id, s.wlcm_message)
    with open('/home/ubuntu/notifications_bot/chats.txt','a') as f:
        if str(message.chat.id) not in f.read().splitlines():
            f.write(f'{message.chat.id}\n')

    old_bot.delete_message(message.chat.id, message.id)

@new_bot.callback_query_handler(func=lambda c: c.data == f'add_group {s.get_password()}')
@old_bot.callback_query_handler(func=lambda c: c.data == f'add_group {s.get_password()}')
def admin_add_group(message):
    s.admin_regime = 'add_group'
    old_bot.edit_message_text('输入以空格分隔的组', message.message.chat.id, message.message.id)
    new_bot.edit_message_text('输入以空格分隔的组', message.message.chat.id, message.message.id)

@new_bot.callback_query_handler(func=lambda c: c.data == f'remove_group {s.get_password()}')
@old_bot.callback_query_handler(func=lambda c: c.data == f'remove_group {s.get_password()}')
def admin_remove_group(message):
    s.admin_regime = 'remove_group'
    old_bot.edit_message_text('输入以空格分隔的组', message.message.chat.id, message.message.id)
    new_bot.edit_message_text('输入以空格分隔的组', message.message.chat.id, message.message.id)

@new_bot.callback_query_handler(func=lambda c: c.data == f'remove_group {s.get_password()}')
@old_bot.message_handler(content_types=['text'])
def got_message(message):
    if message.from_user.id == s.admin_user_id and s.admin_regime == 'add_group':
        groups = message.text.replace(' ', '\n')
        groups += '\n'
        with open('/home/ubuntu/notifications_bot/chats.txt','a') as f:
            f.write(groups)
    elif message.from_user.id == s.admin_user_id and s.admin_regime == 'remove_group':
        if message.text.count(' ') > message.text.count('\n'):
            groups = message.text.split(' ')
        else:
            groups = message.text.split('\n')

        with open('/home/ubuntu/notifications_bot/chats.txt') as f:
            previous_groups_list = f.read().splitlines()

        new_groups_list = previous_groups_list
        for previous_group in previous_groups_list:
            for group in groups:
                if group == previous_group:
                    new_groups_list.remove(group)
        with open('/home/ubuntu/notifications_bot/chats.txt','w') as f:
            f.write('\n'.join(new_groups_list))

    old_bot.send_message(s.admin_user_id, '成功地')
    new_bot.send_message(s.admin_user_id, '成功地')
    s.admin_regime = ''

def start_working():
    while True:
        notifications_list = []
        groups_list = []
        with open('/home/ubuntu/notifications_bot/notifications.txt') as f:
            for line in f.read().splitlines():
                notifications_list.append(line)
        with open('/home/ubuntu/notifications_bot/chats.txt') as f:
            for line in f.read().splitlines():
                groups_list.append(line)

        for group in groups_list:
            notification = random.choice(notifications_list)

            try:
                int(group)
                group_formatted = group
            except ValueError:
                group_formatted = '@' + group.split('/')[-1]

            try:
                old_bot.send_message(group_formatted, notification)
            except:
                with open("chats.txt") as f:
                    chats = []
                    for line in f.read().splitlines():
                        chats.append(line)
                    if group in chats:
                        chats.remove(group)
                    else:
                        old_bot.send_message(s.admin_user_id, f'向群组发送消息时出错 {group}: {traceback.format_exc()}')
                print(traceback.format_exc())
            
            time.sleep(14400 // len(groups_list))
        time.sleep(300)

if __name__ == '__main__':
    threading.excepthook = threading_exceptions_hook
    start_working_function_thread = threading.Thread(target=start_working, name='start_working function')
    start_working_function_thread.start()
    smm_orders_processing_thread = threading.Thread(target=smm_orders_processing.orders_checking, name='smm_orders_processing function')
    smm_orders_processing_thread.start()
    bot_admin_panel_thread = threading.Thread(target=old_bot.polling, name='bot_admin_panel thread')
    bot_admin_panel_thread.start()
    new_bot.polling()
