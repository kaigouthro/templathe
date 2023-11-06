# vearch

```python
from langchain.document\_loaders import TextLoader  
from langchain.embeddings.huggingface import HuggingFaceEmbeddings  
from langchain.text\_splitter import RecursiveCharacterTextSplitter  
from transformers import AutoModel, AutoTokenizer  
from langchain.vectorstores.vearch import Vearch  
  
# repalce to your local model path  
model\_path ="/data/zhx/zhx/langchain-ChatGLM\_new/chatglm2-6b"   
  
tokenizer = AutoTokenizer.from\_pretrained(model\_path, trust\_remote\_code=True)  
model = AutoModel.from\_pretrained(model\_path, trust\_remote\_code=True).half().cuda(0)  

```

```text
 /export/anaconda3/envs/vearch\_cluster\_langchain/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user\_install.html  
 from .autonotebook import tqdm as notebook\_tqdm  
 Loading checkpoint shards: 100%|██████████| 7/7 [00:07<00:00, 1.01s/it]  

```

```python
query = "你好!"  
response, history = model.chat(tokenizer, query, history=[])  
print(f"Human: {query}\nChatGLM:{response}\n")  
query = "你知道凌波微步吗，你知道都有谁学会了吗?"  
response, history = model.chat(tokenizer, query, history=history)  
print(f"Human: {query}\nChatGLM:{response}\n")  

```

```text
 Human: 你好!  
 ChatGLM:你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。  
   
 Human: 你知道凌波微步吗，你知道都有谁学会了吗?  
 ChatGLM:凌波微步是一种步伐，最早出自《倚天屠龙记》。在电视剧《人民的名义》中，侯亮平也学会了凌波微步。  
   

```

```python
# Add your local knowledge files  
file\_path = "/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt"#Your local file path"  
loader = TextLoader(file\_path,encoding="utf-8")  
documents = loader.load()  
  
# split text into sentences and embedding the sentences  
text\_splitter = RecursiveCharacterTextSplitter(chunk\_size=500, chunk\_overlap=100)  
texts = text\_splitter.split\_documents(documents)  
  
#replace to your model path  
embedding\_path = '/data/zhx/zhx/langchain-ChatGLM\_new/text2vec/text2vec-large-chinese'  
embeddings = HuggingFaceEmbeddings(model\_name=embedding\_path)  

```

```text
 No sentence-transformers model found with name /data/zhx/zhx/langchain-ChatGLM\_new/text2vec/text2vec-large-chinese. Creating a new one with MEAN pooling.  

```

```python
#first add your document into vearch vectorstore  
vearch\_standalone = Vearch.from\_documents(  
 texts,embeddings,path\_or\_url="/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/localdb\_new\_test",table\_name="localdb\_new\_test",flag=0)  
  
print("\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*")  
  
vearch\_cluster = Vearch.from\_documents(  
 texts,embeddings,path\_or\_url="http://test-vearch-langchain-router.vectorbase.svc.ht1.n.jd.local",db\_name="vearch\_cluster\_langchian",table\_name="tobenumone",flag=1)  

```

```text
 docids ['18ce6747dca04a2c833e60e8dfd83c04', 'aafacb0e46574b378a9f433877ab06a8', '9776bccfdd8643a8b219ccee0596f370']  
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
 docids ['1841638988191686991', '-4519586577642625749', '5028230008472292907']  

```

