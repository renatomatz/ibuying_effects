import csv
import requests

import pandas as pd

from threading import Thread, Lock
from bs4 import BeautifulSoup


def get_county_to_city(state, link, mutex, state_dfs, errors="warn"):

    print(f"Start {state} processing")

    soup = BeautifulSoup(requests.get("https://en.wikipedia.org"+link).text,
                         "html.parser")

    table = soup.find("table", "wikitable sortable")
    
    if table is None:
        if errors=="raise":
            raise IOError("Table not found")
        elif errors=="skip":
            pass
        elif errors=="warn":
            print("Table for ", link, " not found")
        else:
            raise ValueError("Invalid error option: ", errors)
    else:
        
        df = pd.read_html(table.prettify(), flavor="bs4").pop()
        df = df.iloc[:,[0, 2]]

        # df = df.filter(like="Borough" if state=="AK" else "Parish" if state=="LA" else "County")
        # remove wikipedia references
        # df.columns = [(col+' ')[:(col+' ').find("[")].strip().replace(" ", "_").lower() for col in df.columns]
        # df.drop(["county_code"], axis=1, inplace=True, errors="ignore")

        df.columns = ["county", "county_seat"]

        df["state"] = state
        
        mutex.acquire(1)
        state_dfs.append(df)
        mutex.release()

    print(f"End {state} processing")


DEBUG = False

if __name__ == "__main__":

    root = "https://en.wikipedia.org/wiki/Lists_of_counties_in_the_United_States"
    res = requests.get("https://en.wikipedia.org/wiki/Lists_of_counties_in_the_United_States")
    soup = BeautifulSoup(res.text, "html.parser")

    state_list = soup.find("div", "hlist hlist-separated").find_all("a")

    mutex = Lock()
    state_dfs = list()
    args = lambda state: (state.text, state["href"], mutex, state_dfs)

    if DEBUG:
        for state in state_list: get_county_to_city(*args(state))
    else:
        threads = []
        for state in state_list:
            thread = Thread(target=get_county_to_city, args=args(state))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    df = pd.concat(state_dfs).reset_index(drop=True)
    df["county"] = df["county"].str.replace(" County", "")

    df.to_csv("city_to_county.csv", index=False)
