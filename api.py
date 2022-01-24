from fastapi import APIRouter

from generate import clear_data, generate_data
from models import Store


router = APIRouter()


@router.get("/clear")
async def clear_sample_data():
    return await clear_data()


@router.get("/generate")
async def generate_sample_data():
    return await generate_data()


@router.get("/stores")
async def get_inventory():
    return await Store.find().all()


@router.get("/stores/with/{product_id}")
async def get_inventory(product_id: str):
    return await Store.find(
        (Store.inventory.product_id == product_id) &
        (Store.inventory.quantity != "0")
    ).all()
