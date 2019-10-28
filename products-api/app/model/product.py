class Product:

    def __init__(self,
                 name: str,
                 categories: [],
                 price: float,
                 url: str,
                 id: str = None,
                 user_id: str = None
                 ):
        self.id = id
        self.name = name
        self.categories = categories
        self.price = price
        self.url = url
        self.user_id = user_id


