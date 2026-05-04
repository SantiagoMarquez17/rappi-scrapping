from __future__ import annotations

import random
from datetime import datetime, timezone

from src.config import PLATFORMS, REFERENCE_PRODUCTS
from src.locations import ADDRESSES


PLATFORM_PROFILE = {
    "Rappi": {"price": 1.00, "delivery_fee": 1.08, "service_fee": 0.08, "eta": 1.00, "promo": 0.10},
    "Uber Eats": {"price": 1.02, "delivery_fee": 0.94, "service_fee": 0.10, "eta": 0.96, "promo": 0.16},
    "DiDi Food": {"price": 0.97, "delivery_fee": 0.86, "service_fee": 0.06, "eta": 1.08, "promo": 0.22},
}

# Baseline prices and platform profiles make the sample dataset deterministic
# while preserving realistic differences in price, fees, ETA and promotions.
PRODUCT_BASE_PRICE = {
    "Big Mac": 89,
    "Combo mediano": 145,
    "Nuggets 10 piezas": 109,
    "Coca-Cola 500ml": 32,
    "Agua 1L": 28,
}

ZONE_MULTIPLIER = {
    "premium": 1.12,
    "corporativa": 1.08,
    "alta demanda": 1.03,
    "residencial": 1.00,
    "universitaria": 0.96,
    "turistica": 1.05,
    "periferica": 0.93,
}


def build_sample_rows(seed: int = 42) -> list[dict]:
    """Create a reproducible dataset with the same schema as live collectors."""
    random.seed(seed)
    rows = []
    scraped_at = datetime.now(timezone.utc).isoformat()

    for address in ADDRESSES:
        zone_factor = ZONE_MULTIPLIER[address["zone_type"]]
        for platform in PLATFORMS:
            profile = PLATFORM_PROFILE[platform]
            availability_penalty = 0.08 if address["zone_type"] == "periferica" and platform == "Rappi" else 0
            for product in REFERENCE_PRODUCTS:
                available = random.random() > (0.06 + availability_penalty)
                base_price = PRODUCT_BASE_PRICE[product]
                product_price = round(base_price * zone_factor * profile["price"] * random.uniform(0.96, 1.06), 2)
                delivery_fee = round(random.uniform(18, 48) * profile["delivery_fee"] * zone_factor, 2)
                service_fee = round(product_price * profile["service_fee"], 2)
                discount = round(product_price * profile["promo"] * random.choice([0, 0.5, 1]), 2)
                eta_min = int(random.uniform(18, 42) * profile["eta"] * (1.1 if address["zone_type"] == "periferica" else 1))
                eta_max = eta_min + random.choice([8, 10, 12, 15])
                final_total = round(product_price + delivery_fee + service_fee - discount, 2)

                # Unavailable items are kept as rows with null commercial values;
                # availability itself is a competitive signal.
                rows.append(
                    {
                        "scraped_at": scraped_at,
                        "platform": platform,
                        "city": address["city"],
                        "zone": address["zone"],
                        "zone_type": address["zone_type"],
                        "address_id": address["address_id"],
                        "address": address["address"],
                        "product": product,
                        "restaurant": "McDonald's" if product in ["Big Mac", "Combo mediano", "Nuggets 10 piezas"] else "Retail benchmark",
                        "available": available,
                        "product_price_mxn": product_price if available else None,
                        "delivery_fee_mxn": delivery_fee if available else None,
                        "service_fee_mxn": service_fee if available else None,
                        "discount_mxn": discount if available else None,
                        "eta_min_minutes": eta_min if available else None,
                        "eta_max_minutes": eta_max if available else None,
                        "final_total_mxn": final_total if available else None,
                        "evidence_url": "",
                        "notes": "reproducible_seed_dataset",
                    }
                )

    return rows
