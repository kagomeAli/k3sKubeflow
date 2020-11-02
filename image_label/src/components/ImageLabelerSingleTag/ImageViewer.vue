<template>
  <div class="position-relative">
    <img
      v-if="image !== null && image.imageReader !== null"
      :src="image.imageReader.result"
      style="height: 200px;"
      class="img-fluid rounded"
      draggable="false" />
    <div v-if="image !== null && image.imageReader !== null">
      {{image.imageReader.width}}, {{image.imageReader.height}}
    </div>
    <div
      v-show="image === null || image.imageReader === null"
      :style="{
        'height': `${imageHeight}px`,
      }">
      <span>請稍候...</span>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  name: 'ImageViewer',
  components: {
  },

  props: {
    image: {
      type: Object,
      default: null,
    },
  },

  mounted() {
    this.worker = this.$worker.create([
      {
        message: 'loadImage',
        func: (fileElement) => {
          // eslint-disable-next-line no-undef
          const fileReader = new FileReaderSync();

          return {
            path: fileElement.webkitRelativePath,
            result: fileReader.readAsDataURL(fileElement),
          };
        },
      },
    ]);

    this.renderImage();
    this.hookEvent();
  },

  beforeDestroy() {
    this.unHookEvent();
  },

  activated() {
    this.renderImage();
    this.hookEvent();
  },

  deactivated() {
    this.unHookEvent();
  },

  data() {
    return {
      worker: null,
      heightZoom: 1,
      widthZoom: 1,
      widthOffset: 0,
      imageHeight: 200,
    };
  },

  updated() {
    this.renderImage();
  },

  computed: {
  },

  watch: {
  },

  methods: {
    renderImage: function renderImage() {
      if (this.image.imageReader === null || this.image.imageReader.result === null) {
        this.worker.postMessage('loadImage', [this.image.htmlFileObject])
          .then((response) => {
            this.$store.commit('ImageLabelerSingleTag/setImageContent', response);
            this.$nextTick(() => {
              this.drawLabelRectangle();

              setTimeout(() => {
                const element = this.$el.querySelector('img');
                this.$store.commit('ImageLabelerSingleTag/setImageContentSize', {
                  path: this.image.path,
                  width: element.naturalWidth,
                  height: element.naturalHeight,
                });
              }, 500);
            });
          })
          // eslint-disable-next-line no-console
          .catch(console.error);
      } else {
        this.$nextTick(() => {
          this.drawLabelRectangle();
        });
      }
    },

    drawLabelRectangle: function drawLabelRectangle() {
      const element = this.$el.querySelector('img');
      const container = element.parentNode;

      this.widthOffset = (container.clientWidth - element.width) / 2;
      this.widthZoom = element.width / element.naturalWidth;
      this.heightZoom = element.height / element.naturalHeight;
    },

    handleMenuPush: function handleMenuPush() {
      setTimeout(() => {
        this.renderImage();
      }, 500);
    },

    hookEvent: function hookEvent() {
      window.addEventListener('resize', this.renderImage);
      $(document).on('shown.lte.pushmenu', this.handleMenuPush);
      $(document).on('collapsed.lte.pushmenu', this.handleMenuPush);
    },

    unHookEvent: function unHookEvent() {
      window.removeEventListener('resize', this.renderImage);
      $(document).off('shown.lte.pushmenu', this.handleMenuPush);
      $(document).off('collapsed.lte.pushmenu', this.handleMenuPush);
    },
  },
};
</script>

<style lang="scss" scoped>
.cover {
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
}

.label-box {
  border: solid rgb(82, 235, 82);
}
</style>
