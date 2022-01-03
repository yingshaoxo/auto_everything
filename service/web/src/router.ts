import { createRouter, createWebHashHistory } from 'vue-router'

import { pageIdentity, globalDict } from "./store/memory"

import HomePage from './pages/HomePage.vue'
import VideoPage from './pages/VideoPage.vue'

const routes = [
    { path: pageIdentity.homePage, component: HomePage },
    { path: pageIdentity.videoPage, component: VideoPage },
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})