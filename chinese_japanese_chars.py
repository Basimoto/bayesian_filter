import re
import pdb

# all chinese characters
regex_chinese = re.compile(r"[\u4e00-\u9fff]+", re.IGNORECASE) 
# all japanese characters:
regex_japanese = re.compile(r"[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\u3400-\u4dbf]", re.IGNORECASE)

# check for chinese/japanese tokens
def check_for_cj_chars(tokens):
    for t in tokens:
        if re.search(regex_japanese, t):
            token_string = t
            for x in t:
                if re.search(regex_japanese, x):
                    tokens.append(x)
                    token_string = token_string.replace(x,' ')

              
            more_tokens = token_string.split()
            
            for mt in more_tokens:
                tokens.append(mt)

            tokens.remove(t)        

    return tokens
