


class Basket():
    """
    Bazinė krepšelio klasė, teikianti kai kuriuos numatytuosius veiksmus
    prireikus gali būti paveldimas arba nepaisomas.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product):
        """
        Naudotojų krepšelio seanso duomenų įtraukimas ir atnaujinimas
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': int(product.price)}

        self.session.modified = True
