from src.staking.dot.argparserUtil import action_help, subcommand
from examples import exampleGuide
from logger import logger


def beforeIStartArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                sub_help="Get most helpfull tips abount polkadot protocol and staking.",
                epilog=exampleGuide,
                optional_args=[action_help()])
    def guide(args):
        userGuide = "Polkadot staking notes\n" \
                    "- Nominating currently requires a minimum of 120 DOT staked funds on Polkadot.\n" \
                    "- Nominating currently requires a minimum of 120 DOT staked funds on Polkadot.\n" \
                    "- On the Polkadot network, an address is only active when it holds a minimum amount, " \
                    "currently set at 1 DOT.\n" \
                    "- If an account drops below the ED, the account is reaped (“deactivated”) " \
                    "and any remaining funds are destroyed." \
                    "- If an account is already bonded the use of bond command will be not needed else use (bondextra)"

        logger("Guide").info(userGuide)
