import openai,re
import pandas as pd
import json
from load_data import load_raw,load_csv
import time
import os
inputlist = ['input/news_center.json', 'input/news_entity.json']

def ask_GPT(text):
    openai.api_key = 'API_KEY'
    print('sleeping......')
    time.sleep(3.0)
    print('sleep done')
    
    prompt = f'假设你是一个实体关系五元组抽取模型。我会给你头实体类型列表subject_types，尾实体类型列表object_types，关系列表relations，再给你一个句子，请你根据这三个列表抽出句子中的subject和object，并组成五元组，且形式为(subject, subject_type, relation, object,   object_type)。给定的句子为："{text}"。relations：["获奖","提名","导演","主演","评价","入围","题材","饰演"]。subject_types：["人物","影视作品","事件"]。object_types：["奖项名称","影视作品","人物","事件","评价","艺术流派风格","角色"]。在给定的句子中，可能包含了哪些五元组？请按照形式(subject, subject_type, relation, object, object_type)回答：'
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role":"user","content":prompt}],
            temperature=0.5)
    ans=response['choices'][0]['message']['content']
    return ans.strip()

def get_rel(inputlist):
    res = []
    tdata = load_raw(inputlist)
    for td in tdata:
        res.append(ask_GPT(td['content']))
    return res


def write_to_csv(outlist):
    dic = {'ans':outlist}
    df = pd.DataFrame(dic)
    df.to_csv('output/outtemp.csv',index=False)
    

def write_to_json(fp:str = 'output/outtemp.csv',outs = 'output/outputs.json'):
    df = pd.read_csv(fp)
    ansl = df.ans.tolist()
    core = []
    for ans in ansl:
        temp = re.findall(r'[\(](.*?)[)]', ans)
        for tt in temp:
            tt = tt.replace('"','')
            tt = tt.split(', ')
            core.append({"s":tt[0],"p":tt[2],"o":tt[3]})
    with open(outs,'a') as f:

        for cc in core:
            f.write(json.dumps(cc,ensure_ascii=False)+'\n')


def direct_write_json(content,cnt_id,outs = 'output/outputsina.json'):
    core = []
    print(content)
    temp = re.findall(r'[\(](.*?)[)]', content)
    for tt in temp:
        tt = tt.replace('"','').replace(' ','')
        tt = tt.split(',')
        core.append({"s":tt[0],"p":tt[2],"o":tt[3]})
    with open(outs,'a',encoding='utf-8') as f:

        for cc in core:
            f.write(json.dumps(cc,ensure_ascii=False)+'\n')
    with open('outrecord.txt','w') as fo:
        fo.write(str(cnt_id))


if __name__ == '__main__':
    tdata = load_csv()
    output = 'output/outputsina.json'
    cnt = 0
    if os.path.exists('outrecord.txt'):
        with open('outrecord.txt','r') as f:
            s = f.read()
            cnt = int(s)
    for i,td in enumerate(tdata):
        print(f'processing new no.{i+1}')
        if i>=cnt:
            ar = ask_GPT(td)
            direct_write_json(ar,i+1,output)
