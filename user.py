class User:
    def __init__(self):
        self.id = None
        self.ratings = {}
        self.rating_mean = None
        self.rating_std_dev = None
        self.rating_min = None
        self.rating_max = None
        self.neighbors = []
