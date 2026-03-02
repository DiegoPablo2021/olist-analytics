from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(255), primary_key=True)
    customer_unique_id = Column(String(255))
    customer_zip_code_prefix = Column(Integer)
    customer_city = Column(String(255))
    customer_state = Column(String(2))

class Geolocation(Base):
    __tablename__ = 'geolocation'
    id = Column(Integer, primary_key=True, autoincrement=True) # Precisamos de uma PK sintética pois os dados não possuem
    geolocation_zip_code_prefix = Column(Integer)
    geolocation_lat = Column(String(255))
    geolocation_lng = Column(String(255))
    geolocation_city = Column(String(255))
    geolocation_state = Column(String(2))

class OrderItem(Base):
    __tablename__ = 'order_items'
    order_id = Column(String(255), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String(255))
    seller_id = Column(String(255))
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)

class OrderPayment(Base):
    __tablename__ = 'order_payments'
    order_id = Column(String(255), primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String(50))
    payment_installments = Column(Integer)
    payment_value = Column(Float)

class OrderReview(Base):
    __tablename__ = 'order_reviews'
    review_id = Column(String(255), primary_key=True)
    order_id = Column(String(255), primary_key=True)
    review_score = Column(Integer)
    review_comment_title = Column(Text)
    review_comment_message = Column(Text)
    review_creation_date = Column(DateTime)
    review_answer_timestamp = Column(DateTime)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String(255), primary_key=True)
    customer_id = Column(String(255))
    order_status = Column(String(50))
    order_purchase_timestamp = Column(DateTime)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(DateTime)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(String(255), primary_key=True)
    product_category_name = Column(String(255))
    product_name_lenght = Column(Integer)
    product_description_lenght = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Integer)
    product_length_cm = Column(Integer)
    product_height_cm = Column(Integer)
    product_width_cm = Column(Integer)

class Seller(Base):
    __tablename__ = 'sellers'
    seller_id = Column(String(255), primary_key=True)
    seller_zip_code_prefix = Column(Integer)
    seller_city = Column(String(255))
    seller_state = Column(String(2))

class ProductCategoryNameTranslation(Base):
    __tablename__ = 'product_category_name_translation'
    product_category_name = Column(String(255), primary_key=True)
    product_category_name_english = Column(String(255))
