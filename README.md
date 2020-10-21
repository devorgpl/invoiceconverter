# invoiceconverter
Invoice converter library


# usage

    from invoiceconverterlib import invoiceconverter as ic
    
    parser = ic.ffind_format_parser(filename)

    if parser is None:
        print('Parser not found: ' + filename)
        return
    invoice_obj = ic.fget_invoice(filename, parser)
    ic.fgenerate_epp(filename, invoice_obj)
    
