from setuptools import setup, find_packages

setup(
    name='lessons',
    py_modules=[
        'lesson01',
        'lesson02',
        'lesson03',
        'lesson04',
        'lesson05',
        'lesson06',
        'lesson07',
        'lesson08',
        'lesson09',
        'lesson10'
                ],
    version='1.0.0',
#    url = 'https://gitlab.com/???.git',
    author='Author Name',
    author_email='author@gmail.com',
    description='Description of my package',
    packages=find_packages('lessons'),
    setup_requires=['pytest-runner', 'pytest-pylint'],
    tests_require=['pytest', 'pylint']
    #    install_requires = ['pandas >= 1.11.1', 'xxx >= 1.5.1'],
)
