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
    "smm_api_e": "输入网站API",
    "cryptomus_api_e": "输入支付UID和API",
    "capi_button": "管理API",
    "capi_text": "[支付API申请地址](https://app.cryptomus.com/signup?ref=J6Yaqw) - 先注册一个账号，具体问我把\n\n网站api获取：登录我们的网站，点击右上角 - 设置按钮 -翻到最下面\nAPI密匙 - 生成新的",
    "cryptomus_api": "支付API",
    "smm_api": "网站API",
    "success_p_message": "您已经充值成功✅",
    'balance': '💰 充值',
    'give_b': '人工充值',
    'stats': 'show statistic',
    'add_token': '添加令牌',
    'e_token_a_uid': '手动添加用户令牌UID',
    'e_token': '输入令牌',
    'show_tokens': '显示令牌',
    'remove_token': '删除令牌',
    'edit_name': '更换名字',
    'edit_price': '改变价格',
    'change_smm_rate': '调整价格',
    'show_price': '*💰价格:* ',
    'show_accounts_nickname': '*✅您正在购买:* ',
    'show_accounts_in_stock': '*🏢库存:* ',
    'warning_while_buying': '输入你购买的数量❗',
    'enter_new_perc': '填写新的百分比',
    'enter_new_price': '输入新价格',
    "accept": "确认",
    "reject": "拒绝",
    "ref_stats": "📊查看数据",
    "ref_withdraw": "💰收益提现",
    'ref_button': '💰加入赚钱',
    'change_ref_perc': '设置收益比例',
    'admin_enter_support': '修改联系方式',
    'enter_new_name': '输入新名称',
    "Pending": "代办的",
    "In progress": "进行中",
    "Completed": "完成",
    "Partial": "部分退款",
    "Processing": "处理中",
    "Canceled": "取消",
    "your_balance_is": '您的余额为',
    "min_topup_err": "最低金额 0.5 USD",
    "admin_topup": "输入您的用户名和金额",
    "enter_am_usd": "*❗️请回复我您需充值的USDT金额❗️*\n（注意：最小充值USDT数为：1）",
    "get_payments": "充值记录",
    "look_orders": "查看订单",
    "enter_id": "输入用户 ID",
    'enter_quantity': '输入数量',
    'payment_link_created': '这是您的付款地址: ',
    'amount_error': '对不起，没有存货，联系客服补充货源',
    'support_button': '✉ 联系客服',
    'payment_wallet_generated': '此充值地址*50分钟内*有效，过期后请重新生成新的地址❗️',
    'remove_acc': '删除帐户',
    'menu_button': '🔙 返回',
    'shop_button': '🛒 TG 协 议 号',
    'admin_panel': '控制菜单',
    'back_to_shop': '',
    'back_to_directories': '🔙 返回目录',
    'remove_smm_service': '删除此服务',
    'back_to_crypto': '🔙 货币选择',
    'page': '=> 下一页',
    'general_orders_button': '📜 历史订单',
    'smm_orders_button': '🔵 订购商品',
    'shop_orders_button': '🔴 商店',
    'confirm_button': '确认',
    'payments_button': '📜 充值记录',
    'select_currency': '请选择您的支付方式',
    'statistics': '上周统计',
    'statistics_recharge_amount': '今日充值: ',
    'statistics_new_people': '今日新增人数: ',
    'statistics_orders': '今日下单多少用户: ',
    'welcome_message_1': '欢迎, ',
    'welcome_message_2': ' ✋\nThis is a test message displayed after user nickname 💰',
    'money_error': '你没有足够的余额',
    "download_acc": "下载",
    'successful_order': '我们正在准备您的订单...',
    'enter_s_message': '输入新的客服联系方式',
    'success_message': '您已经下单成功✅',
    'enter_link_and_quality': {'Default': '*下单格式：*链接空格数量 或者 链接|数量',
                               'Poll': '输入链接、数量和答案编号',
                               'Subscriptions': '输入用户名、最小和最大计数、延迟',
                               'Invites from Groups': '输入链接、数量和用户名，以逗号分隔。 示例：t.me/group1 10 用户名 1、用户名 2、用户名 2。', 
                               'Custom Comments': '输入链接和自定义注释，以逗号分隔。 示例：t.me/examplghe t.me/gr1、t.me/gr2、t.me/gr3'},
    'smm_button': '🛒 订购商品',
    'smm_enter_data': 'enter link and quantity',
    'change_wm_button': '设置欢迎信息',
    'enter_wm': '输入欢迎信息',
    'admin_add_service_button': 'add service',
    'change_rate_error': '你没有添加任何服务',
    'admin_enter_rate': '设置百分比',
    "add_adm_button": "添加管理员",
    "enter_new_adm": "输入新的管理员UID",
    "change_permissions": "设置管理",
    "show_admins": "显示管理员",
    "rem_admins": "删除管理员",
    "add_adm_error": "您输入了错误的UID",
    'admin_smm_enter_data': '输入网站的服务ID',
    'rem_adms_err': '抱歉，您无法删除此管理员',
    'manage_tokens': '管理令牌',
    "manage_refs": "管理转移",
    "enter_uid": "输入UID",
    "confirm": "确认",
    "show_tok_stat": "显示复制的bot的统计信息",
    "e_channel": "输入频道",
    "e_uid_a_link": "输入频道ID和链接",
    "go": "转到频道",
    "verify": "验证",
    "restricted": "你应该订阅我们的频道才能使用bot",
    "not_a_link": "抱歉，您输入了错误的链接",
    "transfer_data": "迁移数据",
    "enter_transfer_d": "输入旧的UID和新的UID",
    "min_quant":"数量小于最小下单数量",
    "max_quant":"数量超过最大下单数量",
    "cbot_token": "迁移到新的bot令牌",
    "enter_o_n_token": "输入旧令牌和新令牌",

}
