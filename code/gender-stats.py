import statistics

path = "/Users/emma/Documents/thesis/sources/speakers-to-edit.txt"
# set this to the speaker file
codes = ('ADV', 'ATL', 'CLW', 'DUC', 'FUT', 'GRA', 'GUM', 'KOR', 'MLP', 'OWL', 'PPG', 'RAM', 'SHE', 'SPO', 'STU', 'VOL')
# set this to a tuple of all show codes to analyze

stats = dict()
medstats = dict(set())

def percent(code):
    male = stats[code][0]
    female = stats[code][1]
    nb = stats[code][2]

    total = male + female + nb

    return ((male/total) * 100, (female/total) * 100, (nb/total) * 100)

def percentSpeak(code):
    male = stats[code][3]
    female = stats[code][4]
    nb = stats[code][5]

    total = male + female + nb

    return ((male/total) * 100, (female/total) * 100, (nb/total) * 100)

if __name__ == "__main__":
    with open(path, "r", encoding = "UTF-8") as input:
        content = input.readlines()
    for code in codes:
        stats[code] = [0, 0, 0, 0, 0, 0]
        medstats[code + "male"] = set()
        medstats[code + "female"] = set()
    for line in content:
        parts = line.split("\t")
        if (len(parts) != 3):
            print(parts)
            continue
        thisCode = parts[0].split("/", maxsplit = 1)[0]
        tokens = int(parts[1].split(", ")[2].split("]")[0])
        if (parts[2].strip() == "MALE"):
            stats[thisCode][0] += tokens
            stats[thisCode][3] += 1
            medstats[thisCode + "male"].add(tokens)
        elif (parts[2].strip() == "FEMALE"):
            stats[thisCode][1] += tokens
            stats[thisCode][4] += 1
            medstats[thisCode + "female"].add(tokens)
        elif (parts[2].strip() == "NB"):
            stats[thisCode][2] += tokens
            stats[thisCode][5] += 1
        else:
            print(parts)
    for code in codes:
        percentages = percent(code)
        percentagesSp = percentSpeak(code)
        '''
        print("{}:\nmale tokens/percentages: {}, {}\nfemale tokens/percentages: {}, {}\nnonbinary tokens/percentages: {}, {}"
        .format(code, stats[code][0], percentages[0], stats[code][1], percentages[1], stats[code][2], percentages[2]))
        print("male speakers/percentages: {}, {}\nfemale speakers/percentages: {}, {}\nnonbinary speakers/percentages: {}, {}"
        .format(stats[code][3], percentagesSp[0], stats[code][4], percentagesSp[1], stats[code][5], percentagesSp[2]))
        print("{}\n{}\n{}"
        .format(code, percentages[0], percentages[1]))
        print("{}\n{}"
        .format(percentagesSp[0], percentagesSp[1]))
    for key in medstats:
        print("{}\n{}".format(key, statistics.median(medstats[key])))
    '''