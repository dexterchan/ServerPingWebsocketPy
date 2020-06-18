from setuptools import setup, find_packages


setup(
    name='ServerPingWebSocketPy',
    version='0.1.0',
    description='Ping server',
    author='Dexter Chan',
    author_email='abcd@abcd.com',
    packages=find_packages(exclude=('PyPingServerIntegrationTest', 'docs'))
)