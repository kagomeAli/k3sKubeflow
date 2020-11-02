<template>
  <div>
    <div class="modal" tabindex="-1" :style="{ display: show ? 'block' : 'none' }">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">設置標籤</h5>
          <button type="button" class="close" aria-label="Close" @click="switchModel">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="label-name" class="col-form-label">標籤：</label>
            <select class="form-control" v-model="selected">
              <option v-for="(item, index) in this.$store.state.ImageLabelerSingleTag.labels"
                :key="index">{{ item.name }}</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="switchModel">取消</button>
          <button type="button" class="btn btn-primary" @click="submit">設置</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal-backdrop show" :style="{ display: show ? 'block' : 'none' }"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selected: {},
    };
  },
  computed: {
    show: function show() {
      return this.$attrs.switch;
    },
  },
  methods: {
    switchModel: function showModel() {
      this.$store.commit('ImageLabelerSingleTag/switchSelectLabelModel');
    },

    submit: function submit() {
      if (this.selected.length > 0) {
        this.addLabel();
      }
      this.switchModel();
      this.selected = {};
    },

    addLabel: function addLabel() {
      const selectedImages = this.$store.getters['ImageLabelerSingleTag/getSelectedImages'];
      const selectedImageKeys = Object.keys(selectedImages);

      for (let index = 0; index < selectedImageKeys.length; index += 1) {
        const element = { ...selectedImages[selectedImageKeys[index]] };

        element.labels = [this.selected];

        this.$store.commit('ImageLabelerSingleTag/setImage', element);
      }
    },
  },
};
</script>
