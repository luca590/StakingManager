from src.staking.dot.argparserUtil import actionMnemonic, actionNumberOfTokens, \
    actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand
from src.staking.dot.fxn_implementations.substrateCallImplementation import \
    SubstrateCall
from config import kusamaActiveConfig

from examples import exampleStaker


def ksmStakeDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                sub_help="automatically prepare coins and send them to be staked (bond coin then nominate a validator).",
                epilog=exampleStaker, required_args=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optional_args=[actionRewardsDestination(), actionValidatorAddress(kusamaActiveConfig), actionHelp()])
    def stake(args):
        @SubstrateCall(config=kusamaActiveConfig, cli_name="Bounder", call_module="Staking",
                       call_params={'controller': args.controller_address, 'value': args.number_of_tokens,
                                    'payee': args.rewards_destination, 'targets': args.validator_address},
                       seed=args.mnemonic)
        def stake():
            pass
