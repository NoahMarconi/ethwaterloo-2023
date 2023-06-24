import argparse
import logging
import sys
from slither.core.cfg.node import NodeType

from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.output import Output


class Sequence(AbstractPrinter):

    ARGUMENT = "sequence"
    HELP = "Export a sequence diagram of a function"

    WIKI = "www.example.com"

    def output(self, filename: str) -> Output:
        
        functionName = "UniswapV2Factory.createPair(address,address)"
        testingInternalFunctionCaller = "UniswapV2Pair.mint(address)"
        """
        _filename is not used
        Args:
            _filename(string)
            
        """

        pumlStart = "@startuml\n"
        pumlEnd = "\n@enduml"
        participants = "actor caller \n"
        bodystring = ""
        
        info = ""
        all_files = []
        for contract in self.contracts:  # type: ignore
            participants = f"{participants} participant {contract.name} \n"
            for function in contract.functions :
                if function.canonical_name == testingInternalFunctionCaller: # If it's our function
                    for node in function.nodes_ordered_dominators: #If it's our node
                        if len(node.internal_calls) > 0: 
                            bodystring = f"{bodystring} \n {contract.name} -> {contract.name}: {node.full_name}" 


                if function.canonical_name == functionName: # If it's our function
                    for node in function.nodes_ordered_dominators: # Review each node
                        if node.type == NodeType.ENTRYPOINT:
                            bodystring = f"{bodystring} caller -> {contract.name}: {function.name}"
                        if len(node.state_variables_read) > 0:
                            bodystring = f"{bodystring} \n note over {contract.name}: SLOADS:"
                        for varRead in node.state_variables_read:
                            bodystring = f"{bodystring} \\n   - {varRead.name}"
                            print(node)
                        if len(node.state_variables_written) > 0:
                            bodystring = f"{bodystring} \n note over {contract.name}: SSTORE:"
                        for varWrite in node.state_variables_written:
                            bodystring = f"{bodystring} \\n   - {varWrite.name}"
                            print(node)
        pumlString = f"{pumlStart} {participants} {bodystring} {pumlEnd}"

        if filename:
            rev_function_name = "".join(x for x in functionName if x.isalnum())
            new_filename = f"{filename}-{rev_function_name}.puml"
        else:
            new_filename = f"{functionName}.puml"

        with open(new_filename, "w", encoding="utf8") as f:
            f.write(pumlString)

        all_files.append((new_filename, pumlString))

        info = f"Export to {new_filename}\n" 
        self.info(info)
        res = self.generate_output(info)
        return res
