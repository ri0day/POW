#### 介绍
-----
此项目是 gitlab-ci与 kubernetes整合的发布工具(deployer)image.
此镜像包含一个kubectl用于操作kubernetes集群,config文件是指定集群的配置

`deploy.sh` 负责生成deploy servies 模版 然后apply到kubernetes,
`deploy.sh` 接受4个参数 appname image port replicas

-----
##### 示例:
部署 autoci项目 指定image地址为http://xyz/devops/autoci:v2  对外暴露5000端口 3个副本
example : 
`docker pull http://xyz/devops/deployer`
`docker run -rm deployer deploy.sh autoci http://xyz/devops/autoci:v2 5000 3`
