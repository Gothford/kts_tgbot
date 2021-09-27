import asyncio
import logging
from store.accessor import Accessor
from apps.user.models import User
from datetime import datetime


class Scheduler(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def get_timers(self):
        while True:
            current_time = str(datetime.now().time())[:5]
            try:
                users = await User.query.where(User.timer == current_time).gino.all()
            except Exception as e:
                logging.error(f'FROM SHEDULER: {e}')

            if len(users) > 0:
                await self.news_for_users(users)

            await asyncio.sleep(60)

    async def news_for_users(self, users):
        for user in users:
            await self.store.habr.get_news(user.chat_id, user.tags)




    async def _on_connect(self, _):
        self._task = asyncio.create_task(self.get_timers())


    async def _on_disconnect(self, _) -> None:
        pass