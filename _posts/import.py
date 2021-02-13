import os, glob
from dateutil import parser
from bs4 import BeautifulSoup

ext = lambda line, cap: line.replace("\s", "").replace(cap, "").strip()

def write_post(doc):
    meta =  {
        'title' : ext(doc[0], "TITLE:"),
        'date'  : parser.parse(ext(doc[2], "DATE:")).strftime("%Y-%m-%d"),
        'tag'   : ext(doc[3], "PRIMARY CATEGORY:"),
        'status': ext(doc[4], "STATUS:"),
        'imgs'  : BeautifulSoup("".join(doc), features="html.parser").find_all('img'),
    }
    if not os.path.exists(meta['tag']):
        os.makedirs(meta['tag'])
    fname = f"{meta['tag']}/{meta['date']}-{meta['title'].replace('/', ' ')}.md"
    publish = 'true' if meta['status'] == 'publish' else 'false'
    feature = meta['imgs'][0].attrs['src'] if len(meta['imgs']) > 0 else None
    with open(fname, "wt") as f:
        # write meta
        f.write("---\n")
        f.write(f"layout: post\n")
        f.write(f"title: {meta['title']}\n")
        f.write(f"date:  {meta['date']}\n")
        f.write(f"tag:   {meta['tag']}\n")
        if feature:
            f.write(f"feature: \"{feature}\"\n")
        f.write(f"published: {publish} \n")
        f.write("---\n")
                
        # write boddy
        body = False
        for d in doc:
            if (d[:3] == '---'):
                continue
            if ('<!-- more -->' in d):
                d = d.replace('<!-- more -->', "").strip()
            if len(d) > 0 and body:
                f.write(d)
            body = ('BODY' in d) or body
    print(f"done {fname}")
    return True


#------------------------------
#  Main
#------------------------------
if __name__ == "__main__": 
    posts = 0
    doc = []
    for idx, line in enumerate(open("raw.txt").readlines()):
        if len(doc) and ('TITLE:' in line):
            posts += write_post(doc)
            doc, meta = [], {}
        doc.append(line)

    # latest post
    posts += write_post(doc)
    print(f"converted {posts} posts with {idx} lines")

