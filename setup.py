from setuptools import setup, find_packages

setup(
    name='ftpy',
    use_scm_version=True,
    url='https://github.com/dumunari/ftpy',
    license='MIT',
    author='Eduardo Munari',
    author_email='munari.edu@gmail.com',
    scripts=["bin/ftpy"],
    description='Pyftpdlib-based FTP Server created to be used on performance tests.',
    install_requires=["pyftpdlib"],
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
)