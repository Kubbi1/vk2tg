import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests

# CONFIGURATION FOR VK AND TG /Конфигурация для VK и TG
VK_TOKEN = 'YOU VK TOKEN'#CHANGE
VK_GROUP_ID = 'YOUR GROUP ID'#CHANGE
TELEGRAM_TOKEN = 'TELEGRAM TOKEN'#CHANGE
telegram_chat_id = 'TELEGRAM CHAT ID'#CHANGE

# Инициализация API ВКонтакте
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

# Имя отправителя
def get_sender_name(user_id):
    user_info = vk.users.get(user_ids=user_id)
    if user_info:
        return f"{user_info[0]['first_name']} {user_info[0]['last_name']}"
    return "Unknown"

# Отправка сообщения
def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        pass
    else:
        print('Ошибка отправки сообщения в Telegram')

# Основной цикл
for event in longpoll.listen():
     if event.type == VkBotEventType.MESSAGE_NEW:
        # Получаем текст сообщения и отправителя
        message = event.message.get('text')
        sender = get_sender_name(event.message.get('from_id'))
        fullmsg = str(f"VK ({sender}): {message}")
        send_telegram_message(TELEGRAM_TOKEN,telegram_chat_id,fullmsg)
