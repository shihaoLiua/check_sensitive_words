import time

from fastapi import FastAPI, Body, WebSocket
from multiprocessing import current_process

import ahocorasick
import jieba

# 创建敏感词检测器实例
sensitive_word_detector = ahocorasick.Automaton()

def load_sensitive_words():
    load_file_st = time.time()
    # 从文件加载敏感词列表
    with open('sensitive_words', 'r') as file:
        for word in file:
            word = word.strip()  # 去除换行符和空格
            sensitive_word_detector.add_word(word, word)
    
    print(f"load_sensitive_file cost is {str((time.time() - load_file_st)*1000)[:6]} ms")

# 加载敏感词
load_sensitive_words()

# 构建敏感词自动机
sensitive_word_detector.make_automaton()

app = FastAPI()

# 实现方案：结巴分词后判断是否有敏感词
@app.post("/detect_sensitive_words", summary="敏感词检测")
async def detect_sensitive_words(text: str = Body(..., embed=True)):
    st = time.time()
    # 在文本中查找敏感词
    sensitive_words = set()
    # 分词
    seg_text_list = []
    for word in jieba.cut(text):
        if sensitive_word_detector.exists(word):
            sensitive_words.add(word)
        seg_text_list.append(word)
    print(f"seg_text_list is {seg_text_list}")
    
    
    # for end_index, word in sensitive_word_detector.iter_long(text):
    #     start_index = end_index - len(word) + 1
    #     sensitive_words.add(word)

    return {"text": text, "sensitive_words": list(sensitive_words), "cost": str((time.time() - st)*1000)[:6] + "ms", "worker": current_process().name}


if __name__ == "__main__":
    import uvicorn
    
    # Don't set debug/reload equals True in release, because TimedRotatingFileHandler can't support multi-prcoess
    # please used "uvicorn --host 127.0.0.1 --port 8000 main:app --env-file ./configs/.env" run in release, and used "python sensitive_words.py" in dev
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )