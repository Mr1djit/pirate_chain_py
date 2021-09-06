py Pirate Chain RPC Wallet
==========================

*Python wrapped Pirate Chain RPC Wallet*
----------------------------------------

|Build Status|

Install using pip
-----------------

``pip install pirate-chain-py``

Example
-------

| Find your full node configuration file - 'PIRATE.conf'.
| It should contain all the information to instanciate the wallet object.

.. code:: python

    from pirate_chain_py.pirate_rpc_wallet import PirateWallet

    pw: PirateWallet = PirateWallet(ip='127.0.0.1', port='45453', username='user388885', password='pass388885')

    result: dict = pw.z_get_new_address()

    your_new_address: str = result['result']

    print(your_new_address)

--------------

Learn more
----------

-  Pirate Chain Website:
   `https://pirate.black <https://pirate.black/>`__
-  Komodo Platform:
   `https://komodoplatform.com <https://komodoplatform.com/>`__
-  Pirate Blockexplorer:
   `https://explorer.pirate.black <https://pirate.black/>`__
-  Pirate Discord:
   `https://pirate.black/discord <https://pirate.black/discord>`__
-  Support ping Mr\_Idjit:
   `https://pirate.black/discord <https://pirate.black/discord>`__
-  API references & Documentation:
   `https://docs.pirate.black <https://docs.pirate.black/>`__
-  Whitepaper: `Pirate Chain
   Whitepaper <https://pirate.black/whitepaper>`__

License
-------

MIT

**Free Software, Hell Yeah!**

.. |Build Status| image:: https://travis-ci.org/joemccann/dillinger.svg?branch=master
   :target: https://travis-ci.org/joemccann/dillinger
