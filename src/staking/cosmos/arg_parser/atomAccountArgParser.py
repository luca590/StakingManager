from src.staking.cosmos.fxn_decorator_implementations.accountImplementation import AtomAccountCall
from common import MyHelpFormatter
from examples import exampleAccount, exampleAccountInfos, exampleCreateAccount
from src.staking.dot.argparserUtil import actionHelp, subcommand, actionMnemonic, \
    actionControllerAddress, actionDerivationPath


def atomAccountArgParser(parent_parser):
    # bounder parent parser
    accountAtomParser = parent_parser.add_parser(name="account",
                                                 help=f"account interface to Cosmos.",
                                                 add_help=False, epilog=exampleAccount,
                                                 formatter_class=MyHelpFormatter)

    accountAtomSubParser = accountAtomParser.add_subparsers(help='')

    # account_infos
    @subcommand(parent=accountAtomSubParser, sub_help="get an account info.", epilog=exampleAccountInfos,
                required_args=[actionControllerAddress()],
                optional_args=[actionHelp()])
    def info(args):
        @AtomAccountCall(address=args.controller_address)
        def info():
            pass

    # create_account
    @subcommand(parent=accountAtomSubParser, sub_help="create an account.", epilog=exampleCreateAccount,
                optional_args=[actionHelp()])
    def create(args):
        @AtomAccountCall()
        def create():
            pass

    @subcommand(parent=accountAtomSubParser, sub_help="create an account.", epilog=exampleCreateAccount,
                required_args=[actionMnemonic(), actionDerivationPath()],
                optional_args=[actionHelp()])
    def keypair(args):
        @AtomAccountCall(mnemonic=args.mnemonic, derivation_path=args.derivation_path)
        def keypair():
            pass

    return accountAtomParser
