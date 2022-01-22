from src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import SubstrateCall
from common import MyHelpFormatter
from src.staking.dot.argparserUtil import actionMnemonic, actionValidatorAddress, actionHelp, \
    subcommand, actionNumberOfTokens
from config import DotActiveConfig
from examples import exampleNominator, exampleNominate, exampleUnnominateTmp, exampleUnnominateAll


def dotNominatorArgParser(parser_parent):
    nominatorParser = parser_parent.add_parser(name="nominator", help="""nomination interface to DOT.""",
                                               add_help=False, epilog=exampleNominator,
                                               formatter_class=MyHelpFormatter)
    nominatorSubParser = nominatorParser.add_subparsers(help='')

    # nominate
    @subcommand(parent=nominatorSubParser, sub_help=exampleNominate, required_args=[actionMnemonic()],
                optional_args=[actionValidatorAddress(DotActiveConfig), actionHelp()])
    def nominate(args):
        SubstrateCall(config=DotActiveConfig,
                      cli_name="Nominator",
                      call_module="Staking",
                      call_params={'targets': args.validator_address},
                      seed=args.mnemonic).handle_call('nominate')

    # chill
    # https://githubhelp.com/polkascan/py-scale-codec
    # Stakers can be in any one of the three states: validating, nominating, or chilling. When a staker wants to
    # temporarily pause their active engagement in staking but does not want to unbond their funds, they can choose
    # to "chill" their involvement and keep their funds staked.
    # so in fact to totally unstacked all the coin you need to chill and then unbound
    # https://wiki.polkadot.network/docs/maintain-guides-how-to-chill
    @subcommand(parent=nominatorSubParser, sub_help=exampleUnnominateTmp, required_args=[actionMnemonic()],
                optional_args=[actionHelp()])
    def stop_nominate_tmp(args):
        SubstrateCall(cli_name="Nominator",
                      call_module="Staking",
                      call_params={},
                      seed=args.mnemonic).handle_call('chill')

    @subcommand(parent=nominatorSubParser, sub_help=exampleUnnominateAll,
                required_args=[actionMnemonic(), actionNumberOfTokens()],
                optional_args=[actionHelp()])
    def stop_nominate_all(args):
        SubstrateCall(cli_name="Nominator",
                      call_module="Staking",
                      call_params={'value': args.number_of_tokens},
                      seed=args.mnemonic).stop_nominate_all()

    return nominatorParser
