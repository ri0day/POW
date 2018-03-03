import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'

import Server from '@/views/Server'
import NoSQL from '@/views/NoSQL'
import RDBMS from '@/views/RDBMS'
import LoadBalance from '@/views/LoadBalance'
import IpAddress from '@/views/IpAddress'
import Home from '@/views/Home'
import Sidebar from '@/views/Sidebar'
import Login from '@/views/Login'
import Application from '@/views/Application'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      component: Sidebar,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          component: Home,
          meta: { requiresAuth: true }
        },
        {
          path: 'server',
          component: Server,
          meta: { requiresAuth: true }
        },
        {
          path: 'nosql',
          component: NoSQL,
          meta: { requiresAuth: true }
        },
        {
          path: 'rdbms',
          component: RDBMS,
          meta: { requiresAuth: true }
        },
        {
          path: 'loadbalance',
          component: LoadBalance,
          meta: { requiresAuth: true }
        },
        {
          path: 'ipaddress',
          component: IpAddress,
          meta: { requiresAuth: true }
        },
        {
          path: 'application',
          component: Application,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '*',
      redirect: '/'
    }
  ],
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    axios({
      method: 'get',
      url: process.env.API_URL + '/_db/CMDB/_api/version',
      headers: { 'Authorization': 'bearer ' + localStorage.getItem('Authorization') }
    }).then(
      () => {
        next()
      },
      () => {
        localStorage.removeItem('Authorization')
        next({ path: '/login' })
      }
    )
  } else {
    next() // make sure to always call next()!
  }
})

export default router
