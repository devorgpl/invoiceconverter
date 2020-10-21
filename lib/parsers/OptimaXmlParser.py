import re
from xml.dom.minidom import Element, Document, parse

from lib.InvoiceDocument import InvoiceDocument, InvoiceHeader, InvoiceParty, InvoiceSummary, InvoiceTaxSummary, \
    InvoiceLine
from lib.ParserInterface import ParserInterface
from lib.utils.XmlUtil import xmlExtractText, xmlExtractDate, xmlExtractTextOrEmpty


class OptimaXmlParser(ParserInterface):
    """TODO: not ready, trim name and remove new lines"""

    def test(self, filename: str) -> bool:
        if not filename.endswith('.xml'):
            return False
        doc = parse(filename)
        return len(doc.getElementsByTagName("NAGLOWEK")) > 0

    def parse(self, filename: str) -> InvoiceDocument:
        doc = parse(filename)
        return self.parseXml(doc)

    def parseXml(self, xmlRef: Document) -> InvoiceDocument:
        result = InvoiceDocument()
        result.header = self.parseHeader(xmlRef.getElementsByTagName("NAGLOWEK")[0])
        result.buyer = self.parseParty(xmlRef.getElementsByTagName("ODBIORCA")[0])
        result.seller = self.parseParty(xmlRef.getElementsByTagName("SPRZEDAWCA")[0])
        result.summary = self.parseSummary(xmlRef.getElementsByTagName("NAGLOWEK")[0])
        result.lines = self.parseLines(xmlRef.getElementsByTagName("POZYCJA"))
        result = self.processResult(result)
        return result

    def parseLines(self, xmlLines):
        result = []
        for sl in xmlLines:
            result.append(self.parseLine(sl))
        return result

    def parseHeader(self, xmlHeader: Element) -> InvoiceHeader:
        header = InvoiceHeader()
        header.number = xmlExtractText(xmlHeader, 'NUMER_PELNY')
        header.invoiceDate = xmlExtractDate(xmlHeader, 'DATA_WYSTAWIENIA')
        header.salesDate = xmlExtractDate(xmlHeader, 'DATA_OPERACJI')
        header.currency = xmlExtractText(xmlHeader, 'SYMBOL')
        payment_xml = xmlHeader.getElementsByTagName("PLATNOSC")[0]
        header.paymentDueDate = xmlExtractDate(payment_xml, 'TERMIN')
        header.paymentTerms = xmlExtractText(payment_xml, 'FORMA')
        header.documentFunctionCode = ""
        return header

    def parseParty(self, xmlParty: Element) -> InvoiceParty:
        party = InvoiceParty()
        party.taxId = xmlExtractText(xmlParty, 'NIP')
        party.accountNumber = xmlExtractTextOrEmpty(xmlParty, 'NUMER_KONTA_BANKOWEGO')
        party.name = xmlExtractText(xmlParty, 'NAZWA')
        party.streetAndNumber = xmlExtractText(xmlParty, 'ULICA')
        party.cityName = xmlExtractText(xmlParty, 'MIASTO')
        party.postalCode = xmlExtractText(xmlParty, 'KOD_POCZTOWY')
        party.country = xmlExtractText(xmlParty, 'KRAJ')
        return party

    def parseSummary(self, xmlSummary: Element) -> InvoiceSummary:
        summary = InvoiceSummary()
        summary.totalLines = 0
        summary.totalNetAmount = xmlExtractText(xmlSummary, 'RAZEM_NETTO')
        summary.totalTaxableBasis = xmlExtractText(xmlSummary, 'RAZEM_NETTO')
        summary.totalTaxAmount = xmlExtractText(xmlSummary, 'RAZEM_VAT')
        summary.totalGrossAmount = xmlExtractText(xmlSummary, 'RAZEM_BRUTTO')
        summary.grossAmountInWords = ""
        summary.taxSummary = None
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
        line.LineNumber = xmlExtractText(xmlLine, 'LP')
        line.EAN = xmlExtractText(xmlLine, 'EAN')
        line.BuyerItemCode = xmlExtractText(xmlLine, 'KOD')
        line.SupplierItemCode = xmlExtractText(xmlLine, 'NUMER_KATALOGOWY')
        line.ItemDescription = xmlExtractText(xmlLine, 'NAZWA')
        line.ItemType = ""
        line.InvoiceQuantity = xmlExtractText(xmlLine, "ILOSC")
        line.UnitOfMeasure = xmlExtractText(xmlLine, "JM")
        line.InvoiceUnitPacksize = xmlExtractText(xmlLine, "ILOSC")
        line.PackItemUnitOfMeasure = xmlExtractText(xmlLine, "JM")
        line.InvoiceUnitNetPrice = xmlExtractText(xmlLine, "PO_RABACIE_PLN")
        line.TaxRate = xmlExtractText(xmlLine, "STAWKA")
        line.TaxCategoryCode = xmlExtractText(xmlLine, "FLAGA")
        line.ReferenceType = ""
        line.ReferenceNumber = ""
        line.NetAmount = xmlExtractText(xmlLine, "WARTOSC_NETTO")
        grossAmount = xmlExtractText(xmlLine, "WARTOSC_BRUTTO")
        tax = str(round(float(grossAmount) - float(line.NetAmount), 2))
        line.TaxAmount = tax
        return line

    def processResult(self, result):
        result.buyer.shortName = self.shortName(result.buyer.name)
        result.seller.shortName = self.shortName(result.seller.name)
        result.summary.totalLines = len(result.lines)
        return result

    def shortName(self, name):
        match = re.search('\\A[@\\w]+', name)
        if match:
            return match.group()
        else:
            return name
