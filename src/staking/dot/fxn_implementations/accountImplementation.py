import sys
from config import DotActiveConfig
from logger import logger
from src.staking.dot.fxn_implementations.accountImplementationUtils import *


class AccountImplementation:
    """
    AccountImplementation is a class for containing functions related to accounts.
    An "account" is defined as keypair with associated data.

    AccountImplementation also serves as a kind of interface for all functions outside accountImplementation.py and
    accountImplementationUtils.py to have 1 reference point for 'account' related functions. 
    Any classes/functions outside accountImplementation.py and accountImplementationUtils.py should not need to 
    directly refer to any code in accountImplementationUtils.py

    Therefore, some of the functions in AccountImplementation are "redundant", e.g. 
    createMnemonic just calls MnemonicImplementation in accountImplementationUtils.py
    """

    def __init__(self, mnemonic="", ss58_address=""):
        self.cli_name = "Accounting"
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address
        self.logger = logger(self.cli_name)
        self.logger.info(f"Start {self.cli_name} Program")
        self.activeConfig = DotActiveConfig

    def createNewAccount(self):
        # MnemonicImplementation is called here instead of self.createMnemonic() because it's better
        # for functions in the AccountImplementation class to directly call the implementation classes
        newMnemonic = MnemonicImplementation(self.logger).createMnemonic()
        createAccountKeyPair = KeyPairImplementation(self.activeConfig, self.logger,
                                                     newMnemonic).getAddressFromMnemonic()
        # check if mnemonic is created if this pass keypair will pass without errors
        if not createAccountKeyPair:
            return False
        return True

    def createMnemonic(self):
        newMnemonic = MnemonicImplementation(self.logger).createMnemonic()
        return newMnemonic

    def getAddressFromMnemonic(self):
        address = KeyPairImplementation(self.activeConfig, self.logger, self.mnemonic).getAddressFromMnemonic()
        return address

    def getAllAccountInfo(self):
        try:
            value = self.activeConfig.activeSubstrate.query('System', 'Account', params=[self.ss58_address]).value
            fee_frozen = int(value['data']['fee_frozen']) / self.activeConfig.coinDecimalPlaces
            free = int(value['data']['free']) / self.activeConfig.coinDecimalPlaces
            reserved = int(value['data']['reserved']) / self.activeConfig.coinDecimalPlaces
            misc_frozen = int(value['data']['misc_frozen']) / self.activeConfig.coinDecimalPlaces

            self.logger.info(f"""account {self.ss58_address} infos

            nonce : {value['nonce']}
            consumers : {value['consumers']}
            providers : {value['providers']}
            sufficients : {value['sufficients']}
            free : {free} {self.activeConfig.coinName}
            reserved : {reserved} {self.activeConfig.coinName}
            misc_frozen : {misc_frozen} {self.activeConfig.coinName}
            fee_frozen : {fee_frozen} {self.activeConfig.coinName}
            """)
        except Exception as e:
            self.logger.error(f"{e}")

    def getAccountBalance(self, purpose=None):
        if purpose is None:
            # TODO: improve this to return dictionary with account values
            self.getAllAccountInfo()
        elif purpose == "bonding":
            return AccountBalanceForBonding(self.activeConfig, self.logger,
                                            self.ss58_address).getAccountBalanceForBonding()
        else:
            self.logger.warning(f"Unknown object passed into getAccountBalance. Failing.")
            sys.exit(0)

