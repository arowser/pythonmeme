# -*- coding: utf-8 -*-

import re

filter_dic = [u'shoe', u'snake', u'nail', u'job', u'jobs', u'monty python', 'attack', 'broadcast yourself', 'developer', 'eating', 'gator', 'crocodile', 'alligator', 'bangle', 'python hunter', 'freestyle', 'photo', 'zoo', 'nike air python', "mammal", "store", "shop", "fashion", "python skirt", "tree python", "careers", "sleeping", "park", "died", "sex", "vest", "balmain", "style", "debbie", "shopping", "handbags" "handbag", "sale", "buy", "dresses", "bags", "Herpetology", "legs", "python 5000", "python print case", "the roads to freedom", "film"]

def is_snake(txt):
    for dic in filter_dic:
        if re.search("\\b" + dic + "\\b", txt, re.IGNORECASE) is not None:
           return True

    return False
