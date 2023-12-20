import re

def lrc2dict(lrc: str) -> dict:
    lrc_dict = {}
    def remove(x): return x.strip('[|]')
    for line in lrc.split('\n'):
        time_stamps = re.findall(r'\[[^\]]+\]', line)
        if time_stamps:
            # 截取歌词
            lyric = line
            for tplus in time_stamps:
                lyric = lyric.replace(tplus, '')
            # 如果歌词为空，跳过这一行
            if not lyric.strip():
                continue
            # 解析时间
            for tplus in time_stamps:
                t = remove(tplus)
                tag_flag = t.split(':')[0]
                # 跳过: [ar: 逃跑计划]
                if not tag_flag.isdigit():
                    continue
                # 时间累加
                time_lrc = int(tag_flag) * 60
                time_lrc += int(t.split(':')[1].split('.')[0])
                lrc_dict[time_lrc] = lyric
    return lrc_dict
