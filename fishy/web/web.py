import requests
from whatsmyip.ip import get_ip
from whatsmyip.providers import GoogleDnsProvider

from fishy import helper
from . import urls
from .decorators import fallback, uses_session

_is_subbed = None
_session_id = None


@fallback(False)
def register_user(uid):
    ip = get_ip(GoogleDnsProvider)
    body = {"uid": uid, "ip": ip}
    response = requests.post(urls.user, json=body)
    return response.ok and response.json()["success"]


@fallback(None)
def send_notification(uid, message):
    if not is_subbed(uid):
        return False

    body = {"uid": uid, "message": message}
    requests.post(urls.notify, json=body)


@uses_session
@fallback(None)
def send_hole_deplete(uid, fish_caught, hole_time, fish_times):
    hole_data = {
        "fish_caught": fish_caught,
        "hole_time": hole_time,
        "fish_times": fish_times,
        "session": get_session(uid)
    }

    body = {"uid": uid, "hole_data": hole_data}
    requests.post(urls.hole_depleted, json=body)


@fallback(False)
def sub(uid, name):
    body = {"uid": uid, "discord_name": name}
    response = requests.post(urls.subscription, json=body)
    return response.json()["success"]


@fallback((False, False))
def is_subbed(uid, lazy=True):
    """
    :param uid:
    :param lazy:
    :return: Tuple[is_subbed, success]
    """
    global _is_subbed

    if lazy and _is_subbed is not None:
        return _is_subbed, True

    if uid is None:
        return False, False

    body = {"uid": uid}
    response = requests.get(urls.subscription, params=body)
    _is_subbed = response.json()["subbed"]
    return _is_subbed, True


@fallback(None)
def unsub(uid):
    global _is_subbed

    _is_subbed = False
    body = {"uid": uid}
    requests.delete(urls.subscription, json=body)


@fallback(None)
def get_session(config, lazy=True):
    global _session_id

    if lazy and _session_id is not None:
        return _session_id

    body = {"uid": config.get("uid")}
    response = requests.post(urls.session, params=body)

    if response.status_code == 405:
        config.delete("uid")
        helper.restart()
        return None

    _session_id = response.json()["session_id"]
    return _session_id
