from requests_html import AsyncHTMLSession
import logging
import asyncio
import time

logging.disable(logging.WARNING)

session = AsyncHTMLSession()

start_time = time.perf_counter()
total_time = 0


async def fetch_entry(edition, article, session, progress_counter):
    response = await session.get(f'https://nordiskfamiljebok.dh.gu.se/article/{edition}/{article}')
    await response.html.arender()

    progress_counter[0] += 1

    print(f"{progress_counter[0]} / 10: article #{article} text: {response.text}\n")
    
    return response.html



async def fetch_entries(articles, progress_counter):
    session = AsyncHTMLSession()
    
    async with asyncio.TaskGroup() as task_group:
        tasks = [task_group.create_task(fetch_entry(2, article, session, progress_counter))
                 for article in articles]


async def main():
    progress_counter = [0]
    
    start_time = time.perf_counter()

    await fetch_entries(range(1, 11), progress_counter)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.6f} seconds")


asyncio.run(main())
