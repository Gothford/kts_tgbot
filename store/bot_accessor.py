import logging

from store.accessor import Accessor
from apps.user.models import User
from datetime import datetime


class Result:
    pass

class TgResp:
    ok: str
    result: Result


class BotAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def handle_message(self, item):
        print(item)
        msg = item['message']
        message_id = msg['message_id']
        chat_id = msg['chat']['id']
        username = msg['from']['username']
        message_data = msg['text']

        try:
            user = await self.get_user(chat_id)
        except Exception as e:
            logging.error(f'from get_user: {e}')


        if not user:
            await self.add_user(chat_id, username)
        else:
            await self.check_user_state(user, message_data)

    async def get_user(self, chat_id):
        return await User.query.where(User.chat_id == chat_id).gino.first()


    async def add_user(self, chat_id, username):
        await self.store.tg.send_message(chat_id,
                                         f'Привет, {username}!\nЯ - новостной бот!\n')
        user = await User.create(chat_id=chat_id, username=username, state="await_tags")
        return await self.update_tags(user)


    async def set_user_tags(self, user, message_data):
        await user.update(tags=message_data).apply()
        await self.store.tg.send_message(user.chat_id,
                                         f'Отлично, теперь вы подписаны на: {user.tags}')

        if user.state == 'await_tags':
            await user.update(state='await_timer').apply()
            await self.update_timer(user)
        else:
            await user.update(state='registered').apply()


    async def set_user_timer(self, user, message_data):
        try:
            timer = datetime.strptime(message_data, '%H:%M').time()
        except ValueError:
            return await self.store.tg.send_message(user.chat_id,
                                                    'Неправильный формат времени. Введите час и минуты в формате ЧЧ:ММ. Пример: 18:00')

        await user.update(timer=message_data, state='registered').apply()
        await self.store.tg.send_message(user.chat_id,
                                         f'Отлично, теперь вы будете получать новости по тегам: {user.tags}\nкаждый день в {user.timer}')

    async def check_user_state(self, user, message_data):
        if user.state in ['await_tags', 'change_tags']:
            await self.set_user_tags(user, message_data)
        elif user.state in ['await_timers', 'change_timer']:
            await self.set_user_timer(user, message_data)
        elif user.state == 'registered':
            await self.parse_command(user, message_data)

    # async def parse_message(self, user, message_data):
    #     if not message_data.startswith('/'):
    #         await self.store.tg.send_message(user.chat_id, "Неизвестная команда! Воспользуйтесь /help")
    #     else:
    #         await self.parse_command(user, message_data)

    async def parse_command(self, user, message_data):

        command_list = {
            '/help': self.send_help,
            '/get_my_tags': self.get_user_tags,
            '/get_my_timer': self.get_user_timer,
            '/set_new_tags': self.update_tags,
            '/set_new_timer': self.update_timer
        }
        try:
            await command_list[message_data](user)
        except KeyError:
            await self.store.tg.send_message(user.chat_id, "Неизвестная команда! Воспользуйтесь /help")

    async def send_help(self, user):
        await self.store.tg.send_message(user.chat_id, "/help\n/get_my_tags\n/get_my_timer\n/set_new_tags\n/set_new_timer")

    async def get_user_tags(self, user):
        await self.store.tg.send_message(user.chat_id, f'Вы подписаны на: {user.tags}')

    async def get_user_timer(self, user):
        await self.store.tg.send_message(user.chat_id, f'Время получения новостей: {user.timer}')

    async def update_tags(self, user):
        if user.state == 'registered':
            await user.update(state='change_tags').apply()
        else:
            await user.update(state='await_tags').apply()
        await self.store.tg.send_message(user.chat_id, 'Введите, интересующие вас теги, через запятую: ')

    async def update_timer(self, user):
        await user.update(state='await_timers').apply()
        await self.store.tg.send_message(user.chat_id,
                                         f'Введите время, в которое вы бы хотели получать новости, в формате ЧЧ:ММ ')
