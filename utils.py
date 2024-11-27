# utils.py

def parse_message(message):
    """Example utility function to parse messages."""
    try:
        sender_id, table_data = message.split(' ', 1)
        return int(sender_id), eval(table_data)
    except Exception as e:
        print(f"Error parsing message: {e}")
        return None, None
