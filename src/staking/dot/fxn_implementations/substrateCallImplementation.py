from src.staking.dot.fxn_implementations.substrateCallImplementationUtils import *
from src.staking.dot.fxn_implementations.accountImplementation import *
from substrateinterface import ExtrinsicReceipt
from config import dotModulesErrors, DotActiveConfig
from substrateinterface.exceptions import SubstrateRequestException

from logger import logger


class SubstrateCall:
    def __init__(self, cli_name, call_module, call_params, seed):
        self.activeConfig = DotActiveConfig
        self.call_module = call_module
        self.call_params = call_params
        self.seed = seed
        self.logger = logger(cli_name)
        self.logger.info("Start %s Program." % cli_name)

        try:
            self.call_params['value'] = self.call_params['value'] * self.activeConfig.coinDecimalPlaces
        except KeyError:
            pass

    def error_handler(self, extrinsic_hash, block_hash, logger):
        errors = set()
        receipt = ExtrinsicReceipt(
            substrate=self.activeConfig.activeSubstrate,
            extrinsic_hash=extrinsic_hash,
            block_hash=block_hash
        )
        for event in receipt.triggered_events:

            event_value = event.value
            if event_value['event']['event_id'] == "ExtrinsicFailed":
                error_module = event_value['attributes'][0]['Module']
                error_module_index = error_module[0]
                error_module_message_index = error_module[1]
                errors.add(dotModulesErrors[str(error_module_index)][str(error_module_message_index)])

        for err in errors:
            logger.error(f"{err}")

    def call(self, call):
        this_address = AccountImplementation(mnemonic=self.seed).getAddressFromMnemonic()
        extrinsic = self.activeConfig.activeSubstrate.create_signed_extrinsic(call=call, keypair=this_address)
        try:
            receipt = self.activeConfig.activeSubstrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
            if receipt.is_success:
                self.logger.info(f"Extrinsic {receipt.extrinsic_hash} sent and included in block {receipt.block_hash}")
            else:
                self.error_handler(receipt.extrinsic_hash, receipt.block_hash, self.logger)
        except SubstrateRequestException as e:
            arg = e.args[0]
            try:
                self.logger.error(f"{arg['message']} : {arg['data']}")
                self.__exit__()
            except KeyError:
                if arg['message'] == "Transaction is temporarily banned":
                    error_message = "The tx is already in pool. " \
                                    "Either try on a different node, " \
                                    "or wait to see if the initial transaction goes through."
                    self.logger.error(error_message)
                    self.__exit__()
                else:
                    self.logger.error(f"{arg['message']}")
                    self.__exit__()

    def bond(self):
        self.logger.info("Execute bond function")
        bond_validator = BondingValidator(config=self.activeConfig,
                                          logger=self.logger,
                                          ss58_address=self.call_params['controller'],
                                          token_number=self.call_params['value'])
        bond_validator.validate_account_data_before_bonding()

        call_bond = self.activeConfig.activeSubstrate.compose_call(
            call_module=f"{self.call_module}",
            call_function="bond",
            call_params=self.call_params
        )
        self.call(call_bond)

        self.__exit__()

    def bond_extra(self):
        self.call_params['max_additional'] = self.call_params['value'] * self.activeConfig.coinDecimalPlaces
        bond_validator = BondingValidator(config=self.activeConfig, logger=self.logger,
                                         ss58_address=self.call_params['controller'],
                                         token_number=self.call_params['max_additional'])

        bond_validator.validate_account_data_before_bonding()

        del self.call_params['controller']

        self.__exit__()

    def stop_nominate_all(self):
        call_chill = self.activeConfig.activeSubstrate.compose_call(
            call_module=self.call_module,
            call_function="chill",
            call_params={})

        call_unbond = self.activeConfig.activeSubstrate.compose_call(
            call_module=self.call_module,
            call_function="unbond",
            call_params=self.call_params
        )

        self.call(call_chill)
        self.call(call_unbond)

        self.__exit__()

    def stake(self):
        call_params_bond = {'controller': self.call_params['controller'],
                            'value': self.call_params['value'],
                            'payee': self.call_params['payee']}

        call_bond = self.activeConfig.activeSubstrate.compose_call(
            call_module=self.call_module,
            call_function="bond",
            call_params=call_params_bond
        )
        call_params_nominate = {'targets': self.call_params['targets']}

        call_nominate = self.activeConfig.activeSubstrate.compose_call(
            call_module=self.call_module,
            call_function="nominate",
            call_params=call_params_nominate
        )

        self.call(call_bond)
        self.call(call_nominate)

        self.__exit__()

    def handle_call(self, call_function):
        call = self.activeConfig.activeSubstrate.compose_call(
            call_module=self.call_module,
            call_function=call_function,
            call_params=self.call_params
        )
        self.call(call)
        self.__exit__()

    def __exit__(self):
        self.activeConfig.activeSubstrate.close()
        sys.exit(0)
