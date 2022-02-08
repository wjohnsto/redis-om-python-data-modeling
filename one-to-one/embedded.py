import asyncio
from typing import List, Optional
from aredis_om import connections, Field, JsonModel, EmbeddedJsonModel
from aredis_om.model import Migrator

from utils import Base


class ProductDetail(Base("product_details"), EmbeddedJsonModel):
    description: str
    manufacturer: str
    dimensions: str
    weight: str
    images: List[str]


class Product(Base("products"), JsonModel):
    name: str = Field(index=True)
    image: str = Field(index=True)
    price: int = Field(index=True)
    details: Optional[ProductDetail]


async def add_product():
    product = {
        "name": "Earbuds",
        "image": "https://www.example.com/image.jpg",
        "price": 1999,
        "details": {
                "description": "Ultra lightweight bluetooth 5.0 in-ear headphones with a batter that lasts 8 hours with normal use",
                "manufacturer": "Senheiser",
                "dimensions": "3 x 3 x 1.5 inches",
                "weight": "0.13 ounces",
                "images": ["https://www.example.com/image1.jpg", "https://www.example.com/image2.jpg"]
        }
    }

    return await Product(**product).save()


async def get_product_list():
    results = await connections \
        .get_redis_connection() \
        .execute_command(
            f'FT.SEARCH {Product.Meta.index_name} * LIMIT 0 10 RETURN 3 name image price'
        )

    return Product.from_redis(results)


async def get_product_details(product_id: str):
    return await Product.get(product_id)


async def main():
    await Migrator().run()
    product = await add_product()
    results = await get_product_list()
    print(results)
    results = await get_product_details(product.pk)
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
