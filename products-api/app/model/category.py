AVAILABLE_CATEGORIES = [
"eletrônicos",
"utensílios",
"cama e mesa",
"cozinha",
"higiene pessoal",
"abobrinha"
]


def is_available(category: str) -> bool:
    return category in AVAILABLE_CATEGORIES
