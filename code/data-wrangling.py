from bs4 import BeautifulSoup as bs
import glob
import os
import re

path_base = "/Users/emma/Documents/thesis/sources/"
# set this to the project folder
codes = ('ADV', 'ATL', 'CLW', 'DUC', 'FUT', 'GRA', 'GUM', 'KOR', 'MLP', 'OWL', 'PPG', 'RAM', 'SHE', 'SPO', 'STU', 'VOL')
# set this to a tuple of all show codes to wrangle

def initial_setup():
    show_paths = dict()
    # dictionary of all lists of path files attached to the show names
    for code in codes:
        locals()["path_" + code] = path_base + "html_source/" + code + "/*"
        locals()["files_" + code] = glob.glob(locals()["path_" + code])
        # where the HTML source files are, makes a list of every file path in those folders
        show_paths[code] = locals()["files_" + code]
    return show_paths

def convert_all(show_paths, path = codes):
    for code in show_paths.keys():
        if code in path:
        # handles all codes as default, can be set to only handle some
            if not os.path.exists(path_base + "txt_conversion/" + code):
            # checks if a folder exists, otherwise makes one
                os.makedirs(path_base + "txt_conversion/" + code)
            for episode in show_paths[code]:
            # converts each episode
                convert_single(episode, code)

def convert_single(episode, code):
    with open(episode, encoding = "UTF-8") as epi:
    # converts the HTML format to text
        soup = bs(epi, features="lxml")
        raw_content = soup.get_text()
    raw_content = wrangle(raw_content, code)
    # wrangles the text
    with open(episode.replace("html_source", "txt_conversion") + ".txt", "w", encoding = "UTF-8") as output_file:
    # writes down the wrangled text
        output_file.write(raw_content)

def wrangle(content, code):
    def group0(content, colon):
    # default group
        return content

    def group1(content, colon):
    # ('ATL', 'KOR')
        content = max(content.split("\n\n\n\n\n\n"), key = len)
        # strips the beginning of the transcript
        content = content.split("\nCast\n")[0].strip()
        # strips the end of the transcript
        if colon:
            return colonize(content)
        else:
            return content.strip()

    def group2(content, colon):
    # ('ADV', 'CLW', 'DUC', 'FUT', 'OWL', 'PPG', 'SHE', 'SPO', 'VOL')
        content = content.split("Retrieved from \"")[0].strip()
        if (len(re.split(r'Futurama transcripts', content)) > 1):
            content = (re.split(r'Futurama transcripts', content))[0].strip()
        if (content.endswith("See Also: Episode Transcript List")):
            content = content.split("See Also: Episode Transcript List")[0].strip()
        if (len(content.split("Play Sound")) > 1):
            content = content.split("Play Sound")[1].strip()
        if (len(content.split("The Neutral Planet")) > 1):
            content = content.split("The Neutral Planet")[1].strip()
        if (len(re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)) > 1):
            content = re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)[1].strip()
        if (len(re.split(r'\nTranscripts?\n', content, re.M)) > 2):
            content = re.split(r'\nTranscripts?\n', content, re.M)[2].strip()
        if (len(re.split(r'This article is a transcript of the SpongeBob SquarePants episode .+\n', content)) > 1):
            content = re.split(r'This article is a transcript of the SpongeBob SquarePants episode .+\n', content)[1].strip()
        if (len(re.split(r'\(Opening shot: .+\n', content)) > 1):
            content = re.split(r'\(Opening shot: .+\n', content)[1].strip()
        if (len(re.split(r'\n([A-Z]+: )', content, re.M)) > 2):
            content = re.split(r'\n([A-Z]+: )', content, maxsplit = 1)[1] + re.split(r'\n([A-Z]+:)', content, maxsplit = 1)[2].strip()
        if colon:
            return colonize(content)
        else:
            return content.strip()

    def colonize(content):
    # converts columns to "<speaker>: <sentence>"
        lines = content.splitlines()
        lines = list(filter(None, lines))
        content = ""
        for line in lines:
            if re.match(r'(.*)?(([a-z:])|(b\.o\.y\.d\.))$', line.lower().strip()):
                content += line.strip() + ": "
            else:
                content += line.strip() + "\n"
        return content.strip()
    
    switcher = {
        'ADV': [group2, False],
        'ATL': [group0, True],
        'CLW': [group2, False],
        'DUC': [group2, True],
        'FUT': [group2, False],
        'GRA': [group0, True],
        'GUM': [group0, False],
        'KOR': [group1, True],
        'MLP': [group0, False],
        'OWL': [group2, False],
        'PPG': [group2, False],
        'RAM': [group0, False],
        'SHE': [group2, False],
        'SPO': [group2, False],
        'STU': [group0, True],
        'VOL': [group2, False],
    }

    return switcher.get(code, group0)[0](content, switcher[code][1])

if __name__ == "__main__":
    show_paths = initial_setup()
    convert_all(show_paths, path = ('GRA', 'GUM', 'MLP', 'RAM', 'STU'))