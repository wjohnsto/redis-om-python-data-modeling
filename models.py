from typing import List
from aredis_om import Field, JsonModel, EmbeddedJsonModel


class Address(EmbeddedJsonModel):
    street: str
    city: str = Field(index=True)
    zip: str = Field(index=True)

    class Meta:
        model_key_prefix = "addresses"


class Inventory(EmbeddedJsonModel):
    store_id: str = Field(index=True)
    product_id: str = Field(index=True)
    store_name: str = Field(index=True)
    product_name: str = Field(index=True)
    quantity: str = Field(index=True)

    class Meta:
        model_key_prefix = "inventories"


class Store(JsonModel):
    name: str = Field(index=True)
    address: Address
    inventory: List[Inventory]

    class Meta:
        model_key_prefix = "stores"


class Review(JsonModel):
    product_id: str = Field(index=True)
    user_id: str = Field(index=True)
    product_name: str = Field(index=True)
    user_name: str = Field(index=True)
    rating: str = Field(index=True)
    comment: str = Field(index=True)

    class Meta:
        model_key_prefix = "reviews"


class Product(JsonModel):
    sku: str = Field(index=True)
    name: str = Field(index=True)
    price: int = Field(index=True)
    description: str = Field(index=True, full_text_search=True)
    sold_at: List[Store]
    reviews: List[Review]

    class Meta:
        model_key_prefix = "products"


class Contact(EmbeddedJsonModel):
    phone: str = Field(index=True)
    email: str = Field(index=True)

    class Meta:
        model_key_prefix = "contacts"


class User(JsonModel):
    name: str = Field(index=True)
    contact_info: Contact

    class Meta:
        model_key_prefix = "users"
