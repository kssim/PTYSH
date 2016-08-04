
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    with open('README.md') as f:
        readme = f.read()
except:
    readme = ''

setup(
    name='ptysh',
    version='0.1.0',
    packages=['modules', 'daemon_example'],
    install_requires=['python-config', 'dbus-python'],
    py_modules = [
        'ptysh_main',
        'ptysh_base',
        'ptysh_util',
        'ptysh_module',
    ],

    author='kssim',
    author_email='ksub0912@gmail.com',
    url='https://github.com/IPOT/PTYSH',
    license='MIT License',

    description='Python Teletype Shell',
    long_description=readme,

    keywords=['shell', 'tty', 'terminal'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: System Shells',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