```python
query = "你知道凌波微步吗，你知道都有谁会凌波微步?"  
vearch\_standalone\_res=vearch\_standalone.similarity\_search(query, 3)  
for idx,tmp in enumerate(vearch\_standalone\_res):   
 print(f"{'#'\*20}第{idx+1}段相关文档{'#'\*20}\n\n{tmp.page\_content}\n")  
  
# combine your local knowleadge and query   
context = "".join([tmp.page\_content for tmp in vearch\_standalone\_res])  
new\_query = f"基于以下信息，尽可能准确的来回答用户的问题。背景信息:\n {context} \n 回答用户这个问题:{query}\n\n"  
response, history = model.chat(tokenizer, new\_query, history=[])  
print(f"\*\*\*\*\*\*\*\*ChatGLM:{response}\n")  
  
print("\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*")  
  
query\_c = "你知道凌波微步吗，你知道都有谁会凌波微步?"  
cluster\_res=vearch\_cluster.similarity\_search(query\_c, 3)  
for idx,tmp in enumerate(cluster\_res):   
 print(f"{'#'\*20}第{idx+1}段相关文档{'#'\*20}\n\n{tmp.page\_content}\n")  
  
# combine your local knowleadge and query   
context\_c = "".join([tmp.page\_content for tmp in cluster\_res])  
new\_query\_c = f"基于以下信息，尽可能准确的来回答用户的问题。背景信息:\n {context\_c} \n 回答用户这个问题:{query\_c}\n\n"  
response\_c, history\_c = model.chat(tokenizer, new\_query\_c, history=[])  
print(f"\*\*\*\*\*\*\*\*ChatGLM:{response\_c}\n")  

```

