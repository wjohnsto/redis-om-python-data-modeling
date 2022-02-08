import asyncio
from typing import List
from aredis_om import Field, JsonModel
from aredis_om.model import Migrator

from utils import Base


class ProductDetail(Base("product_details"), JsonModel):
    product_id: str = Field(index=True)
    description: str
    manufacturer: str
    dimensions: str
    weight: str
    images: List[str]


class Product(Base("products"), JsonModel):
    name: str = Field(index=True)
    image: str = Field(index=True)
    price: int = Field(index=True)


async def add_product():
    product = {
        "name": "Earbuds",
        "image": "https://www.example.com/image.jpg",
        "price": 1999,
    }
    details = {
        "description": "Ultra lightweight bluetooth 5.0 in-ear headphones with a batter that lasts 8 hours with normal use",
        "manufacturer": "Senheiser",
        "dimensions": "3 x 3 x 1.5 inches",
        "weight": "0.13 ounces",
        "images": ["https://www.example.com/image1.jpg", "https://www.example.com/image2.jpg"]
    }
    db_product = await Product(**product).save()
    details["product_id"] = db_product.pk
    await ProductDetail(**details).save()

    return db_product


async def get_product_list():
    return await Product.find().all()


async def get_product_details(product_id: str):
    return {
        "product": await Product.get(product_id),
        "details": await ProductDetail.find(
            ProductDetail.product_id == product_id
        ).first()
    }


async def main():
    await Migrator().run()
    product = await add_product()
    results = await get_product_list()
    print(results)
    results = await get_product_details(product.pk)
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
