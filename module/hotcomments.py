import json
import requests
import execjs


# stra = ''
# a=stra.join(random.choice("0123456789abcdef") for i in range(32))
# print(a)



def hotComments(song_id: int, a: int ) -> dict:
  ####参数获取
  # song_id = "191254"
  results = []
  d = '{"rid":"R_SO_4_'+str(song_id)+'","threadId":"R_SO_4_'+str(song_id)+'","pageNo":"1","pageSize":"20","cursor":"-1","offset":"0","orderType":"1","csrf_token": "'+str(a)+'" }'
  sign=get_sign(d)
  sign=sign.split(",")
  #####请求
  headers = { 'content-type': "application/x-www-form-urlencoded" }
  body = {'params': sign[0] ,'encSecKey': sign[1]}
  response = requests.post("https://music.163.com/weapi/comment/resource/comments/get?csrf_token=" + str(a) , data = body, headers = headers)
  # print(response.json()["data"]["hotComments"])
  if response.json()["data"]["hotComments"] == None:
    results = [{'username': '软件作者友情的提醒', 'hotcomments': '听的什么歌啊，这歌无热评啊，有点尴尬（拍爪爪'}, {'username': '兽人控作者友情提醒', 'hotcomments': '听的什么歌啊，这歌无热评啊，有点尴尬（拍爪爪'},{'username': '应用程序作者友情提醒', 'hotcomments': '你来到没有热评的歌曲评论区，非常抱歉，您可以打开肯德基APP点吃的来缓解压力'},{'username': '重岳', 'hotcomments': '如你所见，我时常记下来的，只是一些体悟，而非具体的武功招式。武道在“意”，受限于那些花哨的形式便再难突破。好比看不出夕画里的意境，非抓着她讨论笔力技法，免不了要吃闭门羹, 最后只可惜这首词曲无人获得那热门评价。'},{'username': '魈', 'hotcomments': '嗯，好听…为什么这首曲无人评价，想来是无人能了解其中奥秘。'}]
    return results
  else:
    for comment in response.json()["data"]["hotComments"]:
        keys_to_remove = ['musicPackage', 'vipRights', 'commentVideoVO', 'commentLocationType', 'tag']
        for key in keys_to_remove:
            if key in comment["user"]:
                del comment["user"][key]
        # 将所有参数添加到 JSON 中
        result = {
          "username": comment["user"]["nickname"],
          "hotcomments": comment["content"],
        }
        for key, value in comment.items():
            if key in result:
              # 如果键已经存在于结果中，将值添加到列表中
                if not isinstance(result[key], list):
                    result[key] = [result[key]]
                    result[key].append(value)
                else:
                    result[key] = value
        results.append(result)
    return results



def get_sign(request_info):
    js = execjs.compile(open("res/pyjs.js", encoding="utf-8").read())
    print(execjs.get().name)
    req = js.call("getenc", request_info)
    # print(req.split(",")[0])
    # print(req.split(",")[1])
    return req

