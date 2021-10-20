import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/Chart1',
        name: 'Chart1',
        component: () => import('@/views/Chart1.vue'),
    },
    {
        path: '/Chart2',
        name: 'Chart2',
        component: () => import('@/views/Chart2.vue'),
    },
    {
        path: '/Chart3',
        name: 'Chart3',
        component: () => import('@/views/Chart3.vue'),
    },
    {
        path: '/Chart4',
        name: 'Chart4',
        component: () => import('@/views/Chart4.vue'),
    },
    {
      path: '/Chart5',
      name: 'Chart5',
      component: () => import('@/views/Chart5.vue'),
  },
]

const router = new VueRouter({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes,
})

export default router
