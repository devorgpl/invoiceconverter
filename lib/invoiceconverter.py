import logging

from lib import ParserInterface, InvoiceDocument, GeneratorInterface
from lib.generators.InsertEppGenerator import InsertEppGenerator
from lib.parsers.ComarchXmlParser import ComarchXmlParser
from lib.parsers.OptimaXmlParser import OptimaXmlParser
from lib.parsers.UblXmlParser import UblXmlParser
from lib.parsers.XlsxInvoiceParser import XlsxInvoiceParser


def ffind_format_parser(filename):
    parsers: [ParserInterface] = [
        ComarchXmlParser(),
        XlsxInvoiceParser(),
        UblXmlParser(),
        OptimaXmlParser(),
    ]
    logging.debug("Available parsers: %s", str(parsers))
    found = next(filter(lambda x: x.test(filename), parsers), None)
    logging.debug("For file=%s found parser=%s", filename, found)
    return found


def fget_invoice(filename, parser):
    invoice_obj: InvoiceDocument = parser.parse(filename)
    return invoice_obj


def fgenerate_epp(filename, invoice_obj):
    generator: GeneratorInterface = InsertEppGenerator()
    generator.generate(invoice_obj, filename + ".epp")
