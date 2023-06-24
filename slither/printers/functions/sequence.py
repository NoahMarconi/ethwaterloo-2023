from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.output import Output


class Sequence(AbstractPrinter):

    ARGUMENT = "sequence"
    HELP = "Export a sequence diagram of a function"

    WIKI = "www.example.com"

    def output(self, filename: str) -> Output:
        """
        _filename is not used
        Args:
            _filename(string)
        """

        info = ""
        all_files = []
        for contract in self.contracts:  # type: ignore
            for function in contract.functions + list(contract.modifiers):
                print(function)

        self.info(info)

        res = self.generate_output(info)
        return res
