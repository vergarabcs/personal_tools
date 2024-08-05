
def is_ascii(char):
    return 0 <= ord(char) <= 127

def split_jap(text):
    if(len(text) == 0): 
        return []
    splitted = []
    word = []
    ascii_switch = is_ascii(text[0])
    for char in text:
        is_curr_ascii = is_ascii(char)
        if(is_curr_ascii != ascii_switch):
            splitted.append(word)
            word = [char]
            ascii_switch = is_curr_ascii
        else:
            word.append(char)
    if(len(word) > 0):
        splitted.append(word)
    ret_val = list(map(
        lambda x: ''.join(x).strip(),
        splitted
    ))
    return ret_val

def split(text):
    import re
    sound_tag_removed = re.sub(r"(\[sound:.*\])|['-]", '', text)
    enclosed_paren_removed = re.sub(r'\(.*\):', '', sound_tag_removed)
    splitted = enclosed_paren_removed.split('.')

    ret_val = []
    split_2d = list(map(
        split_jap,
        splitted
    ))
    for x in split_2d:
        for y in x:
            ret_val.append(y)
    return ret_val

splitted = split('''
1.) この避難所では (kono hinansho de wa): This phrase means 'at this shelter' or 'in this evacuation center.'
- この (kono): This is a demonstrative pronoun meaning 'this.'
- 避難所 (hinansho): This term means 'shelter' or 'evacuation center.'
- では (de wa): This combination indicates the location or context.

2.) 犬や猫と一緒に (inu ya neko to issho ni): This part means 'together with dogs and cats.'
- 犬や猫 (inu ya neko): This phrase means 'dogs and cats.'
- と一緒に (to issho ni): This expression means 'together with.'

3.) 生活できます (seikatsu dekimasu): This phrase means 'can live.'
- 生活 (seikatsu): This term means 'life' or 'living.'
- できます (dekimasu): This is a verb that means 'can' or 'is possible.' [sound:say-5b836df9-181814d6-681e7a99-b7ecfd8c-90b43ee8.mp3]
''')

for x in splitted:
    print(x)

