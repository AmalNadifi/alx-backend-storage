#!/usr/bin/env python3
"""The following script is a module with tools
for request caching and tracking."""
import requests
import redis
import time


# Initialize Redis client
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches the result
    with an expiration time of 10 seconds.
    Args:
        url (str): The URL to fetch the HTML content from.
    Returns:
        str: The HTML content of the URL.
    """
    # Track the number of times the URL was accessed
    redis_client.incr(f"count:{url}")

    # Check if the page is cached
    cached_page = redis_client.get(url)
    if cached_page:
        return cached_page.decode('utf-8')

    # If not cached, fetch the page
    response = requests.get(url)
    html_content = response.text

    # Cache the page with expiration time of 10 seconds
    redis_client.setex(url, 10, html_content)
    return html_content
# Test the function


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    start_time = time.time()
    print(get_page(url))
    print("Time taken:", time.time() - start_time, "seconds")
