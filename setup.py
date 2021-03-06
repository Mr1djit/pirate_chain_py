from distutils.core import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='pirate_chain_py',
    packages=['pirate_chain_py'],
    version='1.01',
    license='MIT',
    description='''Pirate Chain, the most anonymous cryptocurrency in existence now with python wrapped Remote Procedure Calls for easy integration with any python based program. https://pirate.black/''',
    long_description=long_description,
    author='Mr_Idjit',
    author_email='mr_idjit@protonmail.com',
    url='https://github.com/Mr1djit/pirate_chain_py',
    download_url='https://github.com/Mr1djit/pirate_chain_py/archive/refs/tags/v1.01.tar.gz',
    keywords=['Pirate Chain', 'pirate', 'chain', 'crypto', 'wallet', 'privacy', 'integration', 'finance', ' '],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Other Audience',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Office/Business :: Financial',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
