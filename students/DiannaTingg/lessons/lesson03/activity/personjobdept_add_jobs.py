"""
Add jobs for the people in the database.
"""

import personjobdept_model as pjd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Job class.')

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4


jobs = [
    ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
    ('Senior Analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
    ('Senior Business Analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
    ('Admin Supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
    ('Admin Manager', '2014-11-14', '2018-01-05', 45900, 'Peter'),
    ('Executive Assistant', '2017-01-01', '2018-06-01', 50000, 'Pam')
    ]

for job in jobs:
    try:
        with pjd.database.transaction():
            new_job = pjd.Job.create(
                job_name=job[JOB_NAME],
                start_date=job[START_DATE],
                end_date=job[END_DATE],
                salary=job[SALARY],
                person_employed=job[PERSON_EMPLOYED])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating {job[JOB_NAME]} for {job[PERSON_EMPLOYED]}.')
        logger.info(e)

logger.info('Reading and print all Job rows (note the value of person)...')

for job in pjd.Job:
    logger.info(f'{job.job_name}: {job.start_date} to {job.end_date} for {job.person_employed}.')

pjd.database.close()
