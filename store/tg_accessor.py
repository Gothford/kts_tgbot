import asyncio
import logging

import aiohttp

from store.accessor import Accessor


class Result:
    pass

class TgResp:
    ok: str
    result: Result


class TgAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_updates(self):
        offset = 1
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(
                        'https://api.telegram.org/bot1982304855:AAGIEvFvUdFwVU_GsZCY2RXBd5McRhIeb_U/'
                        'getUpdates',
                        params={'offset': offset}
                    ) as resp:

                        print(resp.status)
                        doc = await resp.json()
                        print(offset, doc)

                        for item in doc['result']:
                            offset = item['update_id'] + 1
                            await self.store.bot.handle_message(item)
                        if not doc['result']:
                            await asyncio.sleep(0.5)
                except Exception as e:
                    logging.error(f'FROM GET_UPDATES: {e}')

    async def send_message(self, chat_id, text):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.telegram.org/bot1982304855:AAGIEvFvUdFwVU_GsZCY2RXBd5McRhIeb_U/sendMessage',
                params={'chat_id': chat_id, 'text': text}
            ) as resp:
                pass

    # async def get_last_message_id(self):
    #     return await Message.query.where(Message.id.max()).gino.all()

    async def _on_connect(self, _):
        self._task = asyncio.create_task(self.get_updates())


    async def _on_disconnect(self, _) -> None:
        self._task.done()
