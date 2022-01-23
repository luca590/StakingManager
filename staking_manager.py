import argparse
from logger import logger

from src.staking.cosmos.arg_parser.atomAccountArgParser import atomAccountArgParser
from src.staking.cosmos.arg_parser.atomDelegatorArgParser import atomDelegatorArgParser

from src.staking.dot.arg_parser.dotAccountArgParser import dotAccountArgParser
from src.staking.dot.arg_parser.beforeIStartArgParser import beforeIStartArgParser
from src.staking.dot.arg_parser.dotNominatorArgParser import dotNominatorArgParser
from src.staking.dot.arg_parser.dotBonderArgParser import dotBonderArgParser
from src.staking.dot.arg_parser.dotStakerArgParser import dotStakeDotArgParser
from src.staking.ksm.arg_parser.ksmStakerArgParser import ksmStakeDotArgParser

from src.staking.dot.arg_parser.dotValidatorArgParser import validatorDotArgParser
from src.staking.ksm.arg_parser.ksmBonderArgParser import ksmBonderArgParser
from src.staking.ksm.arg_parser.ksmNominatorArgParser import ksmNominatorArgParser

__name = "staking_manager"
logger = logger(__name)
logger.info("Eulith Staking Program Starting.")

"""
a parser can have 
1 - positional arguments
2 - required arguments 
3 - optional arguments

We arrange functionally into categories using a tree of parsers
- coin
   └─── functionX
    ...
        └─── subFunctionY 
        ...

Example:
topParentParser
└───coinSuppParser
    ├───dotParentParser
    │   └───anotherSuppParser
    │       └───anotherParentParser
    │           └───anotherSuppParser
    ├───solParentParser
    │   ...
    │   └───
    └───xtzParentParser
    │   ...
    │   └───
    ...      
"""

# parent parser (top level arguments parser)
parentParser = argparse.ArgumentParser(prog='staking_manager.py')
stakeCoinSubParsers = parentParser.add_subparsers(help='available staking coins')

# staking coin parsers group
# parent parser for any added coin will be declared here
# naming will be as follow (xCoinParentParser)
dotParentParser = stakeCoinSubParsers.add_parser(name='dot', help='Polkadot staking interface')
ksmParentParser = stakeCoinSubParsers.add_parser(name='ksm', help='Kusama staking interface')
atomParentParser = stakeCoinSubParsers.add_parser(name='atom', help='Cosmos staking interface')

# dot
dotSubParser = dotParentParser.add_subparsers(dest="dot", help='available dot staking commands')
dotAccount = dotAccountArgParser(dotSubParser, "DOT")
dotStaker = dotStakeDotArgParser(dotSubParser)
dotNominator = dotNominatorArgParser(dotSubParser)
dotBonder = dotBonderArgParser(dotSubParser)
dotValidator = validatorDotArgParser(dotSubParser)
guide = beforeIStartArgParser(dotSubParser)

# ksm
ksmSubParser = ksmParentParser.add_subparsers(dest="ksm", help='Available ksm staking commands')
ksmAccount = dotAccountArgParser(dotSubParser, "KSM")
ksmStaker = ksmStakeDotArgParser(ksmSubParser)
ksmNominator = ksmNominatorArgParser(ksmSubParser)
ksmBonder = ksmBonderArgParser(ksmSubParser)
ksmValidator = validatorDotArgParser(ksmSubParser)

# atom
atomSubParser = atomParentParser.add_subparsers(dest="atom", help='Available atom staking commands')
atomAccount = atomAccountArgParser(atomSubParser)
atomDelegator = atomDelegatorArgParser(atomSubParser)

help_map = {
    'dot': {
        'stake': dotStaker,
        'nominator': dotNominator,
        'bonder': dotBonder,
        'account': dotAccount,
        'validator': dotValidator,
        'delegator': None,
        'guide': guide,
        'parent_parser': dotParentParser
    },
    'ksm': {
        'stake': None,
        'nominator': ksmNominator,
        'bonder': ksmBonder,
        'account': ksmAccount,
        'validator': ksmValidator,
        'delegator': None,
        'guide': guide,
        'parent_parser': ksmParentParser
    },
    'atom': {
        'stake': None,
        'nominator': None,
        'bonder': None,
        'account': atomAccount,
        'validator': None,
        'guide': guide,
        'parent_parser': atomParentParser
    }
}


if __name__ == "__main__":
    args = parentParser.parse_args()
    var_args = vars(args)

    for key, val in var_args.items():
        if val:
            if val == "stake":
                try:
                    args.func(args)
                except AttributeError:
                    help_map[key][val].print_help()
            elif val == "nominator":
                try:
                    args.func(args)
                except AttributeError:
                    help_map[key][val].print_help()
            elif val == "bonder":
                try:
                    args.func(args)
                except AttributeError:
                    help_map[key][val].print_help()
            elif val == "account":
                try:
                    args.func(args)
                except AttributeError:
                    help_map[key][val].print_help()
            elif val == "validator":
                pass
            elif val == "guide":
                try:
                    args.func(args)
                except AttributeError:
                    help_map[key][val].print_help()
        else:
            help_map[key]['parent_parser'].print_help()
