"""A Python Pig Latin translator
"""
def trans_v(wd):
    return wd + "yay"
vowels = list("aeiou")
def trans_c(wd, vowels):
    if wd[1].lower() in vowels:
        return wd[1:] + wd[:1] + "ay"
    else:
        return wd[2:] + wd[:2] + "ay"
# print(trans_c("to", vowels))
def is_v(wd, vowels):
    return wd[0].lower() in vowels
def trans_txt(txt, vowels):
    wds = txt.split()
    output = []
    # print(output)
    for wd in wds:
        if not wd[-1].isalpha():
            punct = wd[-1]
            wd_push = wd[:-1]
        else:
            wd_push = wd
        if is_v(wd_push, vowels):
            wd_push = trans_v(wd_push)
        else:
            wd_push = trans_c(wd_push, vowels)
        if not wd[-1].isalpha():
            wd_push = wd_push + punct
        output.append(wd_push)
    # print(output)
    return " ".join(output)
txt = "I'm getting married in the morning! Ding, dong, the bells are gonna chime!"
print(trans_txt(txt, vowels))