```text
 ####################第1段相关文档####################  
   
 午饭过后，段誉又练“凌波微步”，走一步，吸一口气，走第二步时将气呼出，六十四卦走完，四肢全无麻痹之感，料想呼吸顺畅，便无害处。第二次再走时连走两步吸一口气，再走两步始行呼出。这“凌波微步”是以动功修习内功，脚步踏遍六十四卦一个周天，内息自然而然地也转了一个周天。因此他每走一遍，内力便有一分进益。  
   
 这般练了几天，“凌波微步”已走得颇为纯熟，不须再数呼吸，纵然疾行，气息也已无所窒滞。心意既畅，跨步时渐渐想到《洛神赋》中那些与“凌波微步”有关的句子：“仿佛兮若轻云之蔽月，飘飘兮若流风之回雪”，“竦轻躯以鹤立，若将飞而未翔”，“体迅飞凫，飘忽若神”，“动无常则，若危若安。进止难期，若往若还”。  
   
   
   
 百度简介  
   
 凌波微步是「逍遥派」独门轻功身法，精妙异常。  
   
 凌波微步乃是一门极上乘的轻功，所以列于卷轴之末，以易经八八六十四卦为基础，使用者按特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。此步法精妙异常，原是要待人练成「北冥神功」，吸人内力，自身内力已【颇为深厚】之后再练。  
   
 ####################第2段相关文档####################  
   
 《天龙八部》第五回 微步縠纹生  
   
 卷轴中此外诸种经脉修习之法甚多，皆是取人内力的法门，段誉虽自语宽解，总觉习之有违本性，单是贪多务得，便非好事，当下暂不理会。  
   
 卷到卷轴末端，又见到了“凌波微步”那四字，登时便想起《洛神赋》中那些句子来：“凌波微步，罗袜生尘……转眄流精，光润玉颜。含辞未吐，气若幽兰。华容婀娜，令我忘餐。”曹子建那些千古名句，在脑海中缓缓流过：“秾纤得衷，修短合度，肩若削成，腰如约素。延颈秀项，皓质呈露。芳泽无加，铅华弗御。云髻峨峨，修眉连娟。丹唇外朗，皓齿内鲜。明眸善睐，靥辅承权。瑰姿艳逸，仪静体闲。柔情绰态，媚于语言……”这些句子用在木婉清身上，“这话倒也有理”；但如用之于神仙姊姊，只怕更为适合。想到神仙姊姊的姿容体态，“皎若太阳升朝霞，灼若芙蓉出绿波”，但觉依她吩咐行事，实为人生至乐，心想：“我先来练这‘凌波微步’，此乃逃命之妙法，非害人之手段也，练之有百利而无一害。”  
   
 ####################第3段相关文档####################  
   
 《天龙八部》第二回 玉壁月华明  
   
 再展帛卷，长卷上源源皆是裸女画像，或立或卧，或现前胸，或见后背。人像的面容都是一般，但或喜或愁，或含情凝眸，或轻嗔薄怒，神情各异。一共有三十六幅图像，每幅像上均有颜色细线，注明穴道部位及练功法诀。  
   
 帛卷尽处题着“凌波微步”四字，其后绘的是无数足印，注明“妇妹”、“无妄”等等字样，尽是《易经》中的方位。段誉前几日还正全心全意地钻研《易经》，一见到这些名称，登时精神大振，便似遇到故交良友一般。只见足印密密麻麻，不知有几千百个，自一个足印至另一个足印均有绿线贯串，线上绘有箭头，最后写着一行字道：“步法神妙，保身避敌，待积内力，再取敌命。”  
   
 段誉心道：“神仙姊姊所遗的步法，必定精妙之极，遇到强敌时脱身逃走，那就很好，‘再取敌命’也就不必了。”  
 卷好帛卷，对之作了两个揖，珍而重之地揣入怀中，转身对那玉像道：“神仙姊姊，你吩咐我朝午晚三次练功，段誉不敢有违。今后我对人加倍客气，别人不会来打我，我自然也不会去吸他内力。你这套‘凌波微步’我更要用心练熟，眼见不对，立刻溜之大吉，就吸不到他内力了。”至于“杀尽我逍遥派弟子”一节，却想也不敢去想。  
   
 \*\*\*\*\*\*\*\*ChatGLM:凌波微步是一门极上乘的轻功，源于《易经》八八六十四卦。使用者按照特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。这门轻功精妙异常，可以使人内力大为提升，但需在练成“北冥神功”后才能真正掌握。凌波微步在金庸先生的《天龙八部》中得到了充分的描写。  
   
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
 ####################第1段相关文档####################  
   
 午饭过后，段誉又练“凌波微步”，走一步，吸一口气，走第二步时将气呼出，六十四卦走完，四肢全无麻痹之感，料想呼吸顺畅，便无害处。第二次再走时连走两步吸一口气，再走两步始行呼出。这“凌波微步”是以动功修习内功，脚步踏遍六十四卦一个周天，内息自然而然地也转了一个周天。因此他每走一遍，内力便有一分进益。  
   
 这般练了几天，“凌波微步”已走得颇为纯熟，不须再数呼吸，纵然疾行，气息也已无所窒滞。心意既畅，跨步时渐渐想到《洛神赋》中那些与“凌波微步”有关的句子：“仿佛兮若轻云之蔽月，飘飘兮若流风之回雪”，“竦轻躯以鹤立，若将飞而未翔”，“体迅飞凫，飘忽若神”，“动无常则，若危若安。进止难期，若往若还”。  
   
   
   
 百度简介  
   
 凌波微步是「逍遥派」独门轻功身法，精妙异常。  
   
 凌波微步乃是一门极上乘的轻功，所以列于卷轴之末，以易经八八六十四卦为基础，使用者按特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。此步法精妙异常，原是要待人练成「北冥神功」，吸人内力，自身内力已【颇为深厚】之后再练。  
   
 ####################第2段相关文档####################  
   
 《天龙八部》第五回 微步縠纹生  
   
 卷轴中此外诸种经脉修习之法甚多，皆是取人内力的法门，段誉虽自语宽解，总觉习之有违本性，单是贪多务得，便非好事，当下暂不理会。  
   
 卷到卷轴末端，又见到了“凌波微步”那四字，登时便想起《洛神赋》中那些句子来：“凌波微步，罗袜生尘……转眄流精，光润玉颜。含辞未吐，气若幽兰。华容婀娜，令我忘餐。”曹子建那些千古名句，在脑海中缓缓流过：“秾纤得衷，修短合度，肩若削成，腰如约素。延颈秀项，皓质呈露。芳泽无加，铅华弗御。云髻峨峨，修眉连娟。丹唇外朗，皓齿内鲜。明眸善睐，靥辅承权。瑰姿艳逸，仪静体闲。柔情绰态，媚于语言……”这些句子用在木婉清身上，“这话倒也有理”；但如用之于神仙姊姊，只怕更为适合。想到神仙姊姊的姿容体态，“皎若太阳升朝霞，灼若芙蓉出绿波”，但觉依她吩咐行事，实为人生至乐，心想：“我先来练这‘凌波微步’，此乃逃命之妙法，非害人之手段也，练之有百利而无一害。”  
   
 ####################第3段相关文档####################  
   
 《天龙八部》第二回 玉壁月华明  
   
 再展帛卷，长卷上源源皆是裸女画像，或立或卧，或现前胸，或见后背。人像的面容都是一般，但或喜或愁，或含情凝眸，或轻嗔薄怒，神情各异。一共有三十六幅图像，每幅像上均有颜色细线，注明穴道部位及练功法诀。  
   
 帛卷尽处题着“凌波微步”四字，其后绘的是无数足印，注明“妇妹”、“无妄”等等字样，尽是《易经》中的方位。段誉前几日还正全心全意地钻研《易经》，一见到这些名称，登时精神大振，便似遇到故交良友一般。只见足印密密麻麻，不知有几千百个，自一个足印至另一个足印均有绿线贯串，线上绘有箭头，最后写着一行字道：“步法神妙，保身避敌，待积内力，再取敌命。”  
   
 段誉心道：“神仙姊姊所遗的步法，必定精妙之极，遇到强敌时脱身逃走，那就很好，‘再取敌命’也就不必了。”  
 卷好帛卷，对之作了两个揖，珍而重之地揣入怀中，转身对那玉像道：“神仙姊姊，你吩咐我朝午晚三次练功，段誉不敢有违。今后我对人加倍客气，别人不会来打我，我自然也不会去吸他内力。你这套‘凌波微步’我更要用心练熟，眼见不对，立刻溜之大吉，就吸不到他内力了。”至于“杀尽我逍遥派弟子”一节，却想也不敢去想。  
   
 \*\*\*\*\*\*\*\*ChatGLM:凌波微步是一门极上乘的轻功，源于《易经》中的六十四卦。使用者按照特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。这门轻功精妙异常，可以使人内力增进，但需要谨慎练习，避免伤害他人。凌波微步在逍遥派中尤为流行，但并非所有逍遥派弟子都会凌波微步。  
   

```

