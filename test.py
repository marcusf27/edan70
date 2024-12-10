from requests_html import HTMLSession
import nest_asyncio
import logging

logging.disable(logging.WARNING)

import time

# Start time
start_time = time.perf_counter()

session = HTMLSession()

total_time = 0

for i in range(1, 11):
    start_time = time.perf_counter()

    r = session.get(f'https://nordiskfamiljebok.dh.gu.se/article/{2}/{i}')
    r.html.render()
    
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    print(f"Article {i} elapsed time: {elapsed_time:.6f} seconds")
    total_time += elapsed_time
    
print(total_time)