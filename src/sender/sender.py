# Write a list of deals including duplicates and some with missing data and send these over to the middle man. 

DEALS_AS_JSON_STRINGS: list[str] = [
    # Duplicates
    '{"deal_id": "123", "deal_name": "Test Deal", "amount": 5000, "pipeline": "Install Pipeline"}',
    '{"deal_id": "123", "deal_name": "Test Deal", "amount": 5000, "pipeline": "Install Pipeline"}',
    '{"deal_id": "124", "deal_name": "Other Deal", "amount": 12000, "pipeline": "Install Pipeline"}',
    '{"deal_id": "124", "deal_name": "Other Deal", "amount": 12000, "pipeline": "Install Pipeline"}',
    # Missing deal_id
    '{"deal_name": "Other Deal", "amount": 12000, "pipeline": "Install Pipeline"}',
    # Missing deal_name
    '{"deal_id": "125", "amount": 15000, "pipeline": "Install Pipeline"}',
    '{"deal_id": "126", "deal_name": "Fourth Deal", "amount": 18000, "pipeline": "Install Pipeline"}',
    # Other pipeline
    '{"deal_id": "127", "deal_name": "Fifth Deal", "amount": 0, "pipeline": "Wrong Pipeline"}',
    '{"deal_id": "128", "deal_name": "Sixth Deal", "amount": 24000, "pipeline": "Install Pipeline"}',
    '{"deal_id": "129", "deal_name": "Seventh Deal", "amount": 27000, "pipeline": "Install Pipeline"}',
    # Mising pipeline
    '{"deal_id": "130", "deal_name": "Eighth Deal", "amount": 30000}',
    '{"deal_id": "131", "deal_name": "Ninth Deal", "amount": 33000, "pipeline": "Install Pipeline"}',
    # Missing pipeline
    '{"deal_id": "132", "deal_name": "Tenth Deal", "amount": 36000, "pipeline": ""}',
]

from middle_man import middle_man

def send_data():
    for deal in DEALS_AS_JSON_STRINGS:
        middle_man.transform_data(deal)