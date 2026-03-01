from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("heritage-db")

HERITAGE_DB: dict[str, dict[str, Any]] = {
    "hampi": {
        "destination": "Hampi",
        "state": "Karnataka",
        "country": "India",
        "spots": [
            {
                "id": "virupaksha_temple",
                "name": "Virupaksha Temple",
                "category": "Temple Complex",
                "best_time": "06:15-08:00 and 16:45-18:15",
                "golden_hour": "Sunrise and pre-sunset",
                "indoor_option": True,
                "description": "A living temple with towering gopuram and lively pilgrim activity ideal for layered heritage street frames.",
                "photo_tips": [
                    "Frame the gopuram from Hampi Bazaar axis",
                    "Use 35mm-50mm for people + architecture compositions",
                ],
                "coordinates": {"lat": 15.3350, "lng": 76.4600},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1715031956632-3af8f6e6f4cb",
                    "https://images.unsplash.com/photo-1687454470701-5fddfcbf5069",
                    "https://images.unsplash.com/photo-1708158010557-f0abf34b7d5f",
                ],
            },
            {
                "id": "vittala_temple",
                "name": "Vittala Temple and Stone Chariot",
                "category": "Temple Complex",
                "best_time": "06:30-09:00",
                "golden_hour": "Early morning",
                "indoor_option": False,
                "description": "Iconic stone chariot, musical pillars, and long colonnades that reward wide-angle symmetry and telephoto details.",
                "photo_tips": [
                    "Reach at opening time for clean foregrounds",
                    "Shoot low-angle wide compositions for chariot scale",
                ],
                "coordinates": {"lat": 15.3357, "lng": 76.4748},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1662056257240-f7955daebc01",
                    "https://images.unsplash.com/photo-1688471863593-3bf3dc73f7e5",
                    "https://images.unsplash.com/photo-1679943661145-6ef6f75e2647",
                ],
            },
            {
                "id": "hemakuta_hill",
                "name": "Hemakuta Hill Temples",
                "category": "Hilltop Ruins",
                "best_time": "06:00-08:00",
                "golden_hour": "Sunrise",
                "indoor_option": False,
                "description": "Cluster of shrines over granite outcrops with panoramic views, ideal for sunrise silhouettes and atmospheric layers.",
                "photo_tips": [
                    "Carry a lightweight tripod for sunrise bracketing",
                    "Use telephoto compression toward Virupaksha side",
                ],
                "coordinates": {"lat": 15.3337, "lng": 76.4579},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1711874584634-5b47e4b57b89",
                    "https://images.unsplash.com/photo-1704385402912-9408659150bc",
                ],
            },
            {
                "id": "achyutaraya_temple",
                "name": "Achyutaraya Temple",
                "category": "Temple Ruins",
                "best_time": "07:00-09:30 and 16:00-17:45",
                "golden_hour": "Late afternoon",
                "indoor_option": False,
                "description": "A quieter complex with dramatic mandapa geometry, perfect for texture-focused frames without large crowds.",
                "photo_tips": [
                    "Walk the old market street for leading lines",
                    "Use side-light for stone texture and relief",
                ],
                "coordinates": {"lat": 15.3323, "lng": 76.4702},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1691908570860-7cd31f5e69ab",
                    "https://images.unsplash.com/photo-1702501925883-0d5f90d95a79",
                ],
            },
            {
                "id": "queen_bath",
                "name": "Queen's Bath",
                "category": "Royal Enclosure",
                "best_time": "10:00-12:00",
                "golden_hour": "N/A",
                "indoor_option": True,
                "description": "A partially enclosed Indo-Islamic pavilion that works as a midday fallback for shade and reflected light.",
                "photo_tips": [
                    "Use central symmetry from the main arch",
                    "Try black-and-white for high-contrast geometry",
                ],
                "coordinates": {"lat": 15.3228, "lng": 76.4708},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1684050862753-fd8b66b89453",
                ],
            },
            {
                "id": "lotus_mahal",
                "name": "Lotus Mahal",
                "category": "Zenana Enclosure",
                "best_time": "08:30-10:30 and 15:30-17:00",
                "golden_hour": "Late afternoon",
                "indoor_option": True,
                "description": "Elegant multi-arched pavilion with softer lines than most Hampi ruins, good for architectural detail studies.",
                "photo_tips": [
                    "Use a 70-200mm lens for arch patterns",
                    "Shoot from diagonal corners for depth",
                ],
                "coordinates": {"lat": 15.3291, "lng": 76.4675},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1676281949414-dd7d8d4d61ea",
                    "https://images.unsplash.com/photo-1699186904531-1a4bf8f2a6cb",
                ],
            },
            {
                "id": "elephant_stables",
                "name": "Elephant Stables",
                "category": "Zenana Enclosure",
                "best_time": "08:30-10:30 and 16:00-17:30",
                "golden_hour": "Late afternoon",
                "indoor_option": True,
                "description": "Rhythmic domes and repeating arches provide strong pattern compositions and dramatic perspective shots.",
                "photo_tips": [
                    "Use centered composition to emphasize rhythm",
                    "Shoot with people for scale reference",
                ],
                "coordinates": {"lat": 15.3298, "lng": 76.4683},
                "sample_photos": [
                    "https://images.unsplash.com/photo-1704706930415-c4f5f89dbf63",
                ],
            },
        ],
    }
}


@mcp.tool()
def list_supported_destinations() -> list[dict[str, str]]:
    """List destinations currently available in the heritage DB."""
    return [
        {
            "slug": slug,
            "destination": payload["destination"],
            "state": payload["state"],
            "country": payload["country"],
        }
        for slug, payload in HERITAGE_DB.items()
    ]


@mcp.tool()
def search_heritage_spots(destination: str, limit: int = 8) -> dict[str, Any]:
    """Return must-visit heritage spots with photography metadata for a destination."""
    slug = destination.strip().lower()
    if slug not in HERITAGE_DB:
        return {
            "destination": destination,
            "status": "not_found",
            "message": "Destination not available in local DB yet. Use list_supported_destinations() first.",
            "spots": [],
        }

    destination_data = HERITAGE_DB[slug]
    spots = destination_data["spots"][: max(1, min(limit, 12))]
    return {
        "destination": destination_data["destination"],
        "status": "ok",
        "total_spots": len(destination_data["spots"]),
        "spots": spots,
    }


@mcp.tool()
def get_spot_by_id(destination: str, spot_id: str) -> dict[str, Any]:
    """Get full details for a single heritage spot by id."""
    slug = destination.strip().lower()
    if slug not in HERITAGE_DB:
        return {"status": "not_found", "message": "Unknown destination."}

    for spot in HERITAGE_DB[slug]["spots"]:
        if spot["id"] == spot_id:
            return {"status": "ok", "spot": spot}

    return {
        "status": "not_found",
        "message": f"Spot id '{spot_id}' not found for {HERITAGE_DB[slug]['destination']}",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