```python
query = "你知道vearch是什么吗?"  
response, history = model.chat(tokenizer, query, history=history)  
print(f"Human: {query}\nChatGLM:{response}\n")  
  
vearch\_info = ["Vearch 是一款存储大语言模型数据的向量数据库，用于存储和快速搜索模型embedding后的向量，可用于基于个人知识库的大模型应用",  
 "Vearch 支持OpenAI, Llama, ChatGLM等模型，以及LangChain库",  
 "vearch 是基于C语言,go语言开发的，并提供python接口，可以直接通过pip安装"]  
vearch\_source=[{'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/tlbb/three\_body.txt'},{'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/tlbb/three\_body.txt'},{'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/tlbb/three\_body.txt'}]  
vearch\_standalone.add\_texts(vearch\_info,vearch\_source)  
  
print("\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*")  
  
vearch\_cluster.add\_texts(vearch\_info,vearch\_source)  

```

```text
 Human: 你知道vearch是什么吗?  
 ChatGLM:是的，我知道 Vearch。Vearch 是一种用于计算机械系统极化子的工具，它可以用于模拟和优化电路的性能。它是一个基于Matlab的电路仿真软件，可以用于设计和分析各种类型的电路，包括交流电路和直流电路。  
   
 docids ['eee5e7468434427eb49829374c1e8220', '2776754da8fc4bb58d3e482006010716', '9223acd6d89d4c2c84ff42677ac0d47c']  
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
 docids ['-4311783201092343475', '-2899734009733762895', '1342026762029067927']  
  
  
  
  
  
 ['-4311783201092343475', '-2899734009733762895', '1342026762029067927']  

```

