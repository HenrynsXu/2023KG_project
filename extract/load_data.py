import json
import pandas as pd

# inputlist = ['input/news_center.json', 'input/news_entity.json']
def load_raw(fps: list):
    data = []
    for fp in fps:
        with open(fp,'rb') as f:
            for line in f:
                temp = json.loads(line)
                data.append({'id':temp['id'],'content':temp['content'].replace('\u3000',' ')})
    return data

def load_csv(fp:str = r'input\sinaent3.csv'): # 新浪娱乐相关新闻（太长的手动截取）
    df = pd.read_csv(fp,encoding='gbk')
    ll = df.content.tolist()
    res = []
    
    for s in ll:
        if len(s)>100: res.append(s)
    need = [res[0],res[1],res[-2],res[-1][:2500],res[-3][:2700]]
    normed = [n.replace('\u3000',' ') for n in need]
    return normed

if __name__ == '__main__':
    # ld = load_raw(inputlist)
    # print(len(ld))
    # print(ld[2])
    pass