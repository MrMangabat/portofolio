import { createRouter, createWebHistory } from 'vue-router'

import ResearchView from '../views/ResearchView.vue'
import AboutView from '../views/AboutView.vue'
// import LogInView from '../views/LogInView.vue'
// import Projects from '../views/Projects.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/research',
      name: 'research',
      component: ResearchView
    },
 
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    
    // {
    //   path: '/projectoverview',
    //   name: 'projectoverview',
    //   component: ProjectsOverview
    // },
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: LogInView

    // }, 
    {
      path: '/',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LogInView.vue')
    }
  ]
})

export default router