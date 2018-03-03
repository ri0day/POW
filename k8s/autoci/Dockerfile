# our base image
FROM alpine:3.5
MAINTAINER wumin wumin@zillionfortune.com

COPY app.py /usr/src/app/
COPY test.py /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN echo "https://mirrors.ustc.edu.cn/alpine/v3.5/main" > /etc/apk/repositories \
&& echo "https://mirrors.ustc.edu.cn/alpine/v3.5/community" >> /etc/apk/repositories 
RUN apk update  
RUN apk add --update py2-pip \
     && pip install --upgrade pip --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple \
    && pip install --no-cache-dir -r /usr/src/app/requirements.txt --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple


EXPOSE 5000

CMD ["python", "/usr/src/app/app.py"]
