<template>
  <div>
    <div class="modal" tabindex="-1" :style="{ display: show ? 'block' : 'none' }">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">移除標籤</h5>
          <button type="button" class="close" aria-label="Close" @click="switchModel">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          確定是否要移除已選擇圖片的標籤？
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="switchModel">取消</button>
          <button type="button" class="btn btn-danger" @click="submit">移除</button>
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
    };
  },
  computed: {
    show: function show() {
      return this.$attrs.switch;
    },
  },
  methods: {
    switchModel: function showModel() {
      this.$store.commit('ImageLabelerSingleTag/switchRemoveLabelModel');
    },

    submit: function submit() {
      this.removeLabel();
      this.switchModel();
      this.selected = '';
    },

    removeLabel: function removeLabel() {
      const selectedImages = this.$store.getters['ImageLabelerSingleTag/getSelectedImages'];
      const selectedImageKeys = Object.keys(selectedImages);

      for (let index = 0; index < selectedImageKeys.length; index += 1) {
        const element = { ...selectedImages[selectedImageKeys[index]] };

        element.labels = [];

        this.$store.commit('ImageLabelerSingleTag/setImage', element);
      }
    },
  },
};
</script>
