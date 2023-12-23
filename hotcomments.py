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

