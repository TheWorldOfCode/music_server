import {createRouter, createWebHistory} from 'vue-router'
import YoutubeDownloader from '../components/YoutubeDownloader.vue';
import MusicLibrary from '../components/MusicLibrary.vue';

export default new createRouter({
    history: createWebHistory(),
    routes:[
        {
            path:'/youtube',
            name:'YoutubeDownloader',
            component: YoutubeDownloader,
        }, 
        {
            path: "/library",
            name: "MusicLibrary",
            component: MusicLibrary

        },
        {
            path: "/",
            redirect: "/library"
        }
            
    ],
})