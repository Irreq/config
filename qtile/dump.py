def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
             'seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
            'eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = int((numStrLen+2)/3)
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = int(groups-(i/3+1))
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
    if join: return ' '.join(words)
    return words

def appendInt(num):
    num = int(num)
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return 'st'
    elif (lastDigit == 2):
        return 'nd'
    elif (lastDigit == 3):
        return 'rd'
    else:
        return 'th'


def time_conversion_24(hours, minutes):
    """Convert time to words"""
    result = numToWords(hours)

    if minutes == 0:
        result += " o'clock"

    elif minutes == 15:
        result = "quarter past " + result

    elif minutes == 30:
        result = "half past " + result

    elif minutes == 45:
        result = "quarter to " + result

    elif minutes < 30:
        result = "{} minute{} past ".format(numToWords(minutes), "" if minutes == 1 else "s") + result

    else:
        result = "{} minute{} to ".format(numToWords(60-minutes), "" if 60 - minutes == 1 else "s") + result
    return result



def parse_query(query):
    # print("  >  {}\n".format(query))
    if query.startswith("hello"):
        notify("Hello, friend!")
    elif query.startswith("exit"):
        notify("Bye!")
        exit(0)

    elif query.startswith("time"):
        d_date = datetime.datetime.now()
        # reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
        # print(reg_format_date)

        # some other date formats.
        date = d_date.strftime("%A %d %B %Y %I %M %S")
        date = date.split()
        result = date[0] + " " + numToWords(int(date[1])) + appendInt(date[1]) + " " + date[2]
        result += " " # + numToWords(int(date[3])) # + " " + numToWords(int(date[4]))
        # result += " " + numToWords(int(date[3])) + " " + str(date[4]) + " " + str(date[5])
        # result += " ".join([numToWords(int(date[i])) for i in (3, 4, 5)])
        result += numToWords(int(date[3])) + " " + time_conversion_24(int(date[4]), int(date[5]))
        result += " or " + numToWords(int(date[4])) + " and " + numToWords(int(date[5]))
        print(result)


        notify(result)
    elif query.startswith("rapport"):
        notify("Welcome back, all systems are online and working properly!")
    elif query.startswith("audio"):
        os.system("python3 -q /home/irreq/github/config/programs/audio.py toggle")
    # elif query.startswith("terminal"):
    else:
        tokenized = nltk.word_tokenize(query)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if (pos[:2] == 'NN')]
        notify(" ".join(nouns))
        notify("What?")
def recognize_speech_from_microphone(recognizer, microphone):
    response = {
            "success": True,
            "error": "",
            "transcription": ""
    }

    if not isinstance(recognizer, sr.Recognizer):
        response["error"] = "`recognizer` must be `Recognizer` instance"

    if not isinstance(microphone, sr.Microphone):
        response["error"] = "`microphone` must be `Microphone` instance"

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unintelligible"

    return response


