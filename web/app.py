from aiohttp import web
from store import Store



def setup_store(app: web.Application):
    store = Store(app)
    app["store"] = store
    store.setup()


def create_app():
    app = web.Application()
    setup_store(app)
    return app
