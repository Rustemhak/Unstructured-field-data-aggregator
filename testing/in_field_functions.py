def in_archangel_field(horizon_name: str) -> bool:
    archangel_fields = ["шешминский",
                        "тульский",
                        "бобриковский",
                        "кыновско-пашийский",
                        "каширский",
                        "верейский",
                        "башкирский",
                        "алексинский",
                        "турнейский"]
    return horizon_name in archangel_fields
