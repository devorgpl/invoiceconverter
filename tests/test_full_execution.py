from invoiceconverterlib import invoiceconverter as ic

def convertFile(filename):
    print(filename)

    parser = ic.ffind_format_parser(filename)

    if parser is None:
        print('Skip: ' + filename)
        return
    invoice_obj = ic.fget_invoice(filename, parser)
    try:
        ic.fgenerate_epp(filename, invoice_obj)
    except UnicodeEncodeError as err:
        print(err)
        print(invoice_obj)
        raise err

def test_should_convert():
    filename = "filename in current directory"
    convertFile(filename)

if __name__ == '__main__':
    test_should_convert()
