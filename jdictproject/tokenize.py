from sudachipy import tokenizer
from sudachipy import dictionary

tokenizer_obj = dictionary.Dictionary().create()

mode = tokenizer.Tokenizer.SplitMode.A

# A - text divided into shortest units
# B - text divided into middle units between A and C
# C - extracts named entities

def toTokensNormal(str):
    normalForm = ([m.normalized_form() for m in tokenizer_obj.tokenize(str, mode)])
    return normalForm


def toTokensDictionary(str):
    dictionaryForm = ([m.dictionary_form() for m in tokenizer_obj.tokenize(str, mode)])
    return dictionaryForm
