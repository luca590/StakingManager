from src.staking.dot.argparserUtil import action_mnemonic, action_number_of_tokens, action_controller_address, \
    action_rewards_destination, action_validator_address, action_help, subcommand
from src.staking.dot.fxn_implementations.substrateCallImplementation import \
    SubstrateCall
from config import DotActiveConfig
from examples import exampleStaker


def dotStakeDotArgParser(parent_parser):
    @subcommand(parent=parent_parser,
                sub_help="automatically prepare coins and send them to be staked "
                         "(bond coin then nominate a validator).",
                epilog=exampleStaker,
                required_args=[action_mnemonic(), action_controller_address(), action_number_of_tokens()],
                optional_args=[action_rewards_destination(), action_validator_address(DotActiveConfig), action_help()])
    def stake(args):
        SubstrateCall(cli_name="Bonder",
                      call_module="Staking",
                      call_params={'controller': args.controller_address, 'value': args.number_of_tokens,
                                   'payee': args.rewards_destination, 'targets': args.validator_address},
                      seed=args.mnemonic).stake()
