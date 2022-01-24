import random
from typing import List
from models import Address, Inventory, Store, Review, Product, Contact, User


async def generate_users():
    return [
        await User(
            name="John Doe",
            contact_info=Contact(
                phone="+1-555-555-5555",
                email="john@doe.com"
            )
        ).save(),

        await User(
            name="Jane Doe",
            contact_info=Contact(
                phone="+1-555-555-5555",
                email="jane@doe.com"
            )
        ).save(),

        await User(
            name="Jim Brown",
            contact_info=Contact(
                phone="+1-555-555-5555",
                email="jim@brown.com"
            )
        ).save(),
    ]


async def generate_stores():
    return [
        await Store(
            name="Townsville Superstore",
            address=Address(
                street="123 Main St",
                city="Townsville",
                zip="12345"
            ),
            inventory=[]
        ).save(),

        await Store(
            name="Anytown Big Store",
            address=Address(
                street="456 Main St",
                city="Anytown",
                zip="54321"
            ),
            inventory=[]
        ).save(),

        await Store(
            name="Everytown General Store",
            address=Address(
                street="789 Main St",
                city="Everytown",
                zip="13524"
            ),
            inventory=[]
        ).save(),
    ]


async def generate_products():
    return [
        await Product(
            sku="1234",
            name="4K TV",
            price=80000,
            description="A new 4K Smart TV",
            sold_at=[],
            reviews=[]
        ).save(),

        await Product(
            sku="5678",
            name="Macbook Pro",
            price=200000,
            description="A new Macbook Pro M1",
            sold_at=[],
            reviews=[]
        ).save(),

        await Product(
            sku="9012",
            name="Shampoo",
            price=500,
            description="A shampoo for curly hair",
            sold_at=[],
            reviews=[]
        ).save(),

        await Product(
            sku="3456",
            name="Lawnmower",
            price=40000,
            description="A self-propelled electric lawnmower with limited-time warranty",
            sold_at=[],
            reviews=[]
        ).save(),

        await Product(
            sku="7890",
            name="Queen Mattress",
            price=20000,
            description="A queen mattress with a soft, padded footrest",
            sold_at=[],
            reviews=[]
        ).save(),

        await Product(
            sku="1234",
            name="Smart Doorbell",
            price=80000,
            description="A smart doorbell with a camera that connects to your home network",
            sold_at=[],
            reviews=[]
        ).save(),
    ]


async def generate_reviews(products: List[Product], users: List[User]):
    new_products = []

    for product in products:
        for user in users:
            rating = random.randint(1, 5)
            product.reviews.append(
                Review(
                    product_id=product.pk,
                    user_id=user.pk,
                    product_name=product.name,
                    user_name=user.name,
                    rating=rating,
                    comment=f"This is a{' great' if rating > 3 else ' good' if rating > 2 else 'n okay' if rating > 1 else ' terrible'} {product.name}, {rating}/5 stars!"
                )
            )
        new_products.append(await product.save())

    return new_products


async def generate_sold_at(products: List[Product], stores: List[Store]):
    new_products = []

    for product in products:
        for store in stores:
            product.sold_at.append(store)
        new_products.append(await product.save())

    return new_products


async def generate_inventory(stores: List[Store], products: List[Product]):
    new_stores = []
    for store in stores:
        for product in products:
            store.inventory.append(Inventory(
                store_id=store.pk,
                product_id=product.pk,
                store_name=store.name,
                product_name=product.name,
                quantity=random.randint(0, 10)
            ))
        new_stores.append(await store.save())

    return new_stores


async def clear_data():
    stores = await Store.find().all()
    for store in stores:
        await store.delete()

    reviews = await Review.find().all()
    for review in reviews:
        await review.delete()

    inventories = await Inventory.find().all()
    for inventory in inventories:
        await inventory.delete()

    products = await Product.find().all()
    for product in products:
        await product.delete()

    users = await User.find().all()
    for user in users:
        await user.delete()


async def generate_data():
    await clear_data()
    stores = await generate_stores()
    products = await generate_products()
    users = await generate_users()

    products = await generate_reviews(products, users)
    products = await generate_sold_at(products, stores)
    stores = await generate_inventory(stores, products)
    return {
        "stores": stores,
        "products": products,
        "users": users
    }
