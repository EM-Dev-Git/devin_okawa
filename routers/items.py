"""
Items router demonstrating modules and schemas integration
Following FastAPI official documentation patterns
"""

from fastapi import APIRouter, HTTPException
from typing import List
from utils.logger import get_router_logger
from schemas.items import ItemCreate, ItemResponse
from modules.items import ItemService

logger = get_router_logger("items")
router = APIRouter(prefix="/items", tags=["items"])
item_service = ItemService()


@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Create a new item"""
    try:
        logger.info(f"Creating item: {item.name}")
        result = item_service.create_item(item)
        logger.info(f"Item created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create item")


@router.get("/", response_model=List[ItemResponse])
async def get_items():
    """Get all items"""
    try:
        logger.info("Retrieving all items")
        items = item_service.get_items()
        logger.info(f"Retrieved {len(items)} items")
        return items
    except Exception as e:
        logger.error(f"Error retrieving items: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve items")
