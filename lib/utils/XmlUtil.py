from datetime import datetime


def xmlExtractText(xmlDoc, tagName):
    name_ = xmlDoc.getElementsByTagName(tagName)[0]
    if name_ and name_.firstChild:
        if len(name_.childNodes) == 1:
            return xmlConvertBaseChars(name_.firstChild.nodeValue)
        else:
            return xmlConvertBaseChars(name_.childNodes[1].nodeValue)
    else:
        return ""


def xmlExtractTextOrEmpty(xmlDoc, tagName):
    if len(xmlDoc.getElementsByTagName(tagName)) == 0:
        return ""
    return xmlExtractText(xmlDoc, tagName)


def xmlExtractDate(xmlDoc, tagName):
    text = xmlExtractText(xmlDoc, tagName)
    return datetime.strptime(text, '%Y-%m-%d')


def xmlConvertBaseChars(convertString):
    return convertString \
        .replace("=C5=82", "ł") \
        .replace("=C5=81", "Ł") \
        .replace("=C5=BC", "ż") \
        .replace("=C5=9B", "ś") \
        .replace("=C5=9A", "Ś") \
        .replace("=C4=87", "ć") \
        .replace("=C3=B3", "ó") \
        .replace("=C4=85", "ą") \
        .replace("=C4=99", "ę") \
        .replace("=C5=BA", "ź") \
        .replace("=C5=84", "ń")
