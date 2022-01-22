from src.staking.cosmos.fxn_decorator_implementations.transactionImplementation import CosmosCall
from common import MyHelpFormatter
from src.staking.dot.argparserUtil import actionMnemonic, actionNumberOfTokens, actionControllerAddress, \
    actionValidatorAddress, actionHelp, subcommand
from examples import exampleBond, exampleBonder, exampleRebond
from config import cosmosActiveConfig


def atomDelegatorArgParser(parent_parser):
    # delegator
    # delegator parent parser
    delegatorParser = parent_parser.add_parser("delegator", help="delegator interface to Cosmos.", epilog=exampleBonder,
                                               formatter_class=MyHelpFormatter)
    delegatorSubParser = delegatorParser.add_subparsers(help='')

    # delegate
    """
    """

    @subcommand(parent=delegatorSubParser,
                sub_help="Submit delegation to a validator.",
                epilog=exampleBond, required_args=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optional_args=[actionValidatorAddress(cosmosActiveConfig), actionHelp()])
    def delegate(args):
        @CosmosCall(config=cosmosActiveConfig, cli_name="delegator",
                    call_params={'controller': args.controller_address, 'value': args.number_of_tokens},
                    mnemonic=args.mnemonic)
        def delegate():
            pass

    # unbonding_delegations
    """
    """

    @subcommand(parent=delegatorSubParser,
                sub_help="stop delegation.",
                epilog=exampleBond, required_args=[actionMnemonic(), actionNumberOfTokens()],
                optional_args=[actionHelp()])
    def unbonding_delegations(args):
        @CosmosCall(config=cosmosActiveConfig, cli_name="delegator",
                    call_params={'value': args.number_of_tokens}, mnemonic=args.mnemonic)
        def unbonding_delegations():
            """
            """
            pass

    # redelegations
    """
    """

    @subcommand(parent=delegatorSubParser,
                sub_help="redelegations a portion of the stash scheduled to be unlocked.",
                epilog=exampleRebond, required_args=[actionMnemonic(), actionNumberOfTokens()],
                optional_args=[actionValidatorAddress(cosmosActiveConfig), actionHelp()])
    def redelegations(args):
        @CosmosCall(config=cosmosActiveConfig, cli_name="delegator",
                    call_params={'value': args.number_of_tokens}, mnemonic=args.mnemonic)
        def redelegations():
            pass

    return delegatorParser
