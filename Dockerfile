FROM python:3.9-alpine

WORKDIR /detect_sensitive_words

ADD . .

# 安装依赖
RUN pip install --upgrade pip  --no-cache-dir &&  \
    pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --no-cache-dir

CMD [ "python","main.py" ]

