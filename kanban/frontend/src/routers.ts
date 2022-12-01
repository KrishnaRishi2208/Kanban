import {createRouter, createWebHistory} from 'vue-router'
import Dashboard from './components/Dashboard.vue'
import Homepage from './components/Homepage.vue'
import Createlist from './components/Createlist.vue'
import Addcards from './components/Addcards.vue'
import Editlist from './components/Editlist.vue'
import Editcard from './components/Editcard.vue'
import Newuser from './components/Newuser.vue'


const routes=[
    {
        path:'/dashboard/:id',
        name:'Dashboard',
        component:Dashboard
    },
    {
        path:'/',
        name:'Home',
        component:Homepage
    },
    {
        path:'/createlist/:id',
        name:'Createlist',
        component:Createlist
    },
    {
        path:'/addcard/:lisnam/:id',
        name:'Addcards',
        component:Addcards
    },
    {
        path:'/editlist/:lname/:id',
        name:'Editlist',
        component:Editlist
    },
    {
        path:'/editcard/:id/:lisname/:cname/:date/:summary',
        name:'Editcard',
        component:Editcard
    },
    {
        path:'/newuser',
        name:'Newuser',
        component:Newuser
    }


]


const router=createRouter({
    history:createWebHistory(),
    routes,
}
)

export default router;