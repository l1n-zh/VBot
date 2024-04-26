from tldextract import extract
from enum import Enum
from .FileHandler import read, write, FILE_PATH
from .DomainStatusChecker import get_status, record_domains_status
from typing import List, Dict


class RETURNCODE(Enum):
    FAILED = -1
    NOT_EXIST = 0
    SUCCESS = 1
    DUPLICATE = 2

def get_domains(uid) -> List[str]:
    return read(FILE_PATH.user_settings).get(uid, [])

async def get_domains_status(uid) -> Dict[str, Dict]:
    all_domains_status = read(FILE_PATH.domains_status)
    target_domains = get_domains(uid)
    target_domains_status = {}

    for domain in target_domains:
        if not domain in all_domains_status:
            domain_status = await get_status(domain)
        else:
            domain_status = all_domains_status[domain]
        target_domains_status[domain] = domain_status
    
    return target_domains_status


async def add_domain(uid, target) -> RETURNCODE:
    try:
        domain = extract(target).registered_domain
        if not domain:
            raise
    except:
        return RETURNCODE.FAILED
    data: dict = read(FILE_PATH.user_settings)
    data.setdefault(uid, [])
    if domain in data[uid]:
        return RETURNCODE.DUPLICATE
    else:
        data[uid].append(domain)

    write(FILE_PATH.user_settings, data)
    await get_status(domain)
    return RETURNCODE.SUCCESS


async def remove_domain(uid: str, domain: str) -> RETURNCODE:
    data = read(FILE_PATH.user_settings)
    domains = data.get(uid)
    try:
        domains.remove(domain)
    except ValueError:
        return RETURNCODE.NOT_EXIST
    else:
        write(FILE_PATH.user_settings, data)
        await record_domains_status()
        return RETURNCODE.SUCCESS