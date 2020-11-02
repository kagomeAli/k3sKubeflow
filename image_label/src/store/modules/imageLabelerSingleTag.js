import Vue from 'vue';

// initial state
// shape: [{}]
const moduleState = {
  images: {},
  jsonData: {},
  labels: [],
  showSelectLabelModel: false,
  showRemoveLabelModel: false,
};

// getters
const moduleGetters = {
  // eslint-disable-next-line no-unused-vars
  getImageSize(state, getters, rootState) {
    return Object.keys(state.images).length;
  },

  // eslint-disable-next-line no-unused-vars
  getImageKeys(state, getters, rootState) {
    return Object.keys(state.images);
  },

  countSelected(state) {
    const keys = Object.keys(state.images);
    let counter = 0;
    for (let index = 0; index < keys.length; index += 1) {
      const element = state.images[keys[index]];
      if (element.selected) {
        counter += 1;
      }
    }
    return counter;
  },

  getSelectedImages(state) {
    const keys = Object.keys(state.images);
    const selected = {};
    for (let index = 0; index < keys.length; index += 1) {
      const element = state.images[keys[index]];
      if (element.selected) {
        Vue.set(selected, element.path, element);
      }
    }
    return selected;
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

  setJsonData(state, payload) {
    Vue.set(state.jsonData, payload.path, payload);
  },

  setJsonDatas(state, payload) {
    state.jsonData = { ...state.jsonData, ...payload };
  },

  clearJsonData(state) {
    state.jsonData = {};
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

  setSelected(state, payload) {
    const element = state.images[payload.path];
    Vue.set(state.images, payload.path, {
      ...element,
      selected: payload.selected,
    });
  },

  setSelectedAll(state, payload) {
    Object.keys(state.images).forEach((key) => {
      if (Object.prototype.hasOwnProperty.call(state.images, key)) {
        const element = state.images[key];
        element.selected = payload;
      }
    });
  },

  switchSelectLabelModel(state) {
    state.showSelectLabelModel = !state.showSelectLabelModel;
  },

  switchRemoveLabelModel(state) {
    state.showRemoveLabelModel = !state.showRemoveLabelModel;
  },
};

export default {
  namespaced: true,
  state: moduleState,
  getters: moduleGetters,
  actions,
  mutations,
};
