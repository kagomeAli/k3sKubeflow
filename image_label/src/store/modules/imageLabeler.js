import Vue from 'vue';

// initial state
// shape: [{}]
const moduleState = {
  images: {},
  xmlData: {},
  labels: [],
};

// getters
const moduleGetters = {
  // eslint-disable-next-line no-unused-vars
  getImageSize(state, getters, rootState) {
    return Object.keys(state.images).length;
  },
  // eslint-disable-next-line no-unused-vars
  getImageKeys(state, getters, rootState) {
    // TODO: maybe browser is sorted it.
    // return Object.keys(state.images).sort((a, b) => a.localeCompare(b));
    return Object.keys(state.images);
  },
  // eslint-disable-next-line no-unused-vars
  getLabelsDistinct(state, getters, rootState) {
    const labels = [];
    Object.keys(state.images).forEach((element) => {
      for (let index = 0; index < state.images[element].labels.length; index += 1) {
        const label = state.images[element].labels[index].name;
        labels.push(label);
      }
    });

    return labels.filter((value, index, self) => self.indexOf(value) === index).sort();
  },
};

// actions
const actions = {
};

// mutations
const mutations = {
  setImage(state, payload) {
    Vue.set(state.images, payload.path, payload);
  },

  setImages(state, payload) {
    state.images = { ...state.images, ...payload };
  },

  setImageContent(state, payload) {
    const element = state.images[payload.path];
    Vue.set(state.images, payload.path, {
      ...element,
      imageReader: {
        ...element.imageReader,
        result: payload.result,
      },
    });
  },

  setImageContentSize(state, payload) {
    const element = state.images[payload.path];
    Vue.set(state.images, payload.path, {
      ...element,
      imageReader: {
        ...element.imageReader,
        width: payload.width,
        height: payload.height,
      },
    });
  },

  clearImages(state) {
    state.images = {};
  },

  setXmlData(state, payload) {
    Vue.set(state.xmlData, payload.path, payload);
  },

  clearXmlData(state) {
    state.xmlData = {};
  },

  addLabel(state, payload) {
    if (state.labels.indexOf(payload) < 0) {
      state.labels.push(payload);
    }
  },

  removeLabel(state, payload) {
    if (state.labels.length > payload) {
      state.labels.splice(payload, 1);
    }
  },
};

export default {
  namespaced: false,
  state: moduleState,
  getters: moduleGetters,
  actions,
  mutations,
};
