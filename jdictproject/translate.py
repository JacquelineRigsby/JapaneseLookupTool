import pykakasi
from pykakasi import kakasi

kakasi = kakasi()

kakasi.setMode("r", "Hepburn")
# Default: use Hepburn Roman table
# Options: Hepburn, Kunrei, Passport

kakasi.setMode("s", True)
# Add space, default: no separator

kakasi.setMode("C", True)
# Capitalize, default: no capitalize

def tokenTranslation(conv, str):
    translateList = list()
    for tokenList in str:
        for element in tokenList:
            translateList.append(conv.do(element))
    return translateList

def toRomaji(str):

    kakasi.setMode("H", "a")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("K", "a")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("J", "a")
    # a,H, K, None - roman, Hiragana, Katakana, or non conversion, default: no conversion

    kakasi.setMode("a", "a")

    conv = kakasi.getConverter()

    return conv.do(str)
    #return tokenTranslation(conv, str)


def toHiragana(str):
    kakasi.setMode("a", "H")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("K", "H")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("J", "H")
    # a,H, K, None - roman, Hiragana, Katakana, or non conversion, default: no conversion

    kakasi.setMode("H", "H")

    conv = kakasi.getConverter()

    return conv.do(str)

def toKatakana(str):
    kakasi.setMode("J", "K")
    # a,H, K, None - roman, Hiragana, Katakana, or non conversion, default: no conversion

    kakasi.setMode("H", "K")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("a", "K")
    # a,H,None - roman, Hiragana or non conversion, default: no conversion

    kakasi.setMode("K", "K")

    conv = kakasi.getConverter()

    return conv.do(str)

def toFurigana(str):
    kakasi = pykakasi.kakasi()

    kakasi.setMode("J", "aF")
    # a,H, K, aF, None - roman, Hiragana, Katakana, Furigana, or non conversion, default: no conversion

    kakasi.setMode("H", "aF")
    # a,H, K, aF, None - roman, Hiragana, Katakana, Furigana, or non conversion, default: no conversion

    kakasi.setMode("K", "aF")
    # a,H, K, aF, None - roman, Hiragana, Katakana, Furigana, or non conversion, default: no conversion

    conv = kakasi.getConverter()

    return tokenTranslation(conv, str)
