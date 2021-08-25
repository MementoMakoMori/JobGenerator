import pywikibot
import mwparserfromhell as cleaner
import re
from toolz import compose

site = pywikibot.Site('en', 'wookiee')
cat = pywikibot.Category(site, 'Category:Occupations')
links = list(cat.articles(recurse=1, content=True))

# i should rearrange this as inherited from a Cleaner class or smthg
# out here global since I don't want to recompile regex for every call!
ex = links[:10]
short_ref = re.compile("<ref name=\"[\w\s':;]+?\" />")
long_ref = re.compile("(<ref name=\"[\w\s':;]+?\">.+?</ref>)")
header = re.compile("\n==.+?==\n")
img = re.compile("\[\[File:.+?\]{2,4}.*\n")
nl_double = re.compile("\n\n")
nl_single = re.compile("\n")
ends = ["\n==Behind the scenes==\n", "\n==Appearances==\n", "\n==Sources==\n", "\n==Notes and references==\n"]
p_ends = ["\nBehind the scenes\n", "\nAppearances\n", "\nSources\n", "\nNotes and references\n"]

# some helper functions so that cleaner looks neater


def rm_ref(text: str) -> str:
    return long_ref.sub("", short_ref.sub("", text))


def rm_img(text: str) -> str:
    return img.sub("", text)


def rm_nl(text: str) -> str:
    return nl_single.sub("", nl_double.sub(" ", text))


clean_links = compose(rm_img, rm_ref)


def clean_text(article: pywikibot.Page) -> str:
    text = clean_links(article.get())
    heads = header.findall(text)
    for each in heads:
        if each not in ends:
            text = re.sub(each, "", text)
    text = str(cleaner.parse(text).strip_code())
    end = -1
    sec = 0
    while end < 0:
        end = text.find(p_ends[sec])
        sec += 1
        if sec >= 4:
            break
    text = rm_nl(text[:end])
    return text


cleaned = list(map(clean_text, links))
with open('../sw_jobs.txt', 'w') as f:
    for each in cleaned:
        f.writelines(each+'\n')

