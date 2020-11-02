import Vue from 'vue';
import VueRouter from 'vue-router';
import VueWorker from 'vue-worker';

Vue.use(VueRouter);
Vue.use(VueWorker);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue'),
  },
  {
    path: '/image-labeler',
    name: 'ImageLabeler',
    component: () => import(/* webpackChunkName: "ImageLabelerCore" */ '../views/ImageLabeler.vue'),
    meta: {
      keepAlive: true,
    },
  },
  {
    path: '/image-label-editor/:index/:path',
    name: 'ImageLabelEditor',
    props: true,
    component: () => import(/* webpackChunkName: "ImageLabelerCore" */ '../views/ImageLabelEditor.vue'),
  },
  {
    path: '/image-labeler-single-tag',
    name: 'ImageLabelerSingleTag',
    component: () => import(/* webpackChunkName: "ImageLabelerSingleTagCore" */ '../views/ImageLabelerSingleTag.vue'),
    meta: {
      keepAlive: true,
    },
  },
  {
    path: '/pipelines',
    name: 'Pipelines',
    component: () => import('../views/Pipelines.vue'),
    meta: {
      keepAlive: true,
    },
  },
];

const router = new VueRouter({
  linkActiveClass: 'active',
  routes,
});

export default router;