```python
query3 = "你知道vearch是什么吗?"  
res1 = vearch\_standalone.similarity\_search(query3, 3)  
for idx,tmp in enumerate(res1):   
 print(f"{'#'\*20}第{idx+1}段相关文档{'#'\*20}\n\n{tmp.page\_content}\n")  
  
context1 = "".join([tmp.page\_content for tmp in res1])  
new\_query1 = f"基于以下信息，尽可能准确的来回答用户的问题。背景信息:\n {context1} \n 回答用户这个问题:{query3}\n\n"  
response, history = model.chat(tokenizer, new\_query1, history=[])  
print(f"\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*ChatGLM:{response}\n")  
  
print("\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*")  
  
query3\_c = "你知道vearch是什么吗?"  
res1\_c = vearch\_standalone.similarity\_search(query3\_c, 3)  
for idx,tmp in enumerate(res1\_c):   
 print(f"{'#'\*20}第{idx+1}段相关文档{'#'\*20}\n\n{tmp.page\_content}\n")  
  
context1\_C = "".join([tmp.page\_content for tmp in res1\_c])  
new\_query1\_c = f"基于以下信息，尽可能准确的来回答用户的问题。背景信息:\n {context1\_C} \n 回答用户这个问题:{query3\_c}\n\n"  
response\_c, history\_c = model.chat(tokenizer, new\_query1\_c, history=[])  
  
print(f"\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*ChatGLM:{response\_c}\n")  

```

```text
 ####################第1段相关文档####################  
   
 Vearch 是一款存储大语言模型数据的向量数据库，用于存储和快速搜索模型embedding后的向量，可用于基于个人知识库的大模型应用  
   
 ####################第2段相关文档####################  
   
 Vearch 支持OpenAI, Llama, ChatGLM等模型，以及LangChain库  
   
 ####################第3段相关文档####################  
   
 vearch 是基于C语言,go语言开发的，并提供python接口，可以直接通过pip安装  
   
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*ChatGLM:是的，Varch是一个向量数据库，旨在存储和快速搜索模型embedding后的向量。它支持OpenAI、ChatGLM等模型，并可直接通过pip安装。  
   
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*after is cluster res\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
 ####################第1段相关文档####################  
   
 Vearch 是一款存储大语言模型数据的向量数据库，用于存储和快速搜索模型embedding后的向量，可用于基于个人知识库的大模型应用  
   
 ####################第2段相关文档####################  
   
 Vearch 支持OpenAI, Llama, ChatGLM等模型，以及LangChain库  
   
 ####################第3段相关文档####################  
   
 vearch 是基于C语言,go语言开发的，并提供python接口，可以直接通过pip安装  
   
 \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*ChatGLM:是的，Varch是一个向量数据库，旨在存储和快速搜索模型embedding后的向量。它支持OpenAI，ChatGLM等模型，并可用于基于个人知识库的大模型应用。Varch基于C语言和Go语言开发，并提供Python接口，可以通过pip安装。  
   

```

