import os
import time
from requests_html import HTML, HTMLSession

dir_name = "yuzu"
search_tags = ['muririn','kobuichi']
mini_idx = 1000000

extension = '.jpg' # '.png' '.jpeg' '.jpg'
caption = '.txt'
save_tags = True
re_index = True
prefix = 'yuzu$style'
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)

session = HTMLSession()
ids = []
for s_tags in search_tags:
    
    print(f"Collecting ids for tags:{s_tags}")
    page_id = 0
    tmp = -1
    while tmp != len(ids):
        tmp = len(ids)
        tmp_ele = session.get(f"https://gelbooru.com/index.php?page=post&s=list&tags={s_tags}&pid={page_id}").html.find('.thumbnail-container', first = True)
        for idx, span in enumerate(tmp_ele.find('a')):
            # _url = span.find('a')
            _id = span.attrs['id'][1::]
            if mini_idx > int(_id):
                tmp = len(ids)
                break
            if _id not in ids:
                ids.append(_id)
        page_id +=idx+1
        idx = -1
    print(f"number of ids :{len(ids)}")

counter = 0
for idx, _id in enumerate(ids):
    if idx % 20 == 0:
        print(f"working on No. {idx} image")
    post = session.get(f"https://gelbooru.com/index.php?page=post&s=view&id={_id}")    
    post_html = post.html
    tags = [prefix]
    for tag in post_html.find('li'):
        if 'class' in tag.attrs and 'tag-type-general' in tag.attrs['class']:
            tmp = tag.find('a')
            tags.append(tmp[1].text.lower())
    for hyperlink in post_html.find('a'):
        if hyperlink.text.lower() == "original image":
            image = hyperlink.attrs['href']
            image_content = session.get(image)
            if re_index:
                _id = idx
            with open(dir_name + f'/{_id}{extension}', 'wb') as f:
                f.write(image_content.content)
                counter+=1
                if save_tags:
                    with open(dir_name + f'/{_id}{caption}', 'w') as capt:
                        capt.write(','.join(str(t) for t in tags))
    

print(f"Total of {counter} images fetched")