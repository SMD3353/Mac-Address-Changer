from __future__ import annotations

from typing import Dict, List

RESTAURANT_DETAILS: Dict[str, str] = {
    "name": "Harmony Bites",
    "description": "A cozy neighborhood spot blending global comfort food with seasonal, locally sourced ingredients.",
    "address": "123 Market Street, Springfield",
    "phone": "(555) 123-4567",
    "hours": "Daily 11am – 10pm",
}

MENU: Dict[str, List[Dict[str, str]]] = {
    "Starters": [
        {
            "name": "Charred Shishito Peppers",
            "description": "Sea salt, yuzu aioli, toasted sesame",
            "price": 9,
        },
        {
            "name": "Heirloom Tomato Bruschetta",
            "description": "Whipped ricotta, basil oil, grilled sourdough",
            "price": 11,
        },
        {
            "name": "Miso Mushroom Soup",
            "description": "Shiitake broth, scallions, crispy garlic",
            "price": 8,
        },
    ],
    "Mains": [
        {
            "name": "Citrus Glazed Salmon Bowl",
            "description": "Forbidden rice, avocado, pickled daikon, ponzu glaze",
            "price": 21,
        },
        {
            "name": "Smoky Cauliflower Shawarma",
            "description": "Tahini yogurt, herb salad, harissa fries",
            "price": 18,
        },
        {
            "name": "Short Rib Pappardelle",
            "description": "Slow braised beef, roasted garlic cream, gremolata",
            "price": 24,
        },
    ],
    "Sides": [
        {
            "name": "Truffle Sweet Potato Mash",
            "description": "Brown butter crumble, chive oil",
            "price": 7,
        },
        {
            "name": "Charred Broccolini",
            "description": "Lemon zest, toasted almonds",
            "price": 6,
        },
        {
            "name": "Herbed Quinoa Pilaf",
            "description": "Preserved lemon, parsley, pine nuts",
            "price": 6,
        },
    ],
    "Desserts": [
        {
            "name": "Honeycomb Panna Cotta",
            "description": "Roasted figs, lavender caramel",
            "price": 9,
        },
        {
            "name": "Warm Chocolate Torte",
            "description": "Espresso ganache, mascarpone cream",
            "price": 10,
        },
    ],
    "Beverages": [
        {
            "name": "Ginger-Lemongrass Sparkler",
            "description": "House-made soda with lime",
            "price": 5,
        },
        {
            "name": "Cold Brew Tonic",
            "description": "Single-origin cold brew, tonic water, orange peel",
            "price": 5,
        },
        {
            "name": "Seasonal Kombucha",
            "description": "Ask about today's fermentation",
            "price": 6,
        },
    ],
    "Specials": [
        {
            "name": "Grilled Peach & Burrata Salad",
            "description": "Prosciutto crisp, mint, pistachio crumble",
            "price": 14,
        },
        {
            "name": "Seared Scallop Risotto",
            "description": "Sweet corn, lemon-thyme butter, micro basil",
            "price": 27,
        },
    ],
}


def format_menu_for_prompt(menu: Dict[str, List[Dict[str, str]]]) -> str:
    sections: List[str] = []
    for category, items in menu.items():
        item_lines = []
        for item in items:
            item_lines.append(
                f"- {item['name']} (${item['price']:.2f}): {item['description']}"
            )
        sections.append(f"{category}:\n" + "\n".join(item_lines))
    return "\n\n".join(sections)
