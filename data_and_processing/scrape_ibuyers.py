import csv
import requests

from threading import Thread, Lock
from bs4 import BeautifulSoup

root = "https://ibuyer.com/ibuyer-markets.html"

data_fields = [
    "avg_monthly_rent",
    "pct_chg_val",
    "med_home_val",
    "best_time_sell",
    "affordability",
    "days_to_sell",
    "job_market",
    "public_school_ranking",
]

all_fields = ["City", "State"] + data_fields + ["top_ibs", "ntop_ibs", "nlocal_ibs"]

mutex = Lock()

def process(page, mutex):
    res = requests.get("https://ibuyer.com/"+page["href"])

    soup = BeautifulSoup(res.text, "html.parser")

    data = soup.find_all("p", "market-data-value")
    data = [p.string for p in data]

    data[0] = data[0].strip("$").replace(",", "").replace(".", "")
    data[1] = data[1].strip("%").strip("+")
    data[2] = data[2].strip("$").replace(",", "").replace(".", "")

    cards = soup.find_all("div", "card")
    top_ibuyers = soup.find_all("div", "card-hover-anim")
    top_names = ", ".join([top.find("h3", "card-title").text for top in top_ibuyers])

    city, state = page.string.split(',')
    state = state.strip(" ")

    mutex.acquire(1)
    writer.writerow([city, state] + data + [top_names, len(top_ibuyers), (len(cards)-len(top_ibuyers))])
    mutex.release()

DEBUG = False

if __name__ == "__main__":

    res = requests.get(root)
    soup = BeautifulSoup(res.text, "html.parser")

    cities = soup.find_all("a", "text-white no-underline js-city-state-name")

    f = open("data/processed/processed_data.csv", "w")
    writer = csv.writer(f)
    writer.writerow(all_fields)

    if DEBUG:
        for page in cities: process(page, mutex)
    else:
        threads = []
        for page in cities:
            thread = Thread(target=process, args=(page, mutex))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
