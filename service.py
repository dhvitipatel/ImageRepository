from model import Schema


class InventoryService:
    def get_products(self):
        result = Schema().get_inventory()
        products = []
        for product in result:
            products.append({
                "id": product[0],
                "name":  product[1],
                "src":   "/static/%s" % (product[2]),
                "price": "$%.2f" % (product[3]/100.0),
                "stock": "%d left" % (product[4]),
            })
        return products

    def get_profit(self):
        result = Schema().get_transactions()
        earnings = result/100.0 if result else 0
        return earnings

    def initialize(self):
        Schema().initialize_db()
    
    def purchase(self, product_id):
        return Schema().do_purchase(product_id)

    def add_peice(self, name: str, img: str, price: int, stock: int):
        return Schema().add_to_inventory(name, img, price, stock)
    
    def get_info(self, product_id):
        product = Schema().get_product_info(product_id)
        if product != 'Invalid product ID!' and product != "Insufficient stock!":
            info = [{
                "id": product[0],
                "name":  product[1],
                "src":   product[2][7:],
                "price": "$%.2f" % (product[3]/100.0),
            }]
            return info
        else:
            return product





