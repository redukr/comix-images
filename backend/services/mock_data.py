"""
Тестові дані для перевірки backend без JOJ файлів
"""

RANKS_MOCK = [
    {
        "id": "recruit",
        "name": "Рекрут",
        "flavor": "Знає різницю між наказом і порадою.",
        "requirement": {},
        "cost": {},
        "bonus": {}
    },
    {
        "id": "soldier",
        "name": "Солдат",
        "flavor": "Навчився не лише слухати, а й виконувати.",
        "requirement": {"reputation": 3, "discipline": 2},
        "cost": {"time": 1},
        "bonus": {"discipline": 1}
    },
    {
        "id": "junior_sergeant",
        "name": "Молодший сержант",
        "flavor": "Перше 'так точно' з нотками відповідальності.",
        "requirement": {"reputation": 5, "discipline": 3, "documents": 1},
        "cost": {"time": 2},
        "bonus": {"discipline": 1, "tech": 1}
    },
    {
        "id": "general",
        "name": "Генерал",
        "flavor": "Вершина кар'єрного шляху.",
        "requirement": {"reputation": 20, "discipline": 15, "documents": 5},
        "cost": {"time": 5, "documents": 3},
        "bonus": {"reputation": 5, "tech": 3}
    }
]

CARDS_MOCK = {
    "version": 1,
    "catalog": [
        {
            "id": "test-01",
            "title": "Перше завдання",
            "category": "COMMAND",
            "image": "/cards/test1.webp",
            "flavor": "Початок великого шляху.",
            "effects": [{"resource": "discipline", "value": 1}]
        },
        {
            "id": "test-02",
            "title": "Навчання на полігоні",
            "category": "VVNZ",
            "image": "/cards/test2.webp",
            "flavor": "Піл і працюй.",
            "effects": [{"resource": "reputation", "value": 2}],
            "grantRank": "junior_lieutenant"
        }
    ]
}
