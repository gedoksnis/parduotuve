


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

    def add(self, product, qty):
        """
        Naudotojų krepšelio seanso duomenų įtraukimas ir atnaujinimas
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty':int(qty)}

        self.session.modified = True

    def __len__(self):
        """
        Gauti krepšelio duomenis ir suskaičiuoti prekių kiekį
        """
        return sum(item['qty'] for item in self.basket.values())