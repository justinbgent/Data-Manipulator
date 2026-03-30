# Transform the data 
# Be sure not to send duplicates if the deal_ids match
# Handle cases where the receiver fails to receive and try resending
import json
from receiver import receiver

# {
#   "customer_name": "Test Deal",
#   "invoice_total": 5000,
#   "deal_id": "123"
# }

deals: set[str] = set()
pending_sends: dict[str, str] = {}

def transform_data(deal: str):
    deal_data = json.loads(deal)

    # Only process if in the Install Pipeline
    pipeline = deal_data['pipeline']
    if pipeline != 'Install Pipeline':
        return

    # Only send if not a duplicate
    deal_id = deal_data['deal_id']
    if deal_id in deals:
        return
    deals.add(deal_id)

    deal_name = deal_data['deal_name']
    amount = deal_data['amount']

    transformed = {
        "customer_name": deal_name,
        "invoice_total": amount,
        "deal_id": deal_id
    }
    send_data(transformed)
    

def send_data(deal: dict):
    out_json = json.dumps(deal)

    # Store the deal in the pending sends until confirmed successful
    pending_sends[deal['deal_id']] = out_json
