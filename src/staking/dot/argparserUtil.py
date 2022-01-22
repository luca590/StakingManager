from common import MyHelpFormatter


def argument(*name_or_flags, **kwargs):
    return [*name_or_flags], kwargs


def subcommand(parent, sub_help="", epilog="", required_args=None, optional_args=None):
    if required_args is None:
        required_args = []

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__, add_help=False, help=sub_help,
                                   formatter_class=MyHelpFormatter, epilog=epilog)

        required_arguments = parser.add_argument_group('required arguments')
        optional_arguments = parser.add_argument_group('optional arguments')

        for rArg in required_args:
            required_arguments.add_argument(*rArg[0], **rArg[1])
        for oArg in optional_args:
            optional_arguments.add_argument(*oArg[0], **oArg[1])
        parser.set_defaults(func=func)

    return decorator


def actionNumSlashingSpans():
    return argument('-nss',
                    '--num_slashing_spans',
                    help="?",
                    default=0,
                    required=False,
                    type=int)


def actionMnemonic():
    return argument('-m', '--mnemonic',
                    help='mnemonic phrase is a group words, often 12 or more,\ncreated when a new wallet is made.\n''to store your cryptocurrency.\n\n',
                    required=True)


def actionControllerAddress():
    help_string = "An address you would like to bond to the stash account.\n" \
                  "Stash and Controller can be the same address but it is not recommended " \
                  "since it defeats the security of the two-account staking model!\n\n"

    return argument('-ca', '--controller_address',
                    help=help_string,
                    required=True,
                    type=str)


def actionDerivationPath():
    help_string = "The key type and sequence number refer to the segment of the BIP44 derivation path" \
                  "(for example, 0, 1, 2, ...) that is used to derive a private and a public key from the mnemonic!\n\n"

    return argument('-dp', '--derivation_path',
                    help=help_string,
                    required=True,
                    type=str)


def actionNumberOfTokens():
    return argument('-nt', '--number_of_tokens',
                    help='The number of DOT you would like to stake to the network.\n',
                    required=True,
                    type=float)


def actionRewardsDestination():
    help_string = "Choices supports the following:\n" \
                  "staked    - Pay into the stash account, increasing the amount at stake accordingly.\n" \
                  "stash       - Pay into the stash account, not increasing the amount at stake.\n" \
                  "account     - Pay into a custom account, for example: Account DMTHrNcmA8QbqRS4rBq8LXn8ipyczFoNMb1X4cY2WD9tdBX.\n" \
                  "controller  - Pay into the controller account.\n\n"

    return argument('-rd', '--rewards_destination',
                    help=help_string,
                    default="Staked",
                    choices=["Staked", "Stash", "Account", "Controller"],
                    required=False,
                    type=str)


def actionValidatorAddress(activeConfig):
    help_string = "Address of a Polkadot validators (where to stake coins). It can be one or more address.\n" \
                  "By default binance validator address will be chosen.\n\n"

    return argument('-va', '--validator_address',
                    help=help_string,
                    default=activeConfig.activeValidator,
                    nargs="*",
                    required=False,)


def actionHelp():
    return argument("-h",
                    "--help",
                    action="help",
                    help="show this help message and exit")

