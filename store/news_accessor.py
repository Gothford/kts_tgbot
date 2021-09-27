from store.accessor import Accessor


class NewsAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def pars_news(self, news):
        for new in news:
            pass
