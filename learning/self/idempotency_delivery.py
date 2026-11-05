import uuid
import time
from typing import Dict, Any, Optional

# =====================================================================
# SYSTEM DESIGN INSIGHT: What is Idempotency?
# Idempotency means that making the same request multiple times has the
# same effect as making it once. In distributed systems, networks can fail.
# If a client sends a payment request and the network drops, the client
# doesn't know if the payment succeeded. So, it retries. Without
# idempotency, the customer would be charged twice!
# =====================================================================

class IdempotencyDb:
    """
    A mock database/cache to store processed request keys.
    In a real system, this would be a distributed store like Redis or a SQL/NoSQL DB.
    """
    def __init__(self):
        # We use a Python dictionary to act as our storage.
        # Key: Idempotency Key (a unique string)
        # Value: A dictionary containing the processing status and the saved response.
        self._db: Dict[str, Dict[str, Any]] = {}

    def get_status(self, key: str) -> Optional[Dict[str, Any]]:
        """Checks if this key has been seen before."""
        return self._db.get(key)

    def mark_as_processing(self, key: str): 
        """Marks the key as 'processing' so duplicate concurrent requests are blocked."""
        self._db[key] = {"status": "processing", "response": None}

    def save_result(self, key: str, response: Any):
        """Saves the final response and marks the key as 'completed'."""
        self._db[key] = {"status": "completed", "response": response}


class PaymentProcessor:
    """
    A service that processes payments.
    It uses our IdempotencyDb to guarantee that each unique payment request
    is processed exactly once.
    """
    def __init__(self, db: IdempotencyDb):
        self.db = db

    def process_payment(self, idempotency_key: str, customer_id: str, amount: float) -> Dict[str, Any]:
        print(f"\n--- [Server] Received payment request with Key: {idempotency_key} ---")

        # 1. Read Phase: Check if we have already processed (or are processing) this key
        existing_record = self.db.get_status(idempotency_key)

        if existing_record:
            status = existing_record["status"]
            if status == "completed":
                # System Design Insight: Deduplication. We do not run the logic again.
                # Instead, we return the cached response.
                print(f"[Idempotency Guard] Key '{idempotency_key}' already processed. Returning cached response.")
                return {
                    "success": True,
                    "amount": amount,
                    "transaction_id": existing_record["response"]["transaction_id"],
                    "duplicated": True
                }
            elif status == "processing":
                # System Design Insight: Concurrent requests protection (Distributed Lock pattern).
                # If the same request comes in while the first is still running, block/reject it.
                print(f"[Idempotency Guard] Key '{idempotency_key}' is in progress. Rejecting duplicate request.")
                return {
                    "success": False,
                    "error": "Request already in progress. Please wait.",
                    "duplicated": True
                }

        # 2. Write Phase: Reserve the key to mark that we are working on it
        self.db.mark_as_processing(idempotency_key)

        # Simulate the actual business logic (charging money via a bank API)
        print(f"[Core Logic] Charging ${amount} from customer '{customer_id}'...")
        time.sleep(0.5)  # Simulate network latency of bank communication
        
        # Create a mock transaction ID
        transaction_id = f"tx_{uuid.uuid4().hex[:8]}"
        response_data = {
            "transaction_id": transaction_id,
            "processed_at": time.time()
        }

        # 3. Update Phase: Save the result and mark as complete
        self.db.save_result(idempotency_key, response_data)
        print(f"[Core Logic] Successfully processed payment. Transaction ID: {transaction_id}")

        return {
            "success": True,
            "amount": amount,
            "transaction_id": transaction_id,
            "duplicated": False
        }


# =====================================================================
# SIMULATION: Client Retries
# =====================================================================
if __name__ == "__main__":
    # Initialize our database and processor
    my_db = IdempotencyDb()
    processor = PaymentProcessor(my_db)

    # Imagine a customer is buying a product
    cust_id = "user_456"
    price = 99.99
    
    # The client creates a unique key for this single action
    # (e.g., clicking the 'Buy Now' button once)
    payment_key = str(uuid.uuid4())

    print(f"Client generated Idempotency Key: {payment_key}")

    # Attempt 1: First request.
    # This represents a normal, successful request.
    print("\n--- ATTEMPT 1 ---")
    result1 = processor.process_payment(payment_key, cust_id, price)
    print(f"Client received: {result1}")

    # Attempt 2: Duplicate request.
    # Imagine a network glitch: the server processed payment #1, but the network
    # broke before the client got the response. The client retries.
    print("\n--- ATTEMPT 2 (Retry due to network failure) ---")
    result2 = processor.process_payment(payment_key, cust_id, price)
    print(f"Client received: {result2}")

    # Notice that the transaction ID is the SAME, and no second charge was made!
