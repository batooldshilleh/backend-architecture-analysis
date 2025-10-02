# company_b_solution.py
# Implementation sketches for Company B - Image Processing Service
# Recommended: Multi-process / Multi-threaded Worker Pool with GPU
# Alternatives: Single-threaded, Multiplexing

import queue
import threading
import multiprocessing
import time
import asyncio

# ==========================================
# Recommended: Multi-process / Multi-threaded Worker Pool
# ==========================================

image_task_queue = multiprocessing.Queue()

def image_worker(task_queue, worker_id):
    while True:
        try:
            image_task = task_queue.get(timeout=5)
        except queue.Empty:
            break
        print(f"Worker {worker_id} processing {image_task['filename']}")
        # Simulate CPU/GPU processing
        time.sleep(image_task['processing_time'])
        print(f"Worker {worker_id} finished {image_task['filename']}")
        task_queue.task_done()

def start_worker_pool(num_workers):
    processes = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=image_worker, args=(image_task_queue, i))
        p.start()
        processes.append(p)
    return processes

# ==========================================
# Alternative 1: Single-threaded Event Loop
# ==========================================

async def single_threaded_worker(task):
    print(f"Async processing {task['filename']}")
    await asyncio.sleep(task['processing_time'])
    print(f"Finished {task['filename']}")

async def single_threaded_main(tasks):
    await asyncio.gather(*(single_threaded_worker(t) for t in tasks))

# ==========================================
# Alternative 2: Multiplexing (simulated)
# ==========================================

class MultiplexedProcessor:
    def __init__(self):
        self.task_queue = []

    def add_task(self, task):
        self.task_queue.append(task)

    async def process_all(self):
        # Simulate processing multiple tasks concurrently over shared resources
        await asyncio.gather(*(self._process_task(t) for t in self.task_queue))

    async def _process_task(self, task):
        print(f"Multiplexed processing {task['filename']}")
        await asyncio.sleep(task['processing_time'])
        print(f"Finished {task['filename']}")

# ==========================================
# Example usage
# ==========================================

if __name__ == "__main__":
    images = [
        {"filename": "image1.jpg", "processing_time": 4},
        {"filename": "image2.jpg", "processing_time": 6},
        {"filename": "image3.jpg", "processing_time": 3},
    ]

    # --- Recommended ---
    for img in images:
        image_task_queue.put(img)
    workers = start_worker_pool(num_workers=4)
    for w in workers:
        w.join()

    # --- Single-threaded alternative ---
    asyncio.run(single_threaded_main(images))

    # --- Multiplexing alternative ---
    mux = MultiplexedProcessor()
    for img in images:
        mux.add_task(img)
    asyncio.run(mux.process_all())
