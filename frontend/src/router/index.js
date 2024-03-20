import { createRouter, createWebHistory } from 'vue-router'

import ResearchView from '../views/InterestView.vue'
import AboutView from '../views/AboutView.vue'
import CVandStuff from '../views/CVandStuff.vue'
// import LogInView from '../views/LogInView.vue'
// import Projects from '../views/Projects.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'About',
      component: AboutView,
      alias: '/about'
    },


    {
      path: '/interests',
      name: 'interests',
      component: ResearchView
    },
 

    {
      path: '/cvandstuff',
      name: 'cvandstuff',
      component: CVandStuff
    },
    
    // {
    //   path: '/login',
    //   name: 'login',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/LogInView.vue')
    // }
  ]
})

export default router
