from src.staking.dot.argparserUtil import actionHelp, subcommand
from src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import SubstrateCall

from examples import exampleStaker


# TODO https://support.polkadot.network/support/solutions/articles/65000150130-how-do-i-know-which-validators-to-choose-
def validatorDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                sub_help="Get a list of validator that meat polkadot requirements.",
                epilog=exampleStaker, required_args=[],
                optional_args=[actionHelp()])
    def validator(args):
        @SubstrateCall()
        def check():
            pass
