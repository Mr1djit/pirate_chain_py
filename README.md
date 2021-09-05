# py Pirate Chain RPC Wallet
## _Python wrapped Pirate Chain RPC Wallet_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Example

Find your full node configuration file - 'PIRATE.conf'.
It should contain all the information to instanciate the wallet object.

```python
from pirate_chain_py.pirate_rpc_wallet import PirateWallet

pw: PirateWallet = PirateWallet(ip='127.0.0.1', port='45453', username='user388885', password='pass388885')

result: dict = pw.z_get_new_address()

your_new_address: str = result['result']

print(your_new_address)
```

## Learn more

- Pirate Chain Website: [https://pirate.black](https://pirate.black/)
- Komodo Platform: [https://komodoplatform.com](https://komodoplatform.com/)
- Pirate Blockexplorer: [https://explorer.pirate.black](https://pirate.black/)
- Pirate Discord: [https://pirate.black/discord](https://pirate.black/discord)
- Support ping Mr_Idjit: [https://pirate.black/discord](https://pirate.black/discord)
- API references & Documentation: [https://docs.pirate.black](https://docs.pirate.black/)
- Whitepaper: [Pirate Chain Whitepaper](https://pirate.black/whitepaper)

## License

MIT

**Free Software, Hell Yeah!**

