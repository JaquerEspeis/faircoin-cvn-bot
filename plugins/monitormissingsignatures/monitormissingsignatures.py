import os

import errbot

from bitcoinrpc import authproxy


_GROUP_FAIRCOIN_CVN_OPERATORS= '-114923528'
_POLL_FREQUENCY = 180  # 3 minutes.
_FAIRCOIN_RPC_URL = 'http://{}:{}@127.0.0.1:40405'
_CVN_OPERATORS = {
    '0x0b4e533d': '@piki46',
    '0x0da3c0e0': '@elopio',
    '0x59e0a12e': '@santiddt',
    '0x86d6cdb7': '@altjensen',
    '0xae5fae5c': '@mmoya',
    '0xaffeaffe': '@ariemer',
    '0xbabd15bd': '@luiski',
    '0xc01dbee1': '@yosug',
    '0xc1cad1da': '@Michalis_K',
    '0xca0dcaa2': '@northcountry',
    '0xd4b69c97': '@s8t8f',
    '0xdabbad00': '@jbarrio',
    '0xe2f3ada2': '@zumbrunn',
    '0xe215f05c': '@prgiorgio',
    '0xf7a69180': '@IvanVdC',
    '0x2d3d4a04': '@chrkon00',
    '0xd4b69c97': '@s8t8f',
    '0x9c1a6161': '@elmanytas',
    '0xa0a748eb': '@rasobar'
    '0xcafecafe': '@thokon00'
}


class MonitorMissingSignatures(errbot.BotPlugin):

    def activate(self):
        super().activate()
        self['latest_block_hash'] = 0
        self['missing_count'] = {}
        self.start_poller(_POLL_FREQUENCY, self._report_missing_signatures)

    def _report_missing_signatures(self):
        latest_block_hash = self._get_latest_block_hash()
        if latest_block_hash != self['latest_block_hash']:
            self['latest_block_hash'] = latest_block_hash

            missing_signatures = self._get_missing_signatures(
                latest_block_hash)
            self._update_missing_count(missing_signatures)

    def _get_latest_block_hash(self):
        rpc_connection = self._get_rpc_connection()
        return rpc_connection.getbestblockhash()

    def _get_missing_signatures(self, block_hash):
        rpc_connection = self._get_rpc_connection()
        missing_signatures = rpc_connection.getblock(
            block_hash)['missingCreatorIds']
        if missing_signatures:
            self._debug('Block {} is missing signatures from {}'.format(
                block_hash, missing_signatures))

        return missing_signatures

    def _get_rpc_connection(self):
        # XXX it seems that the connection is not kept alive.
        return authproxy.AuthServiceProxy(
            _FAIRCOIN_RPC_URL.format(
                os.environ.get('FAIRCOIN_RPC_USER'),
                os.environ.get('FAIRCOIN_RPC_PASSWORD')))

    def _update_missing_count(self, missing_signatures):
        # Reset the count for signatures that are no longer missing.
        for signature in self['missing_count']:
            if signature not in missing_signatures:
                with self.mutable('missing_count') as missing_count:
                    missing_count[signature] = 0

        for signature in missing_signatures:
            count = self['missing_count'].get(signature, 0)
            with self.mutable('missing_count') as missing_count:
                missing_count[signature] = count + 1

            self._debug('New missing count: {} - {}.'.format(
                signature, self['missing_count'][signature]))

            # 5 missing signatures in a row.
            if missing_count[signature] == 5:
                group = self.build_identifier(_GROUP_FAIRCOIN_CVN_OPERATORS)
                message = '{}: your node is down.'.format(
                    _CVN_OPERATORS.get(signature, signature))
                self.send(group, message)

    def _debug(self, message):
        elopio = self.build_identifier('43624396')
        return self.send(elopio, message)
