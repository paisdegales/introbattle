class FighterAttributes:
    def __init__(self, **kwargs):
        self = dict()
        for k,v in kwargs.items():
            self[k] = v
