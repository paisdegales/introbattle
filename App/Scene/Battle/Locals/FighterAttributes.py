class FighterAttributes:
    def __init__(self, **kwargs):
        self = dict()
        for k,v in kwargs:
            self[k] = v
