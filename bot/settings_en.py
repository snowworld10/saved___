import json
import io
import sys
import os

def wm():
    with open("welcome_settings.json") as f:
        return json.loads(f.read())["welcome_message"]

def admin_user_id():
    with open("settings.json") as f:
        return json.loads(f.read())["admins"]

def merchant_uuid():
    with open("settings.json") as f:
        return json.loads(f.read())["cryptomus"][0]

def payment_api():
    with open("settings.json") as f:
        return json.loads(f.read())["cryptomus"][1]

def support():
    with open("settings.json") as f:
        return json.loads(f.read())["support"]

def cur_token():
    with open("cur_token.json") as f:
        return json.loads(f.read())["token"]

def smm_panel_api_token():
    with open("settings.json") as f:
        return json.loads(f.read())["smm_api"]

token = cur_token()
admin_username = 'QBVIP2'
language = {
    "smm_api_e": "Enter new smm panel API key",
    "cryptomus_api_e": "Enter new cryptomus api key",
    "capi_button": "API settings",
    "capi_text": "[Register cryptomus account](https://app.cryptomus.com/signup?ref=J6Yaqw) - we use cryptomus as a merchant\nPlease register an account to get payments from your clients, then write support\nclick API KEY - generate new",
    "cryptomus_api": "Cryptomus API",
    "smm_api": "SMM panel api key",
    "success_p_message": "Successful payment ✅",
    'balance': '💰 balance',
    'give_b': 'Give balance',
    'stats': 'show statistic',
    'add_token': 'add token',
    'e_token_a_uid': 'Enter token and admin UID separated by space ⬇️',
    'e_token': 'Enter token',
    'show_tokens': 'Show tokens',
    'remove_token': 'Remove token',
    'edit_name': 'Edit name📝',
    'edit_price': 'Edit price📝',
    'change_smm_rate': 'Change profit percent',
    'show_price': '*💰Price:* ',
    'show_accounts_nickname': '*✅Nickname:* ',
    'show_accounts_in_stock': '*🏢Accounts in stock:* ',
    'warning_while_buying': 'Enter the quantity you purchased❗',
    'enter_new_perc': 'Enter new resell percent',
    'enter_new_price': 'Enter new price',
    "accept": "Accept",
    "reject": "Reject",
    "ref_stats": "📊Statistic",
    "ref_withdraw": "💰Withdraw",
    'ref_button': '💰Refferal system',
    'change_ref_perc': 'Change percents',
    'admin_enter_support': 'Enter support message',
    'enter_new_name': 'Enter new name',
    "Pending": "Pending",
    "In progress": "In progress",
    "Completed": "In progress",
    "Partial": "Partial",
    "Processing": "Processing",
    "Canceled": "Canceled",
    "your_balance_is": 'Your balance: ',
    "min_topup_err": "Sorry, minimal amount is 0.5 USD",
    "admin_topup": "Enter username and price",
    "enter_am_usd": "*❗Please send the amount you want to topup in USD❗️*\n（Minimal amount is：1）",
    "get_payments": "Payments",
    "look_orders": "Orders",
    "enter_id": "Enter ID",
    'enter_quantity': 'Enter quantity',
    'payment_link_created': 'Payment wallet generated: ',
    'amount_error': 'Sorry, accounts not in stock. Please contact support for recharge',
    'support_button': '✉ Support',
    'payment_wallet_generated': 'Wallet is available for *50 minutes*，please be careful❗️',
    'remove_acc': 'Remove',
    'menu_button': '🔙 back',
    'shop_button': '🛒 shop',
    'admin_panel': 'admin panel',
    'back_to_shop': '',
    'back_to_directories': '🔙 back to catalogues',
    'remove_smm_service': 'remove',
    'back_to_crypto': '🔙 back to currencies',
    'page': '=> page',
    'general_orders_button': '📜 orders',
    'smm_orders_button': '🔵 smm panel',
    'shop_orders_button': '🔴 shop',
    'confirm_button': 'confirm',
    'payments_button': '📜 payments',
    'select_currency': 'select currency',
    'statistics': 'statistics',
    'statistics_recharge_amount': 'recharged: ',
    'statistics_new_people': 'new people invited: ',
    'statistics_orders': 'orders: ',
    'welcome_message_1': 'hi, ',
    'welcome_message_2': ' ✋\nThis is a test message displayed after user nickname 💰',
    'money_error': 'Sorry, you dont have enough money on balance',
    "download_acc": "download",
    'successful_order': 'your order has started completing...',
    'enter_s_message': 'enter support message',
    'success_message': 'Success✅',
    'enter_link_and_quality': {'Default': '*order format：*1 line -1 order. Link and quantity are separated by space, or"|" symbol',
                               'Poll': '',
                               'Subscriptions': 'enter username, min, max and delay *separated by space or "|" symbol. 1 line - 1 order*',
                               'Invites from Groups': '*order format: * enter link and quantity separated by space or "|" symbol. Then specify the list of usernames separated by ","*. Example: example.com 10 username1, username2, username3', 
                               'Custom Comments': '*Order format: enter link and specify a comments* example：t.me/examplegr comment1, comment2, comment3'},
    'smm_button': '🛒 smm panel',
    'smm_enter_data': 'enter link and quantity',
    'change_wm_button': 'welcome message',
    'enter_wm': 'Enter new welcome message',
    'admin_add_service_button': 'add service',
    'change_rate_error': 'Sorry, you havent added any service',
    'admin_enter_rate': 'Enter new resell rate',
    "add_adm_button": "Add new admin",
    "enter_new_adm": "Enter UID",
    "change_permissions": "Manage permissions",
    "show_admins": "Show admins assigned",
    "rem_admins": "Remove admins",
    "add_adm_error": "Please, enter the right UID",
    'admin_smm_enter_data': 'Enter service ID',
    'rem_adms_err': 'Sorry, this admin cant be deleted',
    'manage_tokens': 'Manage tokens',
    "manage_refs": "Manage refferals",
    "enter_uid": "Enter UID",
    "confirm": "Confirm",
    "show_tok_stat": "Show copied bot statistic",
    "e_channel": "Enter channel",
    "e_uid_a_link": "Enter channel ID and link separated by space",
    "go": "Go",
    "verify": "Verify",
    "restricted": "You should subscribe our channel to use bot",
    "not_a_link": "Please, enter the right link",
    "transfer_data": "Transfer data",
    "enter_transfer_d": "Enter the old UID and a new one",
    "min_quant":"Sorry, the quantity is less then min",
    "max_quant":"Sorry, the quantity is more then max",
    "cbot_token": "bot token",
    "enter_o_n_token": "enter old and new token",

}
