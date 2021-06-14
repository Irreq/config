words_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
                  6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
                  11: 'eleven', 12: 'twelve', 13: 'thirteen',
                  14: 'fourteen', 16: 'sixteen', 17: 'seventeen',
                  18: 'eighteen', 19: 'nineteen', 20: 'twenty',
                  21: 'twenty one', 22: 'twenty two', 23: 'twenty three',
                  24: 'twenty four', 25: 'twenty five', 26: 'twenty six',
                  27: 'twenty seven', 28: 'twenty eight', 29: 'twenty nine'}


def time_conversion(words_dict, hours, minutes, period):
    """Return time as words
    based on relevant condition"""
    if hours == 12:
        hours2 = words_dict.get(1)
    else:
        hours2 = words_dict.get(hours+1)
    if hours == 12 and minutes == 0 and period == 'before midday':
        time_words = 'Midnight'
    elif hours == 12 and minutes == 0 and period == 'after midday':
        time_words = 'Midday'
    elif minutes == 0:
        time_words = "{0} o'clock {1}.".format(str(words_dict.get(hours)).title(),
                                               period)
    elif minutes == 15:
        time_words = "Quarter past {0} {1}.".format(words_dict.get(hours),
                                                    period)
    elif minutes == 30:
        time_words = "Half past {0} {1}.".format(words_dict.get(hours),
                                                 period)
    elif minutes == 45:
        time_words = "Quarter to {0} {1}.".format(hours2,
                                                  period)
    elif minutes < 30:
        min_str = words_dict.get(minutes).capitalize()
        min_num = "" if minutes == 1 else "s"
        time_words = "{0} minute{1} past {2} {3}.".format(min_str,
                                                          min_num,
                                                          words_dict.get(hours),
                                                          period)
    else:
        min_str = words_dict.get(60 - minutes).capitalize()
        min_num = "" if 60 - minutes == 1 else "s"
        time_words = '{0} minute{1} to {2} {3}.'.format(min_str,
                                                        min_num,
                                                        hours2,
                                                        period)
    return time_words



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



print(time_conversion_24(23, 58))
