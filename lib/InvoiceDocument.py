from datetime import date


class InvoiceHeader:
    number: str = ""
    invoiceDate: date = None
    salesDate: date = None
    currency: str = ""
    paymentDueDate: date = None
    paymentTerms: str = ""
    documentFunctionCode: str = ""


class InvoiceParty:
    """invoice party"""
    taxId: str = ""
    accountNumber: str = ""
    name: str = ""
    shortName: str = ""
    streetAndNumber: str = ""
    cityName: str = ""
    postalCode: str = ""
    country: str = ""


class InvoiceTaxSummary:
    """tax summary"""
    taxRate: str = ""
    taxCategoryCode: str = ""
    taxAmount: str = ""
    taxableBasis: str = ""
    taxableAmount: str = ""
    grossAmount: str = ""


class InvoiceSummary:
    """invoice summary"""
    totalLines: str = ""
    totalNetAmount: str = ""
    totalTaxableBasis: str = ""
    totalTaxAmount: str = ""
    totalGrossAmount: str = ""
    grossAmountInWords: str = ""
    taxSummary: InvoiceTaxSummary = InvoiceTaxSummary()


class InvoiceLine:
    """invoice line"""
    LineNumber: str = ""
    EAN: str = ""
    BuyerItemCode: str = ""
    SupplierItemCode: str = ""
    ItemDescription: str = ""
    ItemType: str = ""
    InvoiceQuantity: str = ""
    UnitOfMeasure: str = ""
    InvoiceUnitPackSize: str = ""
    PackItemUnitOfMeasure: str = ""
    InvoiceUnitNetPrice: str = ""
    TaxRate: str = ""
    TaxCategoryCode: str = ""
    ReferenceType: str = ""
    ReferenceNumber: str = ""
    TaxAmount: str = ""
    NetAmount: str = ""


class InvoiceDocument:
    header: InvoiceHeader = InvoiceHeader()
    buyer = InvoiceParty()
    seller = InvoiceParty()
    summary = InvoiceSummary()
    lines: [InvoiceLine] = []
