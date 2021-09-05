"""
Pirate Chain RPC methods wrapped in Python
"""

from uuid import uuid4
from requests import post, status_codes
from requests.auth import HTTPBasicAuth


class PirateWallet:
    """
    Class with all fully documented Pirate Chain RPC methods.
    """
    def __init__(self, ip: str, port: str, username: str, password: str):
        self.url = f'http://{ip}:{port}'
        self.auth = HTTPBasicAuth(username=username, password=password)

    def _request(self, payload: dict):
        """
        Used internally to make RPC calls.
        :param payload: {method: method_name, params: params_values}
        :return: { 'result': RESULT(json/dict/string/int/none), 'error': None, 'id': 'opid-GUID' }
        """
        if payload.get('jsonrpc', None) is None: payload['jsonrpc'] = '1.0'
        if payload.get('id', None) is None: payload['id'] = str(uuid4())

        _res = post(url=self.url, json=payload, auth=self.auth)
        if _res.ok:
            if _res.json() == 'null':
                return None
            return _res.json()
        else:
            raise ConnectionError(f'{_res.status_code} - {next(iter(status_codes._codes[_res.status_code]), None)}')

    def get_all_data(self, datatype: int, args=None):
        """
        This function only returns information on wallet addresses with full spending keys.\n
        -------------

        Arguments:
            1. "datatype"     (integer, required)
                                Value of 0: Return address, balance, transactions and blockchain info
                                Value of 1: Return address, balance, blockchain info
                                Value of 2: Return transactions and blockchain info
            2. "transactiontype"     (integer, optional)
                                Value of 0: Return all transactions
                                Value of 1: Return all transactions in the last 24 hours
                                Value of 2: Return all transactions in the last 7 days
                                Value of 3: Return all transactions in the last 30 days
                                Value of 4: Return all transactions in the last 90 days
                                Value of 5: Return all transactions in the last 365 days
                                Other number: Return all transactions
            3. "transactioncount"     (integer, optional)
            4. "Include Watch Only"   (bool, optional, Default = false)
        -------------

        docs: https://docs.pirate.black/docs/rpc/getalldata/

        :param datatype: Required parameter.
        :param args: Optional parameters.
        :return: JSON or None
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'getalldata', 'params': [datatype] + args})

    def zs_get_transaction(self, tx_id: str):
        """
        Returns a decrypted Pirate transaction.\n
        -------------

        Arguments:
            1. "txid:"   (string, required)
        -------------

        docs: https://docs.pirate.black/docs/rpc/zs_gettransaction/

        :param tx_id: String transaction ID
        :return:
        """
        return self._request(payload={'method': 'zs_gettransaction', 'params': [tx_id]})

    def zs_list_received_by_address(self, address: str, args=None):
        """
        Returns decrypted Pirate received outputs for a single address.\n
        This function only returns information on addresses with full spending keys.\n
        -------------

        Arguments:
            1. "address:"                (string, required)
            2. "Minimum Confimations:"   (numeric, optional, default=0)
            3. "Filter Type:"            (numeric, optional, default=0)
                                           Value of 0: Returns all transactions in the wallet
                                           Value of 1: Returns the last x days of transactions
                                           Value of 2: Returns transactions with confimations less than x
                                           Value of 3: Returns transactions with a minimum block height of x
            4. "Filter:"                 (numeric, optional, default=0)
                                           Filter Type equal 0: paramater ignored
                                           Filter Type equal 1: number represents the number of days returned
                                           Filter Type equal 2: number represents the max confirmations for transaction to be returned
                                           Filter Type equal 3: number represents the minimum block height of the transactions returned
            5. "Count:"                 (numeric, optional, default=100000)
                                           Last n number of transactions returned
        Default Parameters:
            2. 0  0 confimations required
            3. 0  Returns all transactions
            4. 0  Ignored
            5. 100000 - Return the last 9,999,999 transactions.
        -------------

        docs: https://docs.pirate.black/docs/rpc/zs_listreceivedbyaddress/

        :param address: Required parameter.
        :param args: Optional parameters.
        :return: JSON or None
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'zs_listreceivedbyaddress', 'params': [address] + args})

    def zs_list_sent_by_address(self, address: str, args: list):
        """
        Returns decrypted Pirate outputs sent to a single address.\n
        This function only returns information on addresses sent from wallet addresses with full spending keys.\n
        -------------

        Arguments:
            1. "address:"                (string, required)
            2. "Minimum Confimations:"   (numeric, optional, default=0)
            3. "Filter Type:"            (numeric, optional, default=0)
                                           Value of 0: Returns all transactions in the wallet
                                           Value of 1: Returns the last x days of transactions
                                           Value of 2: Returns transactions with confimations less than x
                                           Value of 3: Returns transactions with a minimum block height of x
            4. "Filter:"                 (numeric, optional, default=0)
                                           Filter Type equal 0: paramater ignored
                                           Filter Type equal 1: number represents the number of days returned
                                           Filter Type equal 2: number represents the max confirmations for transaction to be returned
                                           Filter Type equal 3: number represents the minimum block height of the transactions returned
            5. "Count:"                 (numeric, optional, default=100000)
                                           Last n number of transactions returned
        Default Parameters:
            2. 0 - 0 confirmations required
            3. 0 - Returns all transactions
            4. 0 - Ignored
            5. 100000 - Return the last 9,999,999 transactions.
        -------------

        docs: https://docs.pirate.black/docs/rpc/zs_listsentbyaddress/

        :param address: Required parameter
        :param args: Optional parameters.
        :return: JSON or None
        """
        return self._request(payload={'method': 'zs_listsentbyaddress', 'params': [address] + args})

    def zs_list_spent_by_address(self, address: str, args=None):
        """
        Returns decrypted Pirate outputs sent to a single address.\n
        This function only returns information on addresses sent from wallet addresses with full spending keys.\n
        -------------

        Arguments:
            1. "address:"                (string, required)
            2. "Minimum Confimations:"   (numeric, optional, default=0)
            3. "Filter Type:"            (numeric, optional, default=0)
                                           Value of 0: Returns all transactions in the wallet
                                           Value of 1: Returns the last x days of transactions
                                           Value of 2: Returns transactions with confimations less than x
                                           Value of 3: Returns transactions with a minimum block height of x
            4. "Filter:"                 (numeric, optional, default=0)
                                           Filter Type equal 0: paramater ignored
                                           Filter Type equal 1: number represents the number of days returned
                                           Filter Type equal 2: number represents the max confirmations for transaction to be returned
                                           Filter Type equal 3: number represents the minimum block height of the transactions returned
            5. "Count:"                 (numeric, optional, default=100000)
                                           Last n number of transactions returned
        Default Parameters:
            2. 0 - 0 confimations required
            3. 0 - Returns all transactions
            4. 0 - Ignored
            5. 100000 - Return the last 9,999,999 transactions.
        -------------

        docs: https://docs.pirate.black/docs/rpc/zs_listsentbyaddress/

        :param address: required parameter
        :param args:
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'zs_listspentbyaddress', 'params': [address] + args})

    def zs_list_transactions(self, args: list):
        """
        Returns an array of decrypted Pirate transactions.\n
        This function only returns information on addresses with full spending keys.\n
        -------------

        Arguments:
            1. "Minimum Confimations:"   (numeric, optional, default=0)
            2. "Filter Type:"            (numeric, optional, default=0)
                                           Value of 0: Returns all transactions in the wallet
                                           Value of 1: Returns the last x days of transactions
                                           Value of 2: Returns transactions with confimations less than x
                                           Value of 3: Returns transactions with a minimum block height of x
            3. "Filter:"                 (numeric, optional, default=0)
                                           Filter Type equal 0: paramater ignored
                                           Filter Type equal 1: number represents the number of days returned
                                           Filter Type equal 2: number represents the max confirmations for transaction to be returned
                                           Filter Type equal 3: number represents the minimum block height of the transactions returned
            4. "Count:"                 (numeric, optional, default=100000)
                                           Last n number of transactions returned
            5. "Include Watch Only"     (bool, optional, Default = false)
        Default Parameters:
            1. 0 - 0 confimations required
            2. 0 - Returns all transactions
            3. 0 - Ignored
            4. 100000 - Return the last 100,000 transactions.
            5. false - exclude watch only
        -------------

        docs: https://docs.pirate.black/docs/rpc/zs_listtransactions/

        :param args: Optional parameters.
        :return: JSON or None
        """
        return self._request(payload={'method': 'zs_listtransactions', 'params': args})

    def z_build_raw_transaction(self, hex_string: str):
        """
        Return a JSON object representing the serialized, hex-encoded transaction.\n
        -------------

        Arguments:
            1. "hex"      (string, required) The transaction hex string
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_buildrawtransaction/

        :param hex_string: Required parameter.
        :return: JSON or None
        """
        return self._request(payload={'method': 'z_buildrawtransaction', 'params': [hex_string]})

    def z_create_build_instructions(self, inputs: list, outputs: list, args=None):
        """
        \n
        -------------

        Arguments:
            1. "inputs"                (array, required) A json array of json input objects
                 [
                   {
                     "txid":"id",          (string, required) The transaction id
                     "index":n,          (numeric, required) shieldedOutputIndex of input transaction
                   }
                   ,...
                 ]
            2. "outputs"               (array, required) A json array of json output objects
                 [
                   {
                     "address":address     (string, required) Pirate zaddr
                     "amount":amount       (numeric, required) The numeric amount in ARRR
                     "memo": "string"    (string, optional) String memo in UTF8 ro Hexidecimal format
                     ,...
                   }
                 ]
            3. fee                  (numeric, optional, default=0.0001
            4. expiryheight          (numeric, optional, default=200) Expiry height of transaction (if Overwinter is active)

        Result:
            "transaction"            (string) hex string of the transaction
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_createbuildinstructions/

        :param outputs:
        :param inputs:
        :param args:
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_createbuildinstructions', 'params': [inputs, outputs] + args})

    def z_export_key(self, z_address: str):
        """
        Reveals the zkey corresponding to ‘zaddr’. Then the z_importkey can be used with this output\n
        -------------

        Arguments:
            1. "zaddr"   (string, required) The zaddr for the private key

        Result:
            "key" (string) The private key
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_exportkey/

        :param z_address: Required parameter.
        :return:
        """
        return self._request(payload={'method': 'z_exportkey', 'params': [z_address]})

    def z_validate_address(self, z_address: str):
        """
        Return information about the given z address.\n
        -------------

        Arguments:
            1. "zaddr"   (string, required) The zaddr for the private key

        Result:
            {
              "isvalid" : true|false,      (boolean) If the address is valid or not. If not, this is the only property returned. \n
              "address" : "zaddr",         (string) The z address validated \n
              "type" : "xxxx",             (string) "sprout" or "sapling" \n
              "ismine" : true|false,       (boolean) If the address is yours or not \n
              "payingkey" : "hex",         (string) [sprout] The hex value of the paying key, a_pk \n
              "transmissionkey" : "hex",   (string) [sprout] The hex value of the transmission key, pk_enc \n
              "diversifier" : "hex",       (string) [sapling] The hex value of the diversifier, d \n
              "diversifiedtransmissionkey" : "hex", (string) [sapling] The hex value of pk_d \n
            }


        -------------

        docs: https://docs.pirate.black/docs/rpc/z_validateaddress/

        :param z_address: Required parameter
        :return:
        """
        return self._request(payload={'method': 'z_validateaddress', 'params': [z_address]})

    def z_export_viewing_key(self, z_address: str):
        """
        Reveals the viewing key corresponding to ‘zaddr’. Then the z_importviewingkey can be used with this output\n
        -------------

        Arguments:
            1. "zaddr"   (string, required) The zaddr for the viewing key

        Result:
            "v_key" (string) The viewing key
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_exportviewingkey/

        :return:
        """
        return self._request(payload={'method': 'z_exportviewingkey', 'params': [z_address]})

    def z_export_wallet(self, filename: str):
        """
        Exports all wallet keys, for taddr and zaddr, in a human-readable format. Overwriting an existing file is not permitted.\n
        Advice the filename should only contain alphanumeric characters.\n
        -------------

        Arguments:
            1. "filename" (string, required) The filename, saved in folder set by pirated -exportdir option

        Result:
            "path" (string) The full path of the destination file
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_exportwallet/

        :param filename: Required parameter
        :return:
        """
        return self._request(payload={'method': 'z_exportwallet', 'params': [filename]})

    def z_get_balance(self, address: str, args=None):
        """
        Returns the balance of a taddr or zaddr belonging to the node’s wallet.\n
        CAUTION: If the wallet has only an incoming viewing key for this address, then spends cannot be detected, and so the returned balance may be larger than the actual balance.\n
        -------------

        Arguments:
            1. "address"      (string) The selected address. It may be a transparent or private address.
            2. minconf          (numeric, optional, default=1) Only include transactions confirmed at least this many times.

        Result:
            amount              (numeric) The total amount in ARRR received for this address.
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_getbalance/

        :param address: Required parameter.
        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_getbalance', 'params': [address] + args})

    def z_get_balances(self, args=None):
        """
        Returns array of wallet sapling addresses and balances. Results are an array of Objects, each of which has: {address,balance,unconfirmed,spendable}\n
        -------------

        Arguments:
            1. includeWatchonly (bool, optional, default=false) Also include watch only addresses (see 'z_importviewingkey')

        Result
            [                             (array of json object)
              {
                "address" : "address",          (string) the transaction id
                "balance" : n             (numeric) confirmed address balance
                "unconfirmed" : n             (numeric) unconfirmed address balance
              }
              ,...
            ]
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_getbalances/

        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_getbalances', 'params': args})

    def z_get_total_balance(self, args=None):
        """
        Return the total value of funds stored in the node’s wallet.\n
        CAUTION: If the wallet contains any addresses for which it only has incoming viewing keys, the returned private balance may be larger than the actual balance, because spends cannot be detected with incoming viewing keys.\n
        -------------

        Arguments:
            1. minconf          (numeric, optional, default=1) Only include private and transparent transactions confirmed at least this many times.
            2. includeWatchonly (bool, optional, default=false) Also include balance in watchonly addresses (see 'importaddress' and 'z_importviewingkey')

        Result:
            {
              "transparent": xxxxx,     (numeric) the total balance of transparent funds
              "private": xxxxx,         (numeric) the total balance of private funds (in both Sprout and Sapling addresses)
              "total": xxxxx,           (numeric) the total balance of both transparent and private funds
            }

        docs: https://docs.pirate.black/docs/rpc/z_gettotalbalance/

        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_gettotalbalance', 'params': args})

    def z_get_new_address(self):
        """
        Returns a new diversified shielded address for receiving payments. \n
        -------------

        Result:
            "PIRATE_address"    (string) The new diversified shielded address.

        docs: https://docs.pirate.black/docs/rpc/z_getnewaddress/

        :return:
        """
        return self._request(payload={'method': 'z_getnewaddress', 'params': []})

    def z_get_new_address_key(self, address_type='sapling'):
        """
        This creates a new sapling extended spending key and returns a new shielded address for receiving payments. \n
        With no arguments, returns a Sapling address. \n
        -------------

        Arguments:
            1. "type"         (string, optional, default="sapling") The type of address. One of ["sprout", "sapling"].
        Result:
            "PIRATE_address"    (string) The new shielded address.
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_getnewaddresskey/

        :param address_type: Optional parameter has to be either ('sprout', 'sapling')
        :return:
        """
        if address_type not in ('sprout', 'sapling'): TypeError(f'"address_type" has to be either "sprout" or "sapling". Got {address_type}')
        return self._request(payload={'method': 'z_getnewaddresskey', 'params': [address_type]})

    def z_get_operation_result(self, operation_ids=None):
        """
        Retrieve the result and status of an operation which has finished, and then remove the operation from memory.\n
        -------------

        Arguments:
            1. "operationid"         (array, optional) A list of operation ids we are interested in.  If not provided, examine all operations known to the node.
        Result:
            "[object, ...]"          (array) A list of JSON objects
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_getoperationresult/

        :param operation_ids: Optional ids of operations...
        :return:
        """
        if operation_ids is None: operation_ids = []
        if not isinstance(operation_ids, list): raise TypeError(f'"operation_ids" parameter should be a list of string - operation ids. Got {type(operation_ids)} instead.')
        return self._request(payload={'method': 'z_getoperationresult', 'params': [operation_ids]})

    def z_get_operation_status(self, operation_ids=None):
        """
        Get operation status and any associated result or error data. The operation will remain in memory.\n
        -------------

        Arguments:
            1. "operationid"         (array, optional) A list of operation ids we are interested in.  If not provided, examine all operations known to the node.
        Result:
            "[object, ...]"          (array) A list of JSON objects
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_getoperationstatus/

        :param operation_ids: Optional parameters.
        :return:
        """
        if operation_ids is None: operation_ids = []
        return self._request(payload={'method': 'z_getoperationstatus', 'params': [operation_ids]})

    def z_import_key(self, z_key: str, args=None):
        """
        Adds a zkey (as returned by z_exportkey) to your wallet.\n
        -------------

        Arguments:
            1. "zkey"             (string, required) The zkey (see z_exportkey)
            2. rescan             (string, optional, default="whenkeyisnew") Rescan the wallet for transactions - can be "yes", "no" or "whenkeyisnew"
            3. startHeight        (numeric, optional, default=0) Block height to start rescan from
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_importkey/

        :param z_key: required parameter.
        :param args: optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_importkey', 'params': [z_key] + args})

    def z_import_viewing_key(self, v_key: str, args=None):
        """
        Adds a viewing key (as returned by z_exportviewingkey) to your wallet.\n
        -------------

        Arguments:
            1. "vkey"             (string, required) The viewing key (see z_exportviewingkey)
            2. rescan             (string, optional, default="whenkeyisnew") Rescan the wallet for transactions - can be "yes", "no" or "whenkeyisnew"
            3. startHeight        (numeric, optional, default=0) Block height to start rescan from

            Note: This call can take minutes to complete if rescan is true.
        Result:
            {
              "type" : "xxxx",                         (string) "sprout" or "sapling"
              "address" : "address|DefaultAddress",    (string) The address corresponding to the viewing key (for Sapling, this is the default address).
            }
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_importviewingkey/

        :param v_key: Required parameter.
        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_importviewingkey', 'params': [v_key] + args})

    def z_import_wallet(self, filename: str):
        """
        Imports taddr and zaddr keys from a wallet export file (see z_exportwallet).\n
        -------------

        Arguments:
            1. "filename"    (string, required) The wallet file
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_importwallet/

        :param filename: Required parameter.
        :return:
        """
        return self._request(payload={'method': 'z_importwallet', 'params': [filename]})

    def z_list_addresses(self, args=None):
        """
        Returns the list of Sprout and Sapling shielded addresses belonging to the wallet.\n
        -------------

        Arguments:
            1. includeWatchonly (bool, optional, default=false) Also include watchonly addresses (see 'z_importviewingkey')
        Result:
            [                     (json array of string)
              "zaddr"           (string) a zaddr belonging to the wallet
              ,...
            ]
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_listaddresses/

        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_listaddresses', 'params': args})

    def z_list_operation_ids(self, args=None):
        """
        Returns the list of operation ids currently known to the wallet.\n
        -------------

        Arguments:
            1. "status"         (string, optional) Filter result by the operation's state e.g. "success".
        Result:
            [                     (json array of string)
              "operationid"       (string) an operation id belonging to the wallet
              ,...
            ]
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_listoperationids/

        :param args: Optional requirements.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_listoperationids', 'params': args})

    def z_list_received_by_address(self, address: str, args=None):
        """
        Return a list of amounts received by a zaddr belonging to the node’s wallet.\n
        -------------

        Arguments:
            1. "address"      (string) The private address.
            2. minconf          (numeric, optional, default=1) Only include transactions confirmed at least this many times.
        Result:
            {
              "txid": xxxxx,           (string) the transaction id \n
              "amount": xxxxx,         (numeric) the amount of value in the note \n
              "memo": xxxxx,           (string) hexadecimal string representation of memo field \n
              "confirmations" : n,     (numeric) the number of confirmations \n
              "jsindex" (sprout) : n,     (numeric) the joinsplit index \n
              "jsoutindex" (sprout) : n,     (numeric) the output index of the joinsplit \n
              "outindex" (sapling) : n,     (numeric) the output index \n
              "change": true|false,    (boolean) true if the address that received the note is also one of the sending addresses \n
            }
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_listreceivedbyaddress/

        :param address: Required parameter.
        :param args: Optional parameters
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_listreceivedbyaddress', 'params': [address] + args})

    def z_list_unspent(self, args=None):
        """
        Returns array of unspent shielded notes with between minconf and maxconf (inclusive) confirmations. \n
        Optionally filter to only include notes sent to specified addresses. \n
        When minconf is 0, unspent notes with zero confirmations are returned, even though they are not immediately spendable. \n
        Results are an array of Objects, see 'result' \n
        -------------

        Arguments:
            1. minconf          (numeric, optional, default=1) The minimum confirmations to filter
            2. maxconf          (numeric, optional, default=9999999) The maximum confirmations to filter
            3. includeWatchonly (bool, optional, default=false) Also include watchonly addresses (see 'z_importviewingkey')
            4. "addresses"      (string) A json array of zaddrs (Sapling Only) to filter on.  Duplicate addresses not allowed.
                [
                  "address"     (string) zaddr
                  ,...
                ]

        Result:
            [                             (array of json object)
              {
                "txid" : "txid",          (string) the transaction id \n
                "jsindex" : n             (numeric) the joinsplit index \n
                "jsoutindex" (sprout) : n          (numeric) the output index of the joinsplit \n
                "outindex" (sapling) : n          (numeric) the output index \n
                "confirmations" : n       (numeric) the number of confirmations \n
                "spendable" : true|false  (boolean) true if note can be spent by wallet, false if note has zero confirmations, false if address is watchonly \n
                "address" : "address",    (string) the shielded address \n
                "amount": xxxxx,          (numeric) the amount of value in the note \n
                "memo": xxxxx,            (string) hexademical string representation of memo field \n
                "change": true|false,     (boolean) true if the address that received the note is also one of the sending addresses \n
              }
              ,...
            ]
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_listunspent/

        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_listunspent', 'params': args})

    def z_merge_to_address(self, from_addresses: list, to_address: str, args=None):
        """
        Merge multiple UTXOs and notes into a single UTXO or note. Coinbase UTXOs are ignored; use z_shieldcoinbase to combine those into a single note. \n
        This is an asynchronous operation, and UTXOs selected for merging will be locked. If there is an error, they are unlocked. \n
        The RPC call listlockunspent can be used to return a list of locked UTXOs. \n
        The number of UTXOs and notes selected for merging can be limited by the caller. \n
        If the transparent limit parameter is set to zero, and Overwinter is not yet active, the -mempooltxinputlimit option will determine the number of UTXOs. \n
        Any limit is constrained by the consensus rule defining a maximum transaction size of 100000 bytes before Sapling, and 200000 bytes once Sapling activates. \n
        -------------

        Arguments:
            1. fromaddresses         (string, required) A JSON array with addresses.
                             The following special strings are accepted inside the array:
                                 - "*": Merge both UTXOs and notes from all addresses belonging to the wallet.
                                 - "ANY_TADDR": Merge UTXOs from all t-addrs belonging to the wallet.
                                 - "ANY_ZADDR": Merge notes from all z-addrs belonging to the wallet.
                             If a special string is given, any given addresses of that type will be ignored.
                [
                  "address"          (string) Can be a t-addr or a z-addr
                  ,...
                ]
            2. "toaddress"           (string, required) The t-addr or z-addr to send the funds to.
            3. fee                   (numeric, optional, default=0.0001) The fee amount to attach to this transaction.
            4. transparent_limit     (numeric, optional, default=50) Limit on the maximum number of UTXOs to merge.  Set to 0 to use node option -mempooltxinputlimit (before Overwinter), or as many as will fit in the transaction (after Overwinter).
            4. shielded_limit        (numeric, optional, default=10 Sprout or 90 Sapling Notes) Limit on the maximum number of notes to merge.  Set to 0 to merge as many as will fit in the transaction.
            5. maximum_utxo_size       (numeric, optional) eg, 0.0001 anything under 10000 satoshies will be merged, ignores 10,000 sat p2pk utxo that iguana uses, and merges coinbase utxo.
            6. "memo"                (string, optional) Encoded as hex. When toaddress is a z-addr, this will be stored in the memo field of the new note.

        Result:
            {
              "remainingUTXOs": xxx               (numeric) Number of UTXOs still available for merging. \n
              "remainingTransparentValue": xxx    (numeric) Value of UTXOs still available for merging. \n
              "remainingNotes": xxx               (numeric) Number of notes still available for merging. \n
              "remainingShieldedValue": xxx       (numeric) Value of notes still available for merging. \n
              "mergingUTXOs": xxx                 (numeric) Number of UTXOs being merged. \n
              "mergingTransparentValue": xxx      (numeric) Value of UTXOs being merged. \n
              "mergingNotes": xxx                 (numeric) Number of notes being merged. \n
              "mergingShieldedValue": xxx         (numeric) Value of notes being merged. \n
              "opid": xxx          (string) An operationid to pass to z_getoperationstatus to get the result of the operation. \n
            }

        -------------

        docs: https://docs.pirate.black/docs/rpc/z_mergetoaddress/

        :param from_addresses: Required list parameter.
        :param to_address: Required parameter.
        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_mergetoaddress', 'params': [from_addresses, to_address] + args})

    def z_send_many(self, from_address: str, amounts: list, args=None):
        """
        Send multiple times. Amounts are decimal numbers with at most 8 digits of precision. \n
        Change generated from a taddr flows to a new taddr address, while change generated from a zaddr returns to itself. \n
        When sending coinbase UTXOs to a zaddr, change is not allowed. The entire value of the UTXO(s) must be consumed. \n
        Before Sapling activates, the maximum number of zaddr outputs is 54 due to transaction size limits. \n

        ! PRO TIP: memo has to be hex... MEMO_STRING.encode('utf-8').hex()
        -------------

        Arguments:
            1. "fromaddress"         (string, required) The taddr or zaddr to send the funds from.
            2. "amounts"             (array, required) An array of json objects representing the amounts to send.
                [{
                  "address":address  (string, required) The address is a taddr or zaddr
                  "amount":amount    (numeric, required) The numeric amount in ARRR is the value
                  "memo":memo        (string, optional) If the address is a zaddr, raw data represented in hexadecimal string format
                }, ... ]
            3. minconf               (numeric, optional, default=1) Only use funds confirmed at least this many times.
            4. fee                   (numeric, optional, default=0.0001) The fee amount to attach to this transaction.

        Result:
            "operationid"          (string) An operationid to pass to z_getoperationstatus to get the result of the operation.
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_sendmany/

        :param from_address: Required parameter.
        :param amounts: Required list of send to objects as shown under arguments.
        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_sendmany', 'params': [from_address, amounts] + args})

    def z_set_primary_spending_key(self, secret_extended_key: str):
        # TODO: Find out wtf this is :?    ... also the method called in the docs is "z_getnewaddress" hmm
        """
        **DOCUMENTATION TO BE UPDATED**\n
        Set the primary spending key used to create diversified payment addresses. \n
        -------------

        Arguments:
            nah...
        Result:
            Result: Returns True if the spending key was successfully set.
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_setprimaryspendingkey/

        :param secret_extended_key: aka. extended spending key
        :return:
        """
        return self._request(payload={'method': 'z_getnewaddress', 'params': [secret_extended_key]})

    def z_shield_coinbase(self, from_taddr: str, to_zaddrr: str, args=None):
        """
        Shield transparent coinbase funds by sending to a shielded zaddr. \n
        This is an asynchronous operation and utxos selected for shielding will be locked. \n
        If there is an error, they are unlocked. \n
        The RPC call listlockunspent can be used to return a list of locked utxos. \n
        The number of coinbase utxos selected for shielding can be limited by the caller. \n
        If the limit parameter is set to zero, and Overwinter is not yet active, the -mempooltxinputlimit option will determine the number of uxtos. \n
        Any limit is constrained by the consensus rule defining a maximum transaction size of 100000 bytes before Sapling, and 200000 bytes once Sapling activates. \n
        -------------

        Arguments:
            1. "fromaddress"         (string, required) The address is a taddr or "*" for all taddrs belonging to the wallet.
            2. "toaddress"           (string, required) The address is a zaddr.
            3. fee                   (numeric, optional, default=0.0001) The fee amount to attach to this transaction.
            4. limit                 (numeric, optional, default=50) Limit on the maximum number of utxos to shield.  Set to 0 to use node option -mempooltxinputlimit (before Overwinter), or as many as will fit in the transaction (after Overwinter).

        Result:
            {
              "remainingUTXOs": xxx       (numeric) Number of coinbase utxos still available for shielding. \n
              "remainingValue": xxx       (numeric) Value of coinbase utxos still available for shielding. \n
              "shieldingUTXOs": xxx        (numeric) Number of coinbase utxos being shielded. \n
              "shieldingValue": xxx        (numeric) Value of coinbase utxos being shielded. \n
              "opid": xxx          (string) An operationid to pass to z_getoperationstatus to get the result of the operation. \n
            }

        -------------

        docs: https://docs.pirate.black/docs/rpc/z_shieldcoinbase/

        :param from_taddr: Required transparent address.
        :param to_zaddrr: Required shielded z address.
        :param args: Optional parameters.
        :return:
        """
        if args is None: args = []
        if not isinstance(args, list): raise TypeError(f'"args" parameter should be a list of optional parameters. Got {type(args)} instead.')
        return self._request(payload={'method': 'z_shieldcoinbase', 'params': [from_taddr, to_zaddrr, ] + args})

    def z_view_transaction(self, tx_id: str):
        """
        Get detailed shielded information about in-wallet transaction\n
        -------------

        Arguments:
            1. "txid" (string, required) The transaction id

        Result:
            {
              "txid" : "transactionid",   (string) The transaction id
              "spends" : [
                {
                  "type" : "sprout|sapling",      (string) The type of address
                  "js" : n,                       (numeric, sprout) the index of the JSDescription within vJoinSplit
                  "jsSpend" : n,                  (numeric, sprout) the index of the spend within the JSDescription
                  "spend" : n,                    (numeric, sapling) the index of the spend within vShieldedSpend
                  "txidPrev" : "transactionid",   (string) The id for the transaction this note was created in
                  "jsPrev" : n,                   (numeric, sprout) the index of the JSDescription within vJoinSplit
                  "jsOutputPrev" : n,             (numeric, sprout) the index of the output within the JSDescription
                  "outputPrev" : n,               (numeric, sapling) the index of the output within the vShieldedOutput
                  "address" : "zcashaddress",     (string) The Zcash address involved in the transaction
                  "value" : x.xxx                 (numeric) The amount in ARRR
                  "valueZat" : xxxx               (numeric) The amount in arrrtoshis
                }
                ,...
              ],
              "outputs" : [
                {
                  "type" : "sprout|sapling",      (string) The type of address
                  "js" : n,                       (numeric, sprout) the index of the JSDescription within vJoinSplit
                  "jsOutput" : n,                 (numeric, sprout) the index of the output within the JSDescription
                  "output" : n,                   (numeric, sapling) the index of the output within the vShieldedOutput
                  "address" : "zcashaddress",     (string) The Zcash address involved in the transaction
                  "recovered" : true|false        (boolean, sapling) True if the output is not for an address in the wallet
                  "value" : x.xxx                 (numeric) The amount in ARRR
                  "valueZat" : xxxx               (numeric) The amount in arrrtoshis
                  "memo" : "hexmemo",             (string) Hexademical string representation of the memo field
                  "memoStr" : "memo",             (string) Only returned if memo contains valid UTF-8 text.
                }
                ,...
              ],
            }
        -------------

        docs: https://docs.pirate.black/docs/rpc/z_viewtransaction/
        :param tx_id: Required parameter.
        :return:
        """
        return self._request(payload={'method': 'z_viewtransaction', 'params': [tx_id]})

    def backup_wallet(self, destination: str):
        """
        Safely copies wallet.dat to destination filename\n
        -------------

        Arguments:
            1. "destination"   (string, required) The destination filename, saved in the directory set by -exportdir option.

        Result:
            "path"             (string) The full path of the destination file
        -------------

        docs: https://docs.pirate.black/docs/rpc/backupwallet/
        :param destination: Required parameter.
        :return:
        """
        return self._request(payload={'method': 'backupwallet', 'params': [destination]})
