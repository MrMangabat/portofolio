import { createRouter, createWebHistory } from 'vue-router'

import ResearchView from '../views/ResearchView.vue'
import AboutView from '../views/AboutView.vue'
// import LogInView from '../views/LogInView.vue'
import ProjectsOverview from '../views/ProjectsOverview.vue'
import JobSearch from '../views/JobSearch.vue'
import PersonalTraining from '../views/PersonalTraining.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/research',
      name: 'Knowledge HUB',
      component: ResearchView
    },
 
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    
    {
      path: '/projectsoverview',
      name: 'projectsoverview',
      component: ProjectsOverview
    },

    {
      path: '/jobsearch',
      name: 'jobsearch',
      component: JobSearch
    },
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: LogInView

    // },
    {
      path: '/personaltraining',
      name: 'personaltraining',
      component: PersonalTraining
    }, 
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
