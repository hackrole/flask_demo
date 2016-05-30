from setuptools import setup, find_packages

readme = open('README').read()

setup(
    name='redq_flask',
    version='0.1.0',
    description=readme.partition('\n')[0],
    long_description=readme,
    author='yelinlin',
    author_email='ll.ye@bigsec.com',
    url='http://www.bigsec.com',
    packages=find_packages(
        exclude=['*.pyc']),
    include_package_data=True,
    package_data={
        'redq_um': [
            'conf/*.*',
            'templates/*.*',
            'attachment/*.*',
            'logs/*.*',
            'tmp/*.*'],
    },
    install_requires=[
        "openpyxl",
        "click",
        "tornado",
        "redq_common",
        "bigsec_common",
        "babel_python",
    ],
    entry_points={
        'console_scripts': [
            'redq_um = redq_um.run:cli',
        ]},
)
