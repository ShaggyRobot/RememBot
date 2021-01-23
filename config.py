from datetime import datetime

token = '1490281339:AAEyQ_gQHVS58otLPhSbVSUJARgVdVu7Cek'

vip_list = ['ChitinousCruciform']

parse_config = {'PREFER_DATES_FROM': 'future'}

time_template = '%H:%M:%S %d.%m.%Y'


def time_now():
    tstr = datetime.now().strftime(time_template)
    return tstr
