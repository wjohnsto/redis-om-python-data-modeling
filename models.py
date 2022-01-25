import datetime
from typing import List
from aredis_om import Field, JsonModel, EmbeddedJsonModel


def make_key(cls, part: str):
    model_prefix = getattr(cls._meta, "model_key_prefix", "").strip(":")
    return f"{model_prefix}:{part}"


counts = {
    "addresses": 0,
    "inventories": 0,
    "stores": 0,
    "product_details": 0,
    "products": 0,
    "reviews": 0,
}

def creator(key: str):
    class PrimaryKeyCreator:
        def create_pk(self, *args, **kwargs) -> str:
            """Create a new primary key"""
            global counts
            counts[key] += 1
            return str(counts[key])

    return PrimaryKeyCreator


class Address(EmbeddedJsonModel):
    street: str
    city: str
    zip: str

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "addresses"
        primary_key_creator_cls = creator("addresses")


class Inventory(JsonModel):
    store_id: str = Field(index=True)
    product_id: str = Field(index=True)
    store_name: str
    store_contact: str
    store_address: Address
    quantity: int = Field(index=True)
    price: int

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "inventories"
        primary_key_creator_cls = creator("inventories")


class Store(JsonModel):
    name: str
    contact: str
    address: Address

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "stores"
        primary_key_creator_cls = creator("stores")


class ProductDetail(EmbeddedJsonModel):
    full_summary: str
    manufacturer: str
    package_dimensions: str
    images: List[str]

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "product_details"
        primary_key_creator_cls = creator("product_details")


class Product(JsonModel):
    name: str
    description: str
    image: str
    review_count: int
    rating_sum: int
    details: ProductDetail

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "products"
        primary_key_creator_cls = creator("products")


class Review(JsonModel):
    product_id: str = Field(index=True)
    reviewer: str
    rating: str = Field(index=True)
    comment: str
    published_date: datetime.date = Field(index=True)

    @classmethod
    def make_key(cls, part: str):
        return make_key(cls, part)

    class Meta:
        model_key_prefix = "reviews"
        primary_key_creator_cls = creator("reviews")