```python
##delete and get function need to maintian docids   
##your docid  
  
res\_d=vearch\_standalone.delete(['eee5e7468434427eb49829374c1e8220', '2776754da8fc4bb58d3e482006010716', '9223acd6d89d4c2c84ff42677ac0d47c'])  
print("delete vearch standalone docid",res\_d)  
query = "你知道vearch是什么吗?"  
response, history = model.chat(tokenizer, query, history=[])  
print(f"Human: {query}\nChatGLM:{response}\n")  
  
res\_cluster=vearch\_cluster.delete(['-4311783201092343475', '-2899734009733762895', '1342026762029067927'])  
print("delete vearch cluster docid",res\_cluster)  
query\_c = "你知道vearch是什么吗?"  
response\_c, history = model.chat(tokenizer, query\_c, history=[])  
print(f"Human: {query}\nChatGLM:{response\_c}\n")  
  
  
get\_delet\_doc=vearch\_standalone.get(['eee5e7468434427eb49829374c1e8220', '2776754da8fc4bb58d3e482006010716', '9223acd6d89d4c2c84ff42677ac0d47c'])  
print("after delete docid to query again:",get\_delet\_doc)  
get\_id\_doc=vearch\_standalone.get(['18ce6747dca04a2c833e60e8dfd83c04', 'aafacb0e46574b378a9f433877ab06a8', '9776bccfdd8643a8b219ccee0596f370','9223acd6d89d4c2c84ff42677ac0d47c'])  
print("get existed docid",get\_id\_doc)  
  
get\_delet\_doc=vearch\_cluster.get(['-4311783201092343475', '-2899734009733762895', '1342026762029067927'])  
print("after delete docid to query again:",get\_delet\_doc)  
get\_id\_doc=vearch\_cluster.get(['1841638988191686991', '-4519586577642625749', '5028230008472292907','1342026762029067927'])  
print("get existed docid",get\_id\_doc)  

```

