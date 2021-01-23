import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
import TGBot, TGBot_tele


time_template = '%H:%M:%S %d.%m.%Y'
job_store = {'default': SQLAlchemyJobStore('sqlite:///remembot_jobstore.db')}
executor = {'default': ThreadPoolExecutor(max_workers=10)}
job_defaults = {
    'coalesce': False,
    'max_instances': 10
}
scheduler = BackgroundScheduler(jobstores=job_store,
                                executors=executor,
                                job_defaults=job_defaults)


def print_jobs():
    print('>>>')
    [print('{2} ** {0} ** {1}'.format(i.name,
                                      i.args[1],
                                      i.next_run_time.strftime(time_template)))
     for i in scheduler.get_jobs()]


def add_job(time: datetime, text: str, chat_id: int, job_name: str):
    """
    Adds notification to Schedulers jobstore

    :param time: notification time
    :param text: notification text
    :param chat_id: chat id to send notification to
    :param job_name: notifications name in jobstore
    :return: none
    """
    scheduler.add_job(TGBot_tele.send_msg, args=[chat_id, text, job_name],
                      next_run_time=time,
                      name=job_name,
                      replace_existing=True)
    print('{} * {} * {}'.format(time.strftime(time_template), text, job_name))

# scheduler.remove_all_jobs()
