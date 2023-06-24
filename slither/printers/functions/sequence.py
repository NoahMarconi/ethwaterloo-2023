import argparse
import logging
import sys

from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.output import Output

def parse_args() -> argparse.Namespace:
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(
        description="Contracts flattening. See https://github.com/crytic/slither/wiki/Contract-Flattening",
        usage="slither-flat filename",
    )

    parser.add_argument("filename", help="The filename of the contract or project to analyze.")

    parser.add_argument("--function", help="The function to diagram.", default=None)


    group_export = parser.add_argument_group("Export options")

    group_export.add_argument(
        "--dir",
        help=f"Export directory (default: {DEFAULT_EXPORT_PATH}).",
        default=None,
    )

    group_export.add_argument(
        "--json",
        help='Export the results as a JSON file ("--json -" to export to stdout)',
        action="store",
        default=None,
    )

    parser.add_argument(
        "--zip",
        help="Export all the files to a zip file",
        action="store",
        default=None,
    )

    parser.add_argument(
        "--zip-type",
        help=f"Zip compression type. One of {','.join(ZIP_TYPES_ACCEPTED.keys())}. Default lzma",
        action="store",
        default=None,
    )

    group_patching = parser.add_argument_group("Patching options")

    group_patching.add_argument(
        "--convert-external", help="Convert external to public.", action="store_true"
    )

    group_patching.add_argument(
        "--convert-private",
        help="Convert private variables to internal.",
        action="store_true",
    )

    group_patching.add_argument(
        "--convert-library-to-internal",
        help="Convert external or public functions to internal in library.",
        action="store_true",
    )

    group_patching.add_argument(
        "--remove-assert", help="Remove call to assert().", action="store_true"
    )

    group_patching.add_argument(
        "--pragma-solidity",
        help="Set the solidity pragma with a given version.",
        action="store",
        default=None,
    )

    # Add default arguments from crytic-compile
    cryticparser.init(parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()



class Sequence(AbstractPrinter):

    ARGUMENT = "sequence"
    HELP = "Export a sequence diagram of a function"

    WIKI = "www.example.com"

    def output(self, filename: str) -> Output:
        
        functionName = "UniswapV2Factory.createPair(address,address)"
        """
        _filename is not used
        Args:
            _filename(string)
            
        """

        info = ""
        all_files = []
        for contract in self.contracts:  # type: ignore
            for function in contract.functions :
                if function.canonical_name == functionName:
                    print(function)


        self.info(info)

        res = self.generate_output(info)
        return res
