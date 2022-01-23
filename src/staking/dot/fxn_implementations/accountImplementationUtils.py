from bip39 import bip39_validate
from substrateinterface import Keypair


class MnemonicImplementation:
    """
    Class creates a mnemonic and prints in the log, currently has no other purpose
    * For security reasons, do not store the mnemonics
    * This class is intentionally separate from AccountImplementation as there may be times
    when features of mnemonics should be added/changed without concerning AccountImplementation
    """
    def __init__(self, logger):
        self.logger = logger

    def create_mnemonic(self):
        mnemonic = Keypair.generate_mnemonic()
        create_mnemonic_log_message = f"New mnemonic phrase: {mnemonic}\n" \
                                      f"NOTE: Please write down this mnemonic on paper and store in a safe place.\n" \
                                      f"Learn more about mnemonic: \n" \
                                      f"https://coinmarketcap.com/alexandria/glossary/mnemonic-phrase"
        try:
            self.logger.info(create_mnemonic_log_message)
            return mnemonic
        except Exception as e:
            self.logger.critical(f"Error : {e}")
            return False


class KeyPairImplementation:
    def __init__(self, config, logger, mnemonic):
        self.activeConfig = config
        self.logger = logger
        self.mnemonic = mnemonic

    def get_address_from_mnemonic(self):
        """
        Calculates the dot address given a mnemonic and prints and returns it (or exits the system if it fails).
        """
        invalid_characters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

        if len(self.mnemonic.split(' ')) < 10:
            self.logger.critical("A bad mnemonic as been passed to create the keypair")
            return False

        try:
            # Keypair ~ https://github.com/polkascan/py-substrate-interface#keypair-creation-and-signing
            key = Keypair.create_from_mnemonic(mnemonic=self.mnemonic, ss58_format=self.activeConfig.ss58_format)
            self.logger.info(f"Here is the address associated with the above mnemonic:\n {key}")

            # Verify key works
            if key.verify("This is a test message", key.sign("This is a test message")):
                return key
            else:
                self.logger.critical("DO NOT USE KEY. KEY INCORRECTLY GENERATED")
                return False
        except ValueError:
            split_mnemonic = self.mnemonic.split(" ")
            length_mnemonic = len(split_mnemonic)

            # check word length and special character
            invalid_length_word = any(word for word in split_mnemonic if len(word) < 3 or len(word) > 8)
            invalid_char_word = any(s for s in self.mnemonic if s in invalid_characters)

            if length_mnemonic not in [12, 15, 18, 21, 24]:
                self.logger.critical(f"Mnemonic must have length: [12, 15, 18, 21, 24]. Actual: {length_mnemonic}")
                return False
            else:
                if invalid_char_word:
                    self.logger.critical(f"Mnemonic words must only contain letters. Actual: {self.mnemonic}")
                    return False
                elif invalid_length_word or not bip39_validate(self.mnemonic):
                    self.logger.critical(f"Mnemonic words must be between 3 and 8 chars. Actual: {self.mnemonic}")
                    return False


class AccountBalanceForBonding:
    def __init__(self, config, logger, ss58_address):
        self.activeConfig = config
        self.logger = logger
        self.ss58_address = ss58_address

    def __call__(self):
        return self.get_account_balance_for_bonding()

    def get_account_balance_for_bonding(self):
        account_balance_info = self.activeConfig.activeSubstrate\
            .query('System', 'Account', params=[self.ss58_address]).value

        # In general, the usable balance of the account is the amount that is free minus any funds that are considered
        # frozen (either misc_frozen or fee_frozen). It depends on the reason for which the funds are to be used.
        # If the funds are to be used for transfers, then the usable amount is the free amount minus
        # any misc_frozen funds. However, if the funds are to be used to pay transaction fees,
        # the usable amount would be the free funds minus fee_frozen.
        # explained: https://wiki.polkadot.network/docs/learn-accounts#balance-types

        free = account_balance_info['data']['free']

        misc_frozen = account_balance_info['data']['misc_frozen']
        total_account_balance = (free - misc_frozen) / self.activeConfig.coinDecimalPlaces

        return total_account_balance
