import Vue from 'vue';
import Vuex from 'vuex';
import ImageLabeler from './modules/imageLabeler';
import ImageLabelerSingleTag from './modules/imageLabelerSingleTag';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    ImageLabeler,
    ImageLabelerSingleTag,
  },
  strict: process.env.NODE_ENV !== 'production',
});
