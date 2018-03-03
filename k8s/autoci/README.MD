##### 介绍
-----
gitlab-ci 结合 kubenrtes CI/CD 示例项目
此项目commit以后会:  
1.自动在gitlab-ci上将代码做成images并打上tag push至内部的harbor镜像仓库,然后运行测试.  

2.如果commit到master branch,除了会构建images打tag以外,会自动部署到kubernetes集群中.  

具体逻辑写在 `.gitlab-ci.yml`


