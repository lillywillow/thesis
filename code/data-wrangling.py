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
    with open(episode, encoding = "UTF-8") as episode:
    # converts the HTML format to text
        soup = bs(episode, features="lxml")
        raw_content = soup.get_text()
        episode_path = episode.name
    raw_content = wrangle(raw_content, code)
    # wrangles the text
    with open(episode_path.replace("html_source", "txt_conversion") + ".txt", "w", encoding = "UTF-8") as output_file:
    # writes down the wrangled text
        output_file.write(raw_content)

def wrangle(content, code):
    def group0(content):
    # default group
        return content

    def group1(content):
    # ATL, KOR
        content = max(content.split("\n\n\n\n\n\n"), key = len)
        # strips the beginning of the transcript
        content = content.split("\nCast\n")[0].strip()
        # strips the end of the transcript
        lines = content.splitlines()
        lines = list(filter(None, lines))
        content = ""
        for line in lines:
            if re.match(r'(.*)?[a-z:]$', line.lower()):
                content += line + ": "
            else:
                content += line + "\n"

        return content.strip()
    
    switcher = {
        'ADV': group0,
        'ATL': group1,
        'CLW': group0,
        'DUC': group0,
        'FUT': group0,
        'GRA': group0,
        'GUM': group0,
        'KOR': group1,
        'MLP': group0,
        'OWL': group0,
        'PPG': group0,
        'RAM': group0,
        'SHE': group0,
        'SPO': group0,
        'STU': group0,
        'VOL': group0,
    }

    return switcher.get(code, group0)(content)

if __name__ == "__main__":
    show_paths = initial_setup()
    convert_all(show_paths, path = ('ATL', 'KOR'))