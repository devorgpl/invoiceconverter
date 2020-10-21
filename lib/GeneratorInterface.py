from lib.InvoiceDocument import InvoiceDocument


class GeneratorInterface:
    def generate(self, document: InvoiceDocument, filename: str) -> None:
        """generate a file from InvoiceDocument object"""
        pass
