import logging
from sqlalchemy import and_
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from apps.user.models import SendedNews
from store.accessor import Accessor


class HabrAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_news(self, chat_id, tags):
        # tag = 'geo'
        BASE_URL = 'https://habr.com'
        #POST_URL = 'https://habr.com/ru/news/t/'

        news = {}
        for tag in tags.split(','):
            tag = tag.strip()
            TAG_URL = f'{BASE_URL}/search/?q=%5B{tag}%5D&target_type=posts&order=date'
            #HUB_URL = f'{BASE_URL}/{tag}/'
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(TAG_URL) as resp:
                        data = await resp.text()
                        soup = BeautifulSoup(data, 'lxml')
                        for div in soup.find('div', {'class': 'tm-articles-list'}):
                            try:
                               date_key, link = div.time['datetime'], div.find_all('a', {'class': 'tm-article-snippet__title-link'})[0]['href']
                               news[date_key] = f'{BASE_URL}{link}'
                            except (TypeError, AttributeError):
                                continue

            except Exception as e:
                logging.error(f'FROM HABR REQUEST: {e}')
            await self.news_parser(chat_id, news, tag)


    async def news_parser(self, chat_id, news, tag):

        have_news = False
        for timer, link in news.items().__reversed__():
            chat_id = int(chat_id)
            try:
                is_old_post = await SendedNews.query.where(and_(SendedNews.chat_id == chat_id, SendedNews.link == link)).gino.first()
                if not is_old_post:
                    await self.store.tg.send_message(chat_id, f'{link}\n\ndate: {timer.split("T")[0]} {timer.split("T")[1][:8]}\ntag: {tag}')
                    await SendedNews.create(chat_id=chat_id, link=link, tag=tag)
                    have_news = True
            except Exception as e:
                logging.error(f'FROM SHEDULER SEND NEWS: {e}')

        if not have_news:
            await self.store.tg.send_message(chat_id, f'Новых новостей по теме {tag} нет :(')

