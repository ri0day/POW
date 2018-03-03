#!/usr/local/bin/bash
appname=${1:?"no appname,exit"}
image=${2:?"no image,exit"}
port=${3:?"no port,exit"}
num=${4:-1}

if [ $# -lt 4 ]
then
echo "Example: appname: flaskapp , image: registry:/flaskapp:v1 port: 5000 ,replicas 4"
echo "usage: ./deploy.sh flaskapp registry:/flaskapp:v1 5000 4"
exit
fi
echo "deployv2 running"
echo "runnig with appname:$appname image:$image port:$port  replicas:$num"
f=/tmp/$appname.$RANDOM.$(date + %Y%m%d-%H:%M:%S).yaml

cat >$f <<ENF
---
apiVersion: v1
kind: Service
metadata:
  name: ${appname}
spec:
  ports:
  - port: 5000
    targetPort: 5000
  selector:
    app: ${appname}
  type: NodePort
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: ${appname}
spec:
  replicas: ${num}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  minReadySeconds: 5
  template:
    metadata:
      labels:
        app: ${appname}
    spec:
      containers:
      - name: ${appname}
        image: ${image}
        imagePullPolicy: Always
        ports:
        - containerPort: ${port}
ENF

echo run with yaml file:
cat $f
kubectl delete deploy/$appname||true
kubectl delete svc/$appname||true
kubectl apply -f $f
rm -rf $f
