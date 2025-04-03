import json
from config import config

class ProductService:
    """
    Service to handle product data operations
    """
    
    def __init__(self):
        """
        Initialize the product service with data path from config
        """
        self.data_path = config['DATA_PATH']
        self.products = self._load_products()
    
    def _load_products(self):
        """
        Load products from the JSON data file
        """
        try:
            with open(self.data_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading product data: {str(e)}")
            return []
    
    def _save_products(self):
        """
        Save products back to the JSON data file
        """
        try:
            with open(self.data_path, 'w') as file:
                json.dump(self.products, file, indent=2)
        except Exception as e:
            print(f"Error saving product data: {str(e)}")
    
    def get_all_products(self):
        """
        Return all products
        """
        return self.products
    
    def get_product_by_id(self, product_id):
        """
        Get a specific product by ID
        """
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def update_product(self, product_id, updated_data):
        """
        Update a product with new data
        """
        for i, product in enumerate(self.products):
            if product['id'] == product_id:
                # Merge the updated data with the existing product
                self.products[i] = {**product, **updated_data}
                self._save_products()
                return self.products[i]
        return None
    
    def add_product(self, product_data):
        """
        Add a new product
        """
        # Generate a new product ID if not provided
        if 'id' not in product_data:
            max_id = 0
            for product in self.products:
                try:
                    prod_id = int(product['id'].replace('prod', ''))
                    max_id = max(max_id, prod_id)
                except:
                    pass
            product_data['id'] = f"prod{max_id + 1:03d}"
        
        self.products.append(product_data)
        self._save_products()
        return product_data
    
    def delete_product(self, product_id):
        """
        Delete a product by ID
        """
        for i, product in enumerate(self.products):
            if product['id'] == product_id:
                deleted_product = self.products.pop(i)
                self._save_products()
                return deleted_product
        return None
    
    def get_products_by_category(self, category):
        """
        Get products filtered by category
        """
        return [p for p in self.products if p.get('category') == category]
    
    def get_products_by_brand(self, brand):
        """
        Get products filtered by brand
        """
        return [p for p in self.products if p.get('brand') == brand]
    
    def get_products_by_price_range(self, min_price, max_price):
        """
        Get products filtered by price range
        """
        if max_price:
            return [p for p in self.products if min_price <= p.get('price', 0) <= max_price]
        else:
            return [p for p in self.products if p.get('price', 0) >= min_price]