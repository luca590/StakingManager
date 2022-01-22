from src.staking.dot.fxn_decorator_implementations.accountImplementation import DotAccountCall
from common import MyHelpFormatter
from examples import exampleCreateMnemonic, exampleCreateAccount, exampleAccountInfos, exampleCreateKeypair, \
    exampleAccount
from src.staking.dot.argparserUtil import actionHelp, subcommand, actionMnemonic, actionControllerAddress


def accountArgParser(parent_parser, coin):
    accountDotParser = parent_parser.add_parser(name="account",
                                                help=f"account interface to {coin}",
                                                epilog=exampleAccount,
                                                formatter_class=MyHelpFormatter)

    accountDotSubParser = accountDotParser.add_subparsers(help='')

    # create mnemonic
    @subcommand(parent=accountDotSubParser, sub_help="create a mnemonic phrase.", epilog=exampleCreateMnemonic,
                optional_args=[actionHelp()])
    def mnemonic(args):
        @DotAccountCall()
        def mnemonic():
            pass

    # create_keypair
    @subcommand(parent=accountDotSubParser, sub_help="create a key pair from seed", epilog=exampleCreateKeypair,
                required_args=[actionMnemonic()],
                optional_args=[actionHelp()])
    def keypair(args):
        @DotAccountCall(mnemonic=args.mnemonic)
        def keypair():
            pass

    # account_infos
    @subcommand(parent=accountDotSubParser, sub_help="get an account info.", epilog=exampleAccountInfos,
                required_args=[actionControllerAddress()],
                optional_args=[actionHelp()])
    def info(args):
        @DotAccountCall(ss58_address=args.controller_address)
        def info():
            pass

    # create_account
    @subcommand(parent=accountDotSubParser, sub_help="create an account.", epilog=exampleCreateAccount,
                optional_args=[actionHelp()])
    def create(args):
        @DotAccountCall()
        def create():
            pass

    return accountDotParser
