"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json
latest_attempts = {}

with open("payments.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        try:
            event = json.loads(line_stripped, strict=False)
            txn_id = event.get("txn_id")
            if txn_id:
                ts = event.get("ts", "")
                if txn_id not in latest_attempts or ts > latest_attempts[txn_id].get("ts", ""):
                    latest_attempts[txn_id] = event
        except json.JSONDecodeError:
            continue

total = 0.0
count = 0

for event in latest_attempts.values():
    if event.get("status") == "success":
        amount_str = str(event["amount"]).replace(",", "")
        total += float(amount_str)
        count += 1

with open("expected.txt", "r", encoding="utf-8") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
