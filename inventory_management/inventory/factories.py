from .models import Product

class ProductFactory:
    @staticmethod
    def create_product(name, description, stock, stock_alert_threshold, barcode):
        return Product.objects.create(
            name=name,
            description=description,
            stock=stock,
            stock_alert_threshold=stock_alert_threshold,
            barcode=barcode
        )
