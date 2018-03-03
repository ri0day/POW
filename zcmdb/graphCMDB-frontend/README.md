#### graphCMDB-frontend

##### 目录结构说明
- `src`  源代码存放目录
  - `api`  API接口
  - `components`  通用组件
  - `assets`  字体、图标
  - `router`  路由
  - `store`  共享、全局变量( vuex )
  - `views`  子页面
  - `App.vue`
  - `main.js`
- `config`  配置文件存放目录
- `build`  webpack自带目录，可忽略

##### 安装部署
1. `npm install` / `yarn install` # 安装相关npm依赖包
2. `npm run dev` / `yarn run dev` # 启动开发环境，可安装Vue.js devtool调试程序
3. `npm run build` / `yarn run build` # 打包项目代码到dist目录，用于生产环境的发布
4. 可安装 `pushstate-server` 或 Nginx等其他Web Server运行打包的静态文件( dist目录下 )
5. `cd dist;pushstate-server ./ 8888`
