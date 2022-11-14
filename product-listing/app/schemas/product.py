from pydantic import BaseModel
from typing import Optional, Union
from enum import Enum


class ProductCategory(str, Enum):
    COMPONENT = "COMPONENT"
    DAMAGED_PRODUCT = "DAMAGED_PRODUCT"
    REFURBISHED_PRODUCT = "REFURBISHED_PRODUCT"


class DeviceCategory(str, Enum):
    LAPTOP = "LAPTOP"
    SMARTPHONE = "SMARTPHONE"
    DESKTOP = "DESKTOP"
    HOME_APPLIANCE = "HOME_APPLIANCE"


class ComponentCategory(str, Enum):
    CPU = "CPU"
    GPU = "GPU"
    MOTHERBOARD = "MOTHERBOARD"
    RAM = "RAM"
    HDD = "HDD"
    SSD = "SSD"
    POWER_UNIT = "POWER_UNIT"
    SCREEN = "SCREEN"


class ProductCreate(BaseModel):
    name: str
    brand: str
    category: ProductCategory


class ComponentCreate(ProductCreate):
    sub_category: ComponentCategory


class DamagedProductCreate(ProductCreate):
    sub_category: DeviceCategory
    issue: str


class RefurbishedProductCreate(ProductCreate):
    sub_category: DeviceCategory


class ProductOut(BaseModel):
    name: str
    brand: str
    category: ProductCategory
    sub_category: Union[DeviceCategory, ComponentCategory]
    issue: Optional[str]
