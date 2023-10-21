from telebot import types
import settings as s

admin_markup = types.InlineKeyboardMarkup()
admin_btn_1 = types.InlineKeyboardButton('添加群组', callback_data=f'add_group {s.get_password()}')
admin_btn_2 = types.InlineKeyboardButton('删除群组', callback_data=f'remove_group {s.get_password()}')
admin_markup.add(admin_btn_1, admin_btn_2)