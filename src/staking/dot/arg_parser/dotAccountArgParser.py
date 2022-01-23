from src.staking.dot.fxn_implementations.accountImplementation import AccountImplementation
from common import MyHelpFormatter
from examples import exampleCreateMnemonic, exampleCreateAccount, exampleAccountInfos, exampleCreateKeypair, \
    exampleAccount
from src.staking.dot.argparserUtil import action_help, subcommand, action_mnemonic, action_controller_address


def dotAccountArgParser(parent_parser, coin):
    dotAccountDotParser = parent_parser.add_parser(name="account",
                                                help=f"account interface to {coin}",
                                                epilog=exampleAccount,
                                                formatter_class=MyHelpFormatter)

    dotAccountDotSubParser = dotAccountDotParser.add_subparsers()

    # create mnemonic
    @subcommand(parent=dotAccountDotSubParser, sub_help="create a mnemonic phrase.", epilog=exampleCreateMnemonic,
                optional_args=[action_help()])
    def mnemonic(args):
        AccountImplementation().createMnemonic()

    # create_keypair
    @subcommand(parent=dotAccountDotSubParser, sub_help="create a key pair from seed", epilog=exampleCreateKeypair,
                required_args=[action_mnemonic()],
                optional_args=[action_help()])
    def keypair(args):
        AccountImplementation(mnemonic=args.mnemonic).getAddressFromMnemonic()

    # account_infos
    @subcommand(parent=dotAccountDotSubParser, sub_help="get an account info.", epilog=exampleAccountInfos,
                required_args=[action_controller_address()],
                optional_args=[action_help()])
    def info(args):
        AccountImplementation(ss58_address=args.controller_address).getAllAccountInfo()

    # create_account
    @subcommand(parent=dotAccountDotSubParser, sub_help="create an account.", epilog=exampleCreateAccount,
                optional_args=[action_help()])
    def create(args):
        AccountImplementation().createNewAccount()

    return dotAccountDotParser
