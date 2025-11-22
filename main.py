import requests
import lxml.html
import json
import os
from types import SimpleNamespace

url = input("輸入 URL: ")
sticker_id  = url.split("/")[5]
print(f"貼圖ID: {sticker_id}")
res = requests.get(url)
tree = lxml.html.fromstring(res.text)
links = tree.xpath('/html/body/div[@class="LyWrap"]/div[@class="LyContents MdCF"]/div[@class="LyMain"]/section/div[@class="mdBox03Inner01"]/div[@class="MdCMN09DetailView mdCMN09Sticker"]/div[@class="mdCMN09ImgList"]/div[@class="mdCMN09ImgListWarp"]/ul/li')
arr = []
for link in links:
    jsontxt = json.loads(link.attrib["data-preview"], object_hook=lambda d: SimpleNamespace(**d))
    if jsontxt.animationUrl != "":
        print(f"找到動態圖片: {jsontxt.animationUrl}")
        arr.append(jsontxt.animationUrl)
    elif jsontxt.staticUrl != "":
        print(f"找到靜態圖片: {jsontxt.staticUrl}")
        arr.append(jsontxt.staticUrl)
    else:
        print("Error")
count = 1
if not os.path.isdir("./output"):
    os.mkdir("./output")
if not os.path.isdir(f"./output/{sticker_id}"):
    os.mkdir(f"./output/{sticker_id}")
for i in arr:
    with open(f'./output/{sticker_id}/{count}.png', 'wb') as handle:
        if i == "":
            print(f"圖片連結為空: {i}")
            continue
        response = requests.get(i, stream=True)
        if not response.ok:
            print(f"無法下載圖片: {i}")
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    count+=1