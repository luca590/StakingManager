from src.staking.dot.fxn_implementations.substrateCallImplementation import SubstrateCall
from common import MyHelpFormatter
from src.staking.dot.argparserUtil import actionMnemonic, actionNumberOfTokens, \
    actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand, actionNumSlashingSpans
from examples import exampleBond, exampleBonder, exampleBondExtra, exampleRebond, exampleWithdrawUnBonded
from config import DotActiveConfig


def dotBonderArgParser(parent_parser):
    bonderParser = parent_parser.add_parser("bonder",
                                            help="bond interface to DOT.",
                                            epilog=exampleBonder,
                                            formatter_class=MyHelpFormatter)

    bonderSubParser = bonderParser.add_subparsers()

    @subcommand(parent=bonderSubParser,
                sub_help="Take the origin account as a stash and lock up `value` of its balance. "
                         "`controller` will be the account that controls it.",
                epilog=exampleBond,
                required_args=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optional_args=[actionRewardsDestination(), actionValidatorAddress(DotActiveConfig), actionHelp()])
    def bond(args):
        SubstrateCall(cli_name="bonder",
                      call_module="Staking",
                      call_params={'controller': args.controller_address,
                                   'value': args.number_of_tokens,
                                   'payee': args.rewards_destination},
                      seed=args.mnemonic).bond()

    @subcommand(parent=bonderSubParser,
                sub_help="Schedule a portion of the stash to be "
                         "unlocked ready for transfer out after the bond period ends.",
                epilog=exampleBond, required_args=[actionMnemonic(), actionNumberOfTokens()],
                optional_args=[actionHelp()])
    def unbond(args):
        SubstrateCall(cli_name="bonder",
                      call_module="Staking",
                      call_params={'value': args.number_of_tokens},
                      seed=args.mnemonic).handle_call('unbond')

    @subcommand(parent=bonderSubParser,
                sub_help="Rebond a portion of the stash scheduled to be unlocked.",
                epilog=exampleRebond,
                required_args=[actionMnemonic(), actionNumberOfTokens()],
                optional_args=[actionRewardsDestination(), actionValidatorAddress(DotActiveConfig), actionHelp()])
    def rebond(args):
        SubstrateCall(cli_name="bonder",
                      call_module="Staking",
                      call_params={'value': args.number_of_tokens},
                      seed=args.mnemonic).handle_call('rebond')

    @subcommand(parent=bonderSubParser,
                sub_help="Add some extra amount that have appeared in "
                         "the stash `free_balance` into the balance up for staking.",
                epilog=exampleBondExtra,
                required_args=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optional_args=[actionRewardsDestination(), actionValidatorAddress(DotActiveConfig), actionHelp()])
    def bondextra(args):
        SubstrateCall(cli_name="bonder",
                      call_module="Staking",
                      call_params={'value': args.number_of_tokens, 'controller': args.controller_address},
                      seed=args.mnemonic).bond_extra()

    @subcommand(parent=bonderSubParser,
                sub_help="Remove any unlocked chunks from the `unlocking` queue. "
                         "This essentially frees up that balance to be used "
                         "by the stash account to do whatever it wants.",
                epilog=exampleWithdrawUnBonded,
                required_args=[actionMnemonic(), actionNumSlashingSpans()],
                optional_args=[actionHelp()])
    def withdrawunbonded(args):
        SubstrateCall(cli_name="bonder",
                      call_module="Staking",
                      call_params={'num_slashing_spans': args.num_slashing_spans},
                      seed=args.mnemonic).handle_call('withdraw_unbonded')

    return bonderParser
