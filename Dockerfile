FROM python:3.8.13-alpine

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /opt/mef
COPY command  /opt/mef/command/
COPY constant /opt/mef/constant/
COPY model /opt/mef/model/
COPY parser /opt/mef/parser/
COPY service /opt/mef/service/
COPY static /opt/mef/static/
COPY util /opt/mef/util/
COPY __init__.py server.py source.json config.json requirements.txt /opt/mef/

#RUN cd /opt/mef && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN cd /opt/mef \
    && python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple/\
    && pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.douban.com/simple/

WORKDIR /opt/mef

EXPOSE 10282

CMD ["python","/opt/mef/server.py"]
