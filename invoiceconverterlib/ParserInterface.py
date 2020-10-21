from invoiceconverterlib.InvoiceDocument import InvoiceDocument


class ParserInterface:

    def parse(self, filename: str) -> InvoiceDocument:
        """parse file and create InvoiceDocument object from it"""
        pass

    def test(self, filename: str) -> bool:
        """test if current parser is applicable for the file"""
        return False
