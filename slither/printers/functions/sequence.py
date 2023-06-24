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



    def handleFunction(self, function_name, internalFunction, bodyString):
        res = bodyString
        
        for contract in self.contracts:
        
                if function.canonical_name == function_name: # If it's our function
        
                    for node in function.nodes_ordered_dominators: # Review each node
                        
                        res = self.externalCall(node, res, contract.name)
                        res = self.entryPoint(node, res, contract.name, function.name)
                        res = self.storageReads(node, res, contract.name)
                        res = self.storageWrites(node, res, contract.name)
                        res = self.handleInternalFunction(self, internalFunction, res)
        
        return res
    
    def handleInternalFunction(self, function_name, res) :
        
        for contract in self.contracts:
            for function in contract.functions :
                if function.canonical_name == function_name: # If it's our function
                    for node in function.nodes_ordered_dominators: #If it's our node
                        if len(node.internal_calls) > 0: 
                            bodyString = f"{bodyString} \n {contract.name} -> {contract.name}: {node.full_name}" 

    
    
    def storageReads(self, node, bodyString, contract_name):
        res = bodyString
        
        if len(node.state_variables_read) > 0:
            res = f"{res}\nnote over {contract_name}: SLOADs:"
        
            for varRead in node.state_variables_read:
                res = f"{res} \\n   - {varRead.name}"
        
        return res

    def storageWrites(self, node, bodyString, contract_name):
        res = bodyString
        
        if len(node.state_variables_written) > 0:
            res = f"{res} \nnote over {contract_name} #A9DCDF: SSTOREs:"
        
        for varWrite in node.state_variables_written:
            res = f"{res} \\n   - {varWrite.name}"
            
        return res

    
    def entryPoint(self, node, bodyString, contract_name, function_name):
        res = bodyString
        
        if node.type == NodeType.ENTRYPOINT:
            res = f"{res}caller -> {contract_name}: {function_name}"
        
        return res


    def externalCall(self, node, bodyString, contract_name):
        res = bodyString
        
        if len(node.high_level_calls) > 0:
            callee = node.high_level_calls[0][0]
            caller = node.high_level_calls[0][1] 

            if callee.contract_kind == "interface":
                
                for external_function in callee.derived_contracts[0].functions:

                    if external_function.canonical_name == caller.canonical_name:
                        res = f"{res} \n{contract_name} -> {callee.name}: {caller.solidity_signature}"

        return res

    def output(self, filename: str) -> Output:
        
        function_from_args = "UniswapV2Factory.createPair(address,address)"
        internalFunctionTester = "UniswapV2Pair.mint(address)"

        """
        _filename is not used
        Args:
            _filename(string)
            
        """

        pumlStart = "@startuml\n"
        pumlEnd = "\n@enduml"
        participants = "actor caller \n"
        bodyString = ""
        
        info = ""
        all_files = []
        # participants = f"{participants} participant {contract.name} \n"
        
        bodyString = self.handleFunction(function_from_args, internalFunctionTester, bodyString)


        pumlString = f"{pumlStart}{participants}{bodyString}{pumlEnd}"

        if filename:
            rev_function_name = "".join(x for x in function_from_args if x.isalnum())
            new_filename = f"{filename}-{rev_function_name}.puml"
        else:
            new_filename = f"{function_from_args}.puml"

        with open(new_filename, "w", encoding="utf8") as f:
            f.write(pumlString)

        all_files.append((new_filename, pumlString))

        info = f"Export to {new_filename}\n" 
        self.info(info)
        res = self.generate_output(info)
        return res
