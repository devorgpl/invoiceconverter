from xml.dom.minidom import parse, Element

from invoiceconverterlib.InvoiceDocument import InvoiceDocument, InvoiceHeader, InvoiceParty, InvoiceLine
from invoiceconverterlib.ParserInterface import ParserInterface
from invoiceconverterlib.utils.XmlUtil import xmlExtractText, xmlExtractDate

"""TODO: unfinished parser"""


class UblXmlParser(ParserInterface):

    def test(self, filename: str) -> bool:
        if not filename.endswith('.xml'):
            return False
        doc = parse(filename)
        return len(doc.getElementsByTagName("cac:AccountingCustomerParty")) > 0

    def parse(self, filename: str) -> InvoiceDocument:
        doc = parse(filename)
        return self.parseXml(doc)

    def parseXml(self, doc) -> InvoiceDocument:
        result = InvoiceDocument()
        result.header = self.parseHeader(doc.getElementsByTagName("Invoice")[0])
        result.buyer = self.parseParty(doc.getElementsByTagName("cac:AccountingCustomerParty")[0])
        result.seller = self.parseParty(doc.getElementsByTagName("cac:AccountingSupplierParty")[0])
        # result.summary = self.parseSummary(doc.getElementsByTagName("Invoice-Summary")[0])
        # result.lines = self.parseLines(doc.getElementsByTagName("cac:InvoiceLine"))
        # result = self.processResult(result)
        return result

    def parseHeader(self, element):
        header = InvoiceHeader()
        header.number = xmlExtractText(element, 'cbc:ID')
        header.invoiceDate = xmlExtractDate(element, 'cbc:IssueDate')
        header.salesDate = xmlExtractDate(element, 'cbc:DueDate')
        header.currency = xmlExtractText(element, 'cbc:DocumentCurrencyCode')
        header.paymentDueDate = xmlExtractDate(element, 'cbc:DueDate')
        header.paymentTerms = ""
        header.documentFunctionCode = ""
        return header

    def parseParty(self, xmlParty: Element) -> InvoiceParty:
        party = InvoiceParty()
        xml_ident = xmlParty.getElementsByTagName("cac:PartyIdentification")[0]
        party.taxId = xmlExtractText(xml_ident, 'cbc:ID')
        party.accountNumber = ""
        xml_party_name = xmlParty.getElementsByTagName("cac:PartyName")[0]
        party.name = xmlExtractText(xml_party_name, 'cbc:Name')
        xml_address = xmlParty.getElementsByTagName("cac:PostalAddress")[0]
        party.streetAndNumber = xmlExtractText(xml_address, 'cbc:StreetName')
        party.cityName = xmlExtractText(xml_address, 'cbc:CityName')
        party.postalCode = xmlExtractText(xml_address, 'cbc:PostalZone')
        party.country = xmlExtractText(xml_address, 'cbc:IdentificationCode')
        return party

    def parseLines(self, xmlLines):
        result = []
        for sl in xmlLines:
            result.append(self.parseLine(sl))
        return result

    def parseLine(self, xmlLine: Element) -> InvoiceLine:
        line = InvoiceLine()
        line.LineNumber = xmlExtractText(xmlLine, 'cbc:ID')
        line.EAN = xmlExtractText(xmlLine, 'EAN')
        line.BuyerItemCode = xmlExtractText(xmlLine, 'BuyerItemCode')
        line.SupplierItemCode = xmlExtractText(xmlLine, 'SupplierItemCode')
        line.ItemDescription = xmlExtractText(xmlLine, 'ItemDescription')
        line.ItemType = xmlExtractText(xmlLine, 'ItemType')
        line.InvoiceQuantity = xmlExtractText(xmlLine, "InvoiceQuantity")
        line.UnitOfMeasure = xmlExtractText(xmlLine, "UnitOfMeasure")
        line.InvoiceUnitPacksize = xmlExtractText(xmlLine, "InvoiceUnitPacksize")
        line.PackItemUnitOfMeasure = xmlExtractText(xmlLine, "PackItemUnitOfMeasure")
        line.InvoiceUnitNetPrice = xmlExtractText(xmlLine, "InvoiceUnitNetPrice")
        line.TaxRate = xmlExtractText(xmlLine, "TaxRate")
        line.TaxCategoryCode = xmlExtractText(xmlLine, "TaxCategoryCode")
        line.ReferenceType = xmlExtractText(xmlLine, "ReferenceType")
        line.ReferenceNumber = xmlExtractText(xmlLine, "ReferenceNumber")
        line.TaxAmount = xmlExtractText(xmlLine, "TaxAmount")
        line.NetAmount = xmlExtractText(xmlLine, "NetAmount")
        return line
