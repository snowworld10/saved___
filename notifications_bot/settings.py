admin_regime = ''
admin_user_id = 5355199432
wlcm_message = '欢迎使用机器人，本机器人是：电报拉人网 dblaren.com 专用机器人，自动删除进群消息和退群消息，设置管理即可！无需其它设置！'
smm_panel_api_token = 'uy03lg8ak2x3qj7ju2a92tng0l7y8qdxlm0u19q3wc7kc9g7oh8jpx5k7a9mjn7q'

def get_password():
    with open('password.txt') as f:
        return f.read()

token = ['5866215386:AAEjxZ1ZhRFMhXXFv8AZGTZI51OMv9Ig6_c', '6029807202:AAEJQwj1GEnDZ-rVjhhh_pyFQPrTuZtIx9Q']
# the first one is for sending messages to groups with interval
# the second one is for processing orders and sending result to clients