import os, glob
from dateutil import parser

raw = open("raw.txt").readlines()
posts = 0
doc = []
for idx, line in enumerate(raw):
    if len(doc) and ('TITLE:' in line):
        ext = lambda line, cap: line.replace("\s", "").replace(cap, "").strip()
        meta =  {
            'title' : ext(doc[0], "TITLE:"),
            'date'  : parser.parse(ext(doc[2], "DATE:")).strftime("%Y-%m-%d"),
            'tag'   : ext(doc[3], "PRIMARY CATEGORY:"),
        }
        fname = f"{meta['date']}-{meta['title'].replace('/', ' ')}.md"
        with open(fname, "wt") as f:
            # write meta
            f.write("---\n")
            f.write(f"layout: post\n")
            f.write(f"title: {meta['title']}\n")
            f.write(f"date:  {meta['date']}\n")
            f.write(f"tag:   {meta['tag']}\n")
            f.write("published: true \n")
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
            posts += 1
#         print(fname)
        doc, meta = [], {}
    doc.append(line)
print(f"converted {posts} posts with {idx} lines")

