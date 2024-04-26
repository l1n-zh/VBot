from ping3 import ping
from .FileHandler import read, write, FILE_PATH


async def record_domains_status():
    domains_status = {}
    for _, domains in read(FILE_PATH.user_settings).items():
        for domain in domains:
            domains_status[domain] = await get_status(domain, False)
    write(FILE_PATH.domains_status, domains_status)


async def get_status(domain, record = True):
    status = {}
    res = ping(domain, unit="ms", timeout=2)
    if res is None:
        status["status"] = "TIMEOUT"
    elif res is False:
        status["status"] = "ERROR"
    else:
        status["status"] = "ONLINE"
    status["ping"] = res if res else 0

    if record:
        domains_status = read(FILE_PATH.domains_status)
        domains_status[domain] = status
        write(FILE_PATH.domains_status, domains_status)

    return status
