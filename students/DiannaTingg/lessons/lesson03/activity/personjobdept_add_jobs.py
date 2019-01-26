"""
Add jobs with departments for the people in the database.
"""

from personjobdept_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Job class')
logger.info('Creating Job records: just like Person. We use the foreign key')

JOB_NAME = 0
DEPT_NUM = 1
DEPT_NAME = 2
DEPT_MANAGER = 3
START_DATE = 4
END_DATE = 5
SALARY = 6
PERSON_EMPLOYED = 7


jobs = [
    ('Analyst', 'H123', 'Human Resources', 'Susan Bell', '2001-09-22', '2003-01-30',65500, 'Andrew'),
    ('Senior Analyst', 'H123', 'Human Resources', 'Susan Bell', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
    ('Senior Business Analyst', 'F245', 'Finance', 'Wally Smith', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
    ('Admin Supervisor', 'Q321', 'Quality', 'Chris Wood', '2012-10-01', '2014-11-10', 45900, 'Peter'),
    ('Admin Manager', 'Q321', 'Quality', 'Chris Wood', '2014-11-14', '2018-01-05', 45900, 'Peter'),
    ('Executive Assistant', 'A432', 'Administration', 'Florence Cook', '2017-01-01', '2018-06-01', 50000, 'Pam')
    ]

for job in jobs:
    try:
        with database.transaction():
            new_job = Job.create(
                job_name=job[JOB_NAME],
                dept_num=job[DEPT_NUM],
                dept_name=job[DEPT_NAME],
                dept_manager=job[DEPT_MANAGER],
                start_date=job[START_DATE],
                end_date=job[END_DATE],
                salary=job[SALARY],
                person_employed=job[PERSON_EMPLOYED])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

logger.info('Reading and print all Job rows (note the value of person)...')

for job in Job:
    logger.info(f'{job.job_name}: {job.start_date} to {job.end_date} for {job.person_employed}')

database.close()
