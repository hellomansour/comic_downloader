#! python3
# threaded_xkcd_downloader.py - Downloads XKCD comics using multiple threads

import threading
from pathlib import Path

import bs4
import requests

folder = Path("xkcd")
folder.mkdir(exist_ok=True)  # store comics in ./xkcd


def download_xkcd(start_comic, end_comic):
    for urlnum in range(start_comic, end_comic):
        print(f"Retrieving page https://xkcd.com/{urlnum}...")
        res = requests.get(f"https://xkcd.com/{urlnum}")
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Find the URL of comic image.
        comic_elem = soup.select("#comic > img")
        if not comic_elem:
            print("Could not find comic image")
        else:
            comic_url = comic_elem[0].get("src")
            print(f"Downloading image {Path(comic_url).name}...")
            res = requests.get(f"https:{comic_url}")
            res.raise_for_status()

            # Save image to xkcd folder
            with open(folder / Path(comic_url).name, "wb") as imgfile:
                for chunk in res.iter_content(100_000):
                    imgfile.write(chunk)


# Download files in batches of 10
download_threads = []
for i in range(1, 100, 10):
    start, end = i, i + 9
    thread = threading.Thread(target=download_xkcd, args=(start, end))
    download_threads.append(thread)
    thread.start()

# Wait for all threads to end
for thread in download_threads:
    thread.join()
print("Done.")
