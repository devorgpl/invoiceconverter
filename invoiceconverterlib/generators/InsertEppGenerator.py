from invoiceconverterlib.InvoiceDocument import InvoiceDocument
from invoiceconverterlib.GeneratorInterface import GeneratorInterface


class InsertEppGenerator(GeneratorInterface):
    def generateTxt(self, input: InvoiceDocument) -> str:
        outputTxt: str = ""
        outputTxt += self.generateInfo(input)
        outputTxt += self.generateInvoice(input)
        outputTxt += self.generateItemDictionary(input)
        return outputTxt

    def generateInfo(self, input):
        result = ""
        invoiceDate = input.header.invoiceDate
        result += "[INFO]\n"
        result += '"1.05",3,1250,"Subiekt GT",'
        result += self.quote(input.seller.shortName) + ","
        result += self.quote(input.seller.shortName) + ","
        result += self.quote(input.seller.name) + ","
        result += self.quote(input.seller.cityName) + ","
        result += self.quote(input.seller.postalCode) + ","
        result += self.quote(input.seller.streetAndNumber) + ","
        result += self.quote(input.seller.taxId) + ","
        result += self.quote("MAG") + ","
        result += self.quote("Magazyn") + ","
        result += ","
        result += ","
        result += "1" + ","
        result += invoiceDate.strftime('%Y%m%d%H%M%S') + ","
        result += invoiceDate.strftime('%Y%m%d%H%M%S') + ","
        result += "Automat" + ","
        result += invoiceDate.strftime('%Y%m%d%H%M%S') + ","
        result += "Polska" + ","
        result += "PL" + ","
        result += ","
        result += "0"
        result += "\n"
        result += "\n"
        return result

    @staticmethod
    def quote(data):
        return '"' + data.replace('"', '\'') + '"'

    def generateInvoice(self, input):
        t = input.header.invoiceDate
        result = "[NAGLOWEK]\n"
        result += '"FS",1,0,2004,,,'
        result += self.quote(input.header.number) + ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += self.quote(input.buyer.shortName) + ","
        result += self.quote(input.buyer.name) + ","
        result += self.quote(input.buyer.name) + ","
        result += self.quote(input.buyer.cityName) + ","
        result += self.quote(input.buyer.postalCode) + ","
        result += self.quote(input.buyer.streetAndNumber) + ","
        result += self.quote(input.buyer.taxId) + ","

        result += self.quote('Sprzedaż') + ","
        result += self.quote('Sprzedaż dla klienta') + ","
        result += self.quote(input.buyer.cityName) + ","
        result += t.strftime('%Y%m%d%H%M%S') + ","
        result += t.strftime('%Y%m%d%H%M%S') + ","
        result += ","
        result += str(len(input.lines)) + ","
        result += "1,"
        result += self.quote('detaliczna') + ","
        result += input.summary.totalNetAmount + ","
        result += input.summary.totalTaxAmount + ","
        result += input.summary.totalGrossAmount + ","
        result += ","
        result += ","

        result += "0.0000,"
        result += t.strftime('%Y%m%d%H%M%S') + ","
        result += "0.0000,"
        result += "0.000,"
        result += "0,"
        result += "0,"
        result += "1,"
        result += "0,"
        result += "0,"
        result += 'Wystawca,'
        result += ","
        result += ","
        result += "0.0000,"
        result += "0.0000,"
        result += "PLN,"
        result += "1.0000,"
        result += ","
        result += ","
        result += ","
        result += ","
        result += "0,"
        result += "0,"
        result += "0,"
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += "\n"
        result += "\n"

        result += "[ZAWARTOSC]"
        result += "\n"

        for item in input.lines:
            result += self.generateInvoiceLine(item)

        result += "\n"
        result += "\n"
        return result

    def generateInvoiceLine(self, item):
        result = ''
        result += item.LineNumber + ","
        result += "1,"
        result += self.quote(item.EAN) + ","
        result += "1,"
        result += "0,"
        result += "0,"
        result += "1,"
        result += "0.0000,"
        result += "0.0000,"  # rabat?
        result += "szt.,"
        result += self.quote(item.InvoiceQuantity) + ","
        result += self.quote(item.InvoiceQuantity) + ","
        result += ","
        result += self.quote(item.InvoiceUnitNetPrice) + ","  # cena bazowa
        result += self.quote(item.InvoiceUnitNetPrice) + ","  # cena sugerowana
        result += self.quote(item.TaxRate) + ","
        result += self.quote(item.NetAmount) + ","
        result += self.quote(item.TaxAmount) + ","
        result += self.quote(str(round(float(item.NetAmount) + float(item.TaxAmount), 4))) + ","
        result += ","
        result += ","

        result += "\n"
        return result

    def generateItemDictionary(self, input):
        result = ""
        result += "[NAGLOWEK]\n"
        result += '"TOWARY"'
        result += "\n"
        result += "\n"
        result += "[ZAWARTOSC]"
        result += "\n"

        for item in input.lines:
            result += self.generateItemDictionaryLine(item)
        return result

    def generateItemDictionaryLine(self, item):
        result = ''
        result += "1,"
        result += self.quote(item.EAN) + ","
        result += self.quote(item.EAN) + ","
        result += self.quote(item.EAN) + ","
        result += self.quote(item.ItemDescription.strip()) + ","

        result += ","
        result += ","
        result += ","
        result += self.quote("") + ","
        result += '"szt.",'
        result += self.quote(str(round(float(item.TaxRate)))) + ","
        result += item.TaxRate + ","
        result += self.quote(str(round(float(item.TaxRate)))) + ","
        result += item.TaxRate + ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += self.quote('') + ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += ","
        result += self.quote(item.EAN) + ","
        result += ","
        result += ","
        result += "\n"
        return result

    def generate(self, invoice_obj, filename):
        text_file = open(filename, "w", encoding='cp1250', newline='\r\n')

        txt = self.generateTxt(invoice_obj)
        # print(txt)
        text_file.write(txt)
        text_file.close()
