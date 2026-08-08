import csv
import json
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List
 
logger = logging.getLogger(__name__)
 
class ProductSchema(BaseModel):
    name: str
    price: float = Field(gt=0)
    category: str
    description: str
    ingredients: List[str] = []
    suitable_for: List[str] = []
    in_stock: bool = True
 
def load_catalog_from_csv(path: str) -> List[ProductSchema]:
    """
    Load and validate a product catalog from a CSV file.
    Returns a list of validated Product objects.
    Logs and skips any rows that fail validation.
    """
    catalog_path = Path(path)
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found at {path}")
 
    products = []
    with open(catalog_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # Row 2 (1-indexed, header is 1)
            try:
                # CSV gives us strings; Pydantic coerces to correct types
                if "ingredients" in row:
                    row["ingredients"] = [
                        ing.strip() for ing in row["ingredients"].split(",")
                        if ing.strip()
                    ]
                if "suitable_for" in row:
                    row["suitable_for"] = [
                        s.strip() for s in row["suitable_for"].split(",")
                        if s.strip()
                    ]
                product = ProductSchema(**row)
                products.append(product)
            except Exception as e:
                logger.warning(f"Skipping row {i}: {e}")
 
    logger.info(f"Loaded {len(products)} valid products from {path}")
    return products
 
def catalog_to_context(products: List[ProductSchema]) -> str:
    """
    Convert the product list into a compact text format
    suitable for inclusion in an agent's context window.
    """
    lines = []
    for p in products:
        line = (
            f"[{p.name}] Price: R{p.price:.2f} | "
            f"Category: {p.category} | "
            f"Suitable for: {', '.join(p.suitable_for) or 'all skin types'} | "
            f"Ingredients: {', '.join(p.ingredients[:5]) or 'not listed'} | "
            f"In stock: {'Yes' if p.in_stock else 'No'}"
        )
        lines.append(line)
    return "\n".join(lines)
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Create a sample CSV for testing
    sample_csv = "sample_catalog.csv"
    with open(sample_csv, "w") as f:
        f.write("name,price,category,description,ingredients,suitable_for\n")
        f.write("Glow Serum,349,serums,Brightening vitamin C serum,\"vitamin c,niacinamide,hyaluronic acid\",\"oily,combination\"\n")
        f.write("Hydra Toner,199,toners,Hydrating toner for dry skin,\"glycerin,centella asiatica\",\"dry,sensitive\"\n")
 
    catalog = load_catalog_from_csv(sample_csv)
    context = catalog_to_context(catalog)
    print(context)
