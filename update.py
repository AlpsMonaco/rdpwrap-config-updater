import logging

import requests


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

rdpwrap_ini_url = (
    "https://raw.githubusercontent.com/sebaxakerhtc/rdpwrap.ini/master/rdpwrap.ini"
)


def get_update_time(s: str) -> str:
    KEYWORD = "Updated="
    start_index = s.find(KEYWORD)
    if start_index == -1:
        raise RuntimeError("unable to get update time")
    return s[start_index + len(KEYWORD) : start_index + len(KEYWORD) + 10]


def get_local_update_time() -> str:
    try:
        with open(r"C:\Program Files\RDP Wrapper\rdpwrap.ini", "r") as fd:
            return get_update_time(fd.read())
    except Exception as e:
        logging.error(e)
        return ""


def write_local_rdpwrap(s:str):
    with open(r"C:\Program Files\RDP Wrapper\rdpwrap.ini", "wb") as fd:
        fd.write(s.encode())


try:
    response = requests.get(
        rdpwrap_ini_url,
        proxies={
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        },
    )
    if response.status_code != 200:
        raise RuntimeError({"code": response.status_code, "body": response.text})
    if get_local_update_time() != get_update_time(response.text):
        write_local_rdpwrap(response.text)

except Exception as e:
    logging.error(e)
