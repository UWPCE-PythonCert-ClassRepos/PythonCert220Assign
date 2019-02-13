import config


def check_status(status):
    if type(status) is bool:
        return bool
    if status.lower() == 'active' or status.lower() == 'true':
        return True
    if status.lower() == 'inactive' or status.lower() == 'false':
        return False
    raise ValueError(config.etext['req_bool'].format(status))
