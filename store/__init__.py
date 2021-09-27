from aiohttp import web



class Store:
    def __init__(self, app: web.Application):
        from store.pg import PgAccessor
        from store.gino import GinoAccessor
        from store.bot_accessor import BotAccessor
        from store.tg_accessor import TgAccessor
        from store.habr_accessor import HabrAccessor
        from store.scheduler import Scheduler

        self.pg = PgAccessor(app)
        self.gino = GinoAccessor(app)
        self.tg = TgAccessor(app)
        self.bot = BotAccessor(app)
        self.habr = HabrAccessor(app)
        self.scheduler = Scheduler(app)

    def setup(self, ):
        self.pg.setup()
        self.tg.setup()
        self.gino.setup()
        self.scheduler.setup()
