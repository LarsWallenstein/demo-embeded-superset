import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../components/DashBoard.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'DashBoard',
    component: Dashboard,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
