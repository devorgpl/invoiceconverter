import re
from xml.dom.minidom import Element, Document, parse

from lib.InvoiceDocument import InvoiceDocument, InvoiceHeader, InvoiceParty, InvoiceSummary, InvoiceTaxSummary, InvoiceLine
from lib.ParserInterface import ParserInterface
from lib.utils.XmlUtil import xmlExtractText, xmlExtractDate


class ComarchXmlParser(ParserInterface):

    def test(self, filename: str) -> bool:
        if not filename.endswith('.xml'):
            print("not xml")
            return False
        doc = parse(filename)
        print(len(doc.getElementsByTagName("Invoice-Header")))
        return len(doc.getElementsByTagName("Invoice-Header")) > 0

    def parse(self, filename: str) -> InvoiceDocument:
        doc = parse(filename)
        return self.parseXml(doc)

    def parseXml(self, xmlRef: Document) -> InvoiceDocument:
        result = InvoiceDocument()
        result.header = self.parseHeader(xmlRef.getElementsByTagName("Invoice-Header")[0])
        result.buyer = self.parseParty(xmlRef.getElementsByTagName("Buyer")[0])
        result.seller = self.parseParty(xmlRef.getElementsByTagName("Seller")[0])
        result.summary = self.parseSummary(xmlRef.getElementsByTagName("Invoice-Summary")[0])
        result.lines = self.parseLines(xmlRef.getElementsByTagName("Line-Item"))
        result = self.processResult(result)
        return result

    def parseLines(self, xmlLines):
        result = []
        for sl in xmlLines:
            result.append(self.parseLine(sl))
        return result

    def parseHeader(self, xmlHeader: Element) -> InvoiceHeader:
        header = InvoiceHeader()
        header.number = xmlExtractText(xmlHeader, 'InvoiceNumber')
        header.invoiceDate = xmlExtractDate(xmlHeader, 'InvoiceDate')
        header.salesDate = xmlExtractDate(xmlHeader, 'SalesDate')
        header.currency = xmlExtractText(xmlHeader, 'InvoiceCurrency')
        header.paymentDueDate = xmlExtractDate(xmlHeader, 'InvoicePaymentDueDate')
        header.paymentTerms = xmlExtractText(xmlHeader, 'InvoicePaymentTerms')
        header.documentFunctionCode = xmlExtractText(xmlHeader, 'DocumentFunctionCode')
        return header

    def parseParty(self, xmlParty: Element) -> InvoiceParty:
        party = InvoiceParty()
        party.taxId = xmlExtractText(xmlParty, 'TaxID')
        party.accountNumber = xmlExtractText(xmlParty, 'AccountNumber')
        party.name = xmlExtractText(xmlParty, 'Name')
        party.streetAndNumber = xmlExtractText(xmlParty, 'StreetAndNumber')
        party.cityName = xmlExtractText(xmlParty, 'CityName')
        party.postalCode = xmlExtractText(xmlParty, 'PostalCode')
        party.country = xmlExtractText(xmlParty, 'Country')
        return party

    def parseSummary(self, xmlSummary: Element) -> InvoiceSummary:
        summary = InvoiceSummary()
        summary.totalLines = xmlExtractText(xmlSummary, 'TotalLines')
        summary.totalNetAmount = xmlExtractText(xmlSummary, 'TotalNetAmount')
        summary.totalTaxableBasis = xmlExtractText(xmlSummary, 'TotalTaxableBasis')
        summary.totalTaxAmount = xmlExtractText(xmlSummary, 'TotalTaxAmount')
        summary.totalGrossAmount = xmlExtractText(xmlSummary, 'TotalGrossAmount')
        summary.grossAmountInWords = xmlExtractText(xmlSummary, 'GrossAmountInWords')
        summary.taxSummary = self.parseTaxSummary(xmlSummary.getElementsByTagName("Tax-Summary-Line")[0])
        return summary

    def parseTaxSummary(self, xmlTaxSummary: Element) -> InvoiceTaxSummary:
        tax_summary = InvoiceTaxSummary()
        tax_summary.taxRate = xmlExtractText(xmlTaxSummary, 'TaxRate')
        tax_summary.taxCategoryCode = xmlExtractText(xmlTaxSummary, 'TaxCategoryCode')
        tax_summary.taxAmount = xmlExtractText(xmlTaxSummary, 'TaxAmount')
        tax_summary.taxableBasis = xmlExtractText(xmlTaxSummary, 'TaxableBasis')
        tax_summary.taxableAmount = xmlExtractText(xmlTaxSummary, 'TaxableAmount')
        tax_summary.grossAmount = xmlExtractText(xmlTaxSummary, 'GrossAmount')
        return tax_summary

    def parseLine(self, xmlLine: Element) -> InvoiceLine:
        line = InvoiceLine()
        line.LineNumber = xmlExtractText(xmlLine, 'LineNumber')
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

    def processResult(self, result):
        result.buyer.shortName = self.shortName(result.buyer.name)
        result.seller.shortName = self.shortName(result.seller.name)
        return result

    def shortName(self, name):
        match = re.search('\\A[@\\w]+', name)
        if match:
            return match.group()
        else:
            return name
