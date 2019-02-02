"""
Adding people to our database.
"""

import personjobdept_model as pjd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with the Person class.')

PERSON_NAME = 0
LIVES_IN_TOWN = 1
NICKNAME = 2

people = [
    ('Andrew', 'Sumner', 'Andy'),
    ('Peter', 'Seattle', None),
    ('Susan', 'Boston', 'Beannie'),
    ('Pam', 'Coventry', 'PJ'),
    ('Steven', 'Colchester', None),
    ]

for person in people:
    try:
        with pjd.database.transaction():
            new_person = pjd.Person.create(
                    person_name=person[PERSON_NAME],
                    lives_in_town=person[LIVES_IN_TOWN],
                    nickname=person[NICKNAME])
            new_person.save()
            logger.info('Database add successful.')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

logger.info('Read and print all Person records we created...')

for person in pjd.Person:
    logger.info(f'{person.person_name} lives in {person.lives_in_town} '
                f'and likes to be known as {person.nickname}.')

pjd.database.close()
