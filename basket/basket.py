from decimal import Decimal

from shop.models import Product


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
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __iter__(self):        
        """
        Surenkame produkto_id seanse, kad pateiktume duomenų bazės užklausą
         ir grąžintume prekes
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
         Gauti krepšelio duomenis ir suskaičiuoti prekių kiekį
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        """
        Pridėti daugiau prekių krepšelyje
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def delete(self, product):
        """
        Ištrinti iš krepšelio prekes 
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    def save(self):
        self.session.modified = True
