"""
Item management business logic module
Example module following FastAPI official documentation patterns
"""

from utils.logger import get_logger
from schemas.items import ItemCreate, ItemResponse
from typing import List, Optional

logger = get_logger("fastapi_app.modules.items")


class ItemService:
    """Service class for item operations"""
    
    def __init__(self):
        self._items: List[dict] = []
        self._next_id = 1
    
    def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """
        Create a new item
        
        Args:
            item_data: Item creation data
            
        Returns:
            ItemResponse: Created item data
        """
        logger.info(f"Creating new item: {item_data.name}")
        
        item = {
            "id": self._next_id,
            "name": item_data.name,
            "description": item_data.description
        }
        self._items.append(item)
        self._next_id += 1
        
        logger.info(f"Item created with ID: {item['id']}")
        return ItemResponse(**item)
    
    def get_items(self) -> List[ItemResponse]:
        """Get all items"""
        logger.info(f"Retrieving {len(self._items)} items")
        return [ItemResponse(**item) for item in self._items]
