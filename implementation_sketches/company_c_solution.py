# company_c_solution.py
# Implementation sketches for Company C - API Gateway
# Recommended: Multiplexing + Connection Pooling
# Alternatives: Single-threaded, Multi-threaded

import asyncio
import random

# ==========================================
# Recommended: Multiplexing + Connection Pooling
# ==========================================

class ConnectionPool:
    def __init__(self, service_name, pool_size=5):
        self.service_name = service_name
        self.pool_size = pool_size
        self.semaphore = asyncio.Semaphore(pool_size)

    async def request(self, data):
        async with self.semaphore:
            print(f"Requesting {self.service_name} with {data}")
            await asyncio.sleep(random.uniform(0.1, 0.5))  # simulate network latency
            return f"Response from {self.service_name}"

async def handle_client_request(request_id):
    services = ["users", "orders", "inventory", "pricing"]
    pool_map = {s: ConnectionPool(s, pool_size=3) for s in services}

    # Fan-out requests concurrently
    responses = await asyncio.gather(*(pool_map[s].request(f"{request_id}-{s}") for s in services))
    aggregated_response = {s: r for s, r in zip(services, responses)}
    print(f"Aggregated response for {request_id}: {aggregated_response}")

# ==========================================
# Alternative 1: Single-threaded Event Loop
# ==========================================

async def single_threaded_request(request_id):
    services = ["users", "orders", "inventory", "pricing"]
    responses = []
    for s in services:
        print(f"Single-threaded requesting {s}")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        responses.append(f"Response from {s}")
    print(f"Single-threaded aggregated {request_id}: {responses}")

# ==========================================
# Alternative 2: Multi-threaded
# ==========================================

import threading

def multi_threaded_request(request_id, service):
    print(f"Thread requesting {service}")
    import time, random
    time.sleep(random.uniform(0.1, 0.5))
    print(f"Thread response from {service}")

def handle_multi_threaded_client(request_id):
    services = ["users", "orders", "inventory", "pricing"]
    threads = []
    for s in services:
        t = threading.Thread(target=multi_threaded_request, args=(request_id, s))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"Multi-threaded aggregated response for {request_id} done.")

# ==========================================
# Example usage
# ==========================================

if __name__ == "__main__":
    # Recommended multiplexing
    asyncio.run(handle_client_request("req-1"))

    # Single-threaded alternative
    asyncio.run(single_threaded_request("req-2"))

    # Multi-threaded alternative
    handle_multi_threaded_client("req-3")
