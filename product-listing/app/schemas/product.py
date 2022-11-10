from pydantic import BaseModel
from enum import Enum


class ProductCategory(str, Enum):
    component = "COMPONENT"
    damage_product = "DAMAGEPRODUCT"
    refurbishedproduct = "REFURBISHEDPRODUCT"

class DeviceCategory(str, Enum):
    laptop = "LAPTOP"
    smartphone = "SMARTPHONE"
    desktop = "DESkTOP"
    homeapplicance = "HOMEAPPLICANCE"


class ComponentCategory(str, Enum):
    cpu = "CPU"
    gpu = "GPU"
    matherboard = "MOTHERBOARD"
    ram = "RAM"
    hdd = "HDD"
    ssd = "SSD"
    power_unit = "POWERUNIT"
    screen = "SCREEN"


class ProductCreate(BaseModel):
    name: str
    brand: str


class DamageProductCreate(ProductCreate):
    category: DeviceCategory
    issue: str


class RefurbishedProductCreate(ProductCreate):
    category: DeviceCategory


class ComponentCreate(ProductCreate):
    category: ComponentCategory
