import asyncio
from typing import List
from aredis_om import Field, JsonModel
from aredis_om.model import Migrator

from utils import Base


class Store(Base("stores"), JsonModel):
    name: str
    phone: str
    zip: str


class Product(Base("products"), JsonModel):
    name: str = Field(index=True)
    image: str = Field(index=True)
    price: int = Field(index=True)


class Inventory(Base("inventories"), JsonModel):
    product_id: str = Field(index=True)
    store_id: str = Field(index=True)
    quantity: int = Field(index=True)
    store: Store


async def add_product():
    product = {
        "name": "Earbuds",
        "image": "https://www.example.com/image.jpg",
        "price": 1999,
    }

    return await Product(**product).save()


async def add_stores():
    store1 = await Store(**{
        "name": "Best Buy Humbolt",
        "phone": "123-555-7890",
        "zip": "90210"
    }).save()
    store2 = await Store(**{
        "name": "Best Buy Fremont",
        "phone": "123-555-7890",
        "zip": "97261"
    }).save()

    return store1, store2


# async def add_inventory(product: Product, stores: List[Store]):
#     await Inventory(**{
#         "product_id": product.pk,
#         "store_id": stores[0].pk,
#         "quantity": 100
#     }).save()

#     await Inventory(**{
#         "product_id": product.pk,
#         "store_id": stores[1].pk,
#         "quantity": 0
#     }).save()


# async def get_in_stock(product_id: str):
#     inventory = await Inventory.find(
#         (Inventory.product_id == product_id) &
#         (Inventory.quantity > 0)
#     ).all()

#     return await Store.find(Store.pk << [i.store_id for i in inventory]).all()



async def add_inventory(product: Product, stores: List[Store]):
    await Inventory(**{
        "product_id": product.pk,
        "store_id": stores[0].pk,
        "quantity": 100,
        "store": stores[0]
    }).save()

    await Inventory(**{
        "product_id": product.pk,
        "store_id": stores[1].pk,
        "quantity": 0,
        "store": stores[1]
    }).save()

async def get_in_stock(product_id: str):
    return await Inventory.find(
        (Inventory.product_id == product_id) &
        (Inventory.quantity > 0)
    ).all()


async def main():
    await Migrator().run()
    product = await add_product()
    store1, store2 = await add_stores()
    await add_inventory(product, [store1, store2])

    results = await get_in_stock(product.pk)

    print(results)

if __name__ == '__main__':
    asyncio.run(main())
