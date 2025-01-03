class ProductNotFoundError(Exception):
    def __init__(self, id: int):
        self.product_id = id
        self.message = f'Product with {id=} not found'
        super().__init__(self.message)
