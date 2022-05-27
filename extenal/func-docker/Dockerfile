FROM python:3.8.13-alpine

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /opt/mef
COPY core  /opt/mef/core/
COPY static /opt/mef/static/
COPY templates /opt/mef/templates/
COPY proxy.py requirements.txt /opt/mef/
COPY source.list /etc/apt/sources.list

#RUN cd /opt/mef && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN cd /opt/mef \
#    && apt-get update && apt-get install libxml2-dev libxslt-dev -y \
    && python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple/\
    && pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.douban.com/simple/

WORKDIR /opt/mef

EXPOSE 10284

CMD ["python","/opt/mef/proxy.py"]