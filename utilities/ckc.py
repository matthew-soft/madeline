import random

smallcaps_alphabet = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ1234567890"

uppercase_fraktur = "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
lowercase_fraktur = "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷1234567890"

uppercase_boldfraktur = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
lowercase_boldfraktur = "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟1234567890"


double_uppercase = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"

double_lowercase = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"

bold_fancy_lowercase = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃1234567890"
bold_fancy_uppercase = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"

fancy_lowercase = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
fancy_uppercase = "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"


alphabet = dict(zip("abcdefghijklmnopqrstuvwxyz1234567890", range(0, 36)))
uppercase_alphabet = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(0, 26)))
punctuation = dict(zip("§½!\"#¤%&/()=?`´@£$€{[]}\\^¨~'*<>|,.-_:", range(0, 37)))
space = " "
aesthetic_space = "\u3000"
aesthetic_punctuation = '§½！"＃¤％＆／（）＝？`´＠£＄€｛［］｝＼＾¨~＇＊＜＞|，．－＿：'
aesthetic_lowercase = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ１２３４５６７８９０"
aesthetic_uppercase = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"

eight_ball_responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
]


def aesthetics(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += aesthetic_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += aesthetic_uppercase[uppercase_alphabet[letter]]
            elif letter in punctuation:
                returnthis += aesthetic_punctuation[punctuation[letter]]
            elif letter == space:
                returnthis += aesthetic_space
            else:
                returnthis += letter
    return returnthis


def double_font(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += double_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += double_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_fraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_fraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def bold_fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_boldfraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_boldfraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def bold_fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += bold_fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += bold_fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def smallcaps(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += smallcaps_alphabet[alphabet[letter]]
            else:
                returnthis += letter
    return returnthis


def ball_response():
    returnthis = random.choice(eight_ball_responses)
    return returnthis
