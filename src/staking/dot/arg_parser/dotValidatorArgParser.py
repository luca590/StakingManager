from src.staking.dot.argparserUtil import action_help, subcommand


# TODO https://support.polkadot.network/support/solutions/articles/65000150130-how-do-i-know-which-validators-to-choose-
def validatorDotArgParser(parent_parser):
    @subcommand(parent=parent_parser,
                sub_help="Get a list of validator that meet polkadot requirements.",
                optional_args=[action_help()])
    def validator(args):
        # TODO Implement
        pass