```text
 delete vearch standalone docid True  
 Human: 你知道vearch是什么吗?  
 ChatGLM:Vearch是一种用于处理向量的库,可以轻松地将向量转换为矩阵,并提供许多有用的函数和算法,以操作向量。 Vearch支持许多常见的向量操作,例如加法、减法、乘法、除法、矩阵乘法、求和、统计和归一化等。 Vearch还提供了一些高级功能,例如L2正则化、协方差矩阵、稀疏矩阵和奇异值分解等。  
   
 delete vearch cluster docid True  
 Human: 你知道vearch是什么吗?  
 ChatGLM:Vearch是一种用于处理向量数据的函数,可以应用于多种不同的编程语言和数据结构中。  
   
 Vearch最初是作为Java中一个名为“vearch”的包而出现的,它的目的是提供一种高效的向量数据结构。它支持向量的多态性,可以轻松地实现不同类型的向量之间的转换,同时还支持向量的压缩和反向操作等操作。  
   
 后来,Vearch被广泛应用于其他编程语言中,如Python、Ruby、JavaScript等。在Python中,它被称为“vectorize”,在Ruby中,它被称为“Vector”。  
   
 Vearch的主要优点是它的向量操作具有多态性,可以应用于不同类型的向量数据,同时还支持高效的向量操作和反向操作,因此可以提高程序的性能。  
   
 after delete docid to query again: {}  
 get existed docid {'18ce6747dca04a2c833e60e8dfd83c04': Document(page\_content='《天龙八部》第二回 玉壁月华明\n\n再展帛卷，长卷上源源皆是裸女画像，或立或卧，或现前胸，或见后背。人像的面容都是一般，但或喜或愁，或含情凝眸，或轻嗔薄怒，神情各异。一共有三十六幅图像，每幅像上均有颜色细线，注明穴道部位及练功法诀。\n\n帛卷尽处题着“凌波微步”四字，其后绘的是无数足印，注明“妇妹”、“无妄”等等字样，尽是《易经》中的方位。段誉前几日还正全心全意地钻研《易经》，一见到这些名称，登时精神大振，便似遇到故交良友一般。只见足印密密麻麻，不知有几千百个，自一个足印至另一个足印均有绿线贯串，线上绘有箭头，最后写着一行字道：“步法神妙，保身避敌，待积内力，再取敌命。”\n\n段誉心道：“神仙姊姊所遗的步法，必定精妙之极，遇到强敌时脱身逃走，那就很好，‘再取敌命’也就不必了。”\n卷好帛卷，对之作了两个揖，珍而重之地揣入怀中，转身对那玉像道：“神仙姊姊，你吩咐我朝午晚三次练功，段誉不敢有违。今后我对人加倍客气，别人不会来打我，我自然也不会去吸他内力。你这套‘凌波微步’我更要用心练熟，眼见不对，立刻溜之大吉，就吸不到他内力了。”至于“杀尽我逍遥派弟子”一节，却想也不敢去想。', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'}), 'aafacb0e46574b378a9f433877ab06a8': Document(page\_content='《天龙八部》第五回 微步縠纹生\n\n卷轴中此外诸种经脉修习之法甚多，皆是取人内力的法门，段誉虽自语宽解，总觉习之有违本性，单是贪多务得，便非好事，当下暂不理会。\n\n卷到卷轴末端，又见到了“凌波微步”那四字，登时便想起《洛神赋》中那些句子来：“凌波微步，罗袜生尘……转眄流精，光润玉颜。含辞未吐，气若幽兰。华容婀娜，令我忘餐。”曹子建那些千古名句，在脑海中缓缓流过：“秾纤得衷，修短合度，肩若削成，腰如约素。延颈秀项，皓质呈露。芳泽无加，铅华弗御。云髻峨峨，修眉连娟。丹唇外朗，皓齿内鲜。明眸善睐，靥辅承权。瑰姿艳逸，仪静体闲。柔情绰态，媚于语言……”这些句子用在木婉清身上，“这话倒也有理”；但如用之于神仙姊姊，只怕更为适合。想到神仙姊姊的姿容体态，“皎若太阳升朝霞，灼若芙蓉出绿波”，但觉依她吩咐行事，实为人生至乐，心想：“我先来练这‘凌波微步’，此乃逃命之妙法，非害人之手段也，练之有百利而无一害。”', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'}), '9776bccfdd8643a8b219ccee0596f370': Document(page\_content='午饭过后，段誉又练“凌波微步”，走一步，吸一口气，走第二步时将气呼出，六十四卦走完，四肢全无麻痹之感，料想呼吸顺畅，便无害处。第二次再走时连走两步吸一口气，再走两步始行呼出。这“凌波微步”是以动功修习内功，脚步踏遍六十四卦一个周天，内息自然而然地也转了一个周天。因此他每走一遍，内力便有一分进益。\n\n这般练了几天，“凌波微步”已走得颇为纯熟，不须再数呼吸，纵然疾行，气息也已无所窒滞。心意既畅，跨步时渐渐想到《洛神赋》中那些与“凌波微步”有关的句子：“仿佛兮若轻云之蔽月，飘飘兮若流风之回雪”，“竦轻躯以鹤立，若将飞而未翔”，“体迅飞凫，飘忽若神”，“动无常则，若危若安。进止难期，若往若还”。\n\n\n\n百度简介\n\n凌波微步是「逍遥派」独门轻功身法，精妙异常。\n\n凌波微步乃是一门极上乘的轻功，所以列于卷轴之末，以易经八八六十四卦为基础，使用者按特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。此步法精妙异常，原是要待人练成「北冥神功」，吸人内力，自身内力已【颇为深厚】之后再练。', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'})}  
 after delete docid to query again: {}  
 get existed docid {'1841638988191686991': Document(page\_content='《天龙八部》第二回 玉壁月华明\n\n再展帛卷，长卷上源源皆是裸女画像，或立或卧，或现前胸，或见后背。人像的面容都是一般，但或喜或愁，或含情凝眸，或轻嗔薄怒，神情各异。一共有三十六幅图像，每幅像上均有颜色细线，注明穴道部位及练功法诀。\n\n帛卷尽处题着“凌波微步”四字，其后绘的是无数足印，注明“妇妹”、“无妄”等等字样，尽是《易经》中的方位。段誉前几日还正全心全意地钻研《易经》，一见到这些名称，登时精神大振，便似遇到故交良友一般。只见足印密密麻麻，不知有几千百个，自一个足印至另一个足印均有绿线贯串，线上绘有箭头，最后写着一行字道：“步法神妙，保身避敌，待积内力，再取敌命。”\n\n段誉心道：“神仙姊姊所遗的步法，必定精妙之极，遇到强敌时脱身逃走，那就很好，‘再取敌命’也就不必了。”\n卷好帛卷，对之作了两个揖，珍而重之地揣入怀中，转身对那玉像道：“神仙姊姊，你吩咐我朝午晚三次练功，段誉不敢有违。今后我对人加倍客气，别人不会来打我，我自然也不会去吸他内力。你这套‘凌波微步’我更要用心练熟，眼见不对，立刻溜之大吉，就吸不到他内力了。”至于“杀尽我逍遥派弟子”一节，却想也不敢去想。', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'}), '-4519586577642625749': Document(page\_content='《天龙八部》第五回 微步縠纹生\n\n卷轴中此外诸种经脉修习之法甚多，皆是取人内力的法门，段誉虽自语宽解，总觉习之有违本性，单是贪多务得，便非好事，当下暂不理会。\n\n卷到卷轴末端，又见到了“凌波微步”那四字，登时便想起《洛神赋》中那些句子来：“凌波微步，罗袜生尘……转眄流精，光润玉颜。含辞未吐，气若幽兰。华容婀娜，令我忘餐。”曹子建那些千古名句，在脑海中缓缓流过：“秾纤得衷，修短合度，肩若削成，腰如约素。延颈秀项，皓质呈露。芳泽无加，铅华弗御。云髻峨峨，修眉连娟。丹唇外朗，皓齿内鲜。明眸善睐，靥辅承权。瑰姿艳逸，仪静体闲。柔情绰态，媚于语言……”这些句子用在木婉清身上，“这话倒也有理”；但如用之于神仙姊姊，只怕更为适合。想到神仙姊姊的姿容体态，“皎若太阳升朝霞，灼若芙蓉出绿波”，但觉依她吩咐行事，实为人生至乐，心想：“我先来练这‘凌波微步’，此乃逃命之妙法，非害人之手段也，练之有百利而无一害。”', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'}), '5028230008472292907': Document(page\_content='午饭过后，段誉又练“凌波微步”，走一步，吸一口气，走第二步时将气呼出，六十四卦走完，四肢全无麻痹之感，料想呼吸顺畅，便无害处。第二次再走时连走两步吸一口气，再走两步始行呼出。这“凌波微步”是以动功修习内功，脚步踏遍六十四卦一个周天，内息自然而然地也转了一个周天。因此他每走一遍，内力便有一分进益。\n\n这般练了几天，“凌波微步”已走得颇为纯熟，不须再数呼吸，纵然疾行，气息也已无所窒滞。心意既畅，跨步时渐渐想到《洛神赋》中那些与“凌波微步”有关的句子：“仿佛兮若轻云之蔽月，飘飘兮若流风之回雪”，“竦轻躯以鹤立，若将飞而未翔”，“体迅飞凫，飘忽若神”，“动无常则，若危若安。进止难期，若往若还”。\n\n\n\n百度简介\n\n凌波微步是「逍遥派」独门轻功身法，精妙异常。\n\n凌波微步乃是一门极上乘的轻功，所以列于卷轴之末，以易经八八六十四卦为基础，使用者按特定顺序踏着卦象方位行进，从第一步到最后一步正好行走一个大圈。此步法精妙异常，原是要待人练成「北冥神功」，吸人内力，自身内力已【颇为深厚】之后再练。', metadata={'source': '/data/zhx/zhx/langchain-ChatGLM\_new/knowledge\_base/天龙八部/lingboweibu.txt'})}  

```
