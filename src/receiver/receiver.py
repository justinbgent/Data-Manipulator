# Receive data and send a boolean value if it's been received
# Print out each piece of data that was received

received = False

def receive_data(deal: str) -> bool:
    global received
    received = not received
    if received:
        print(deal)
    return received