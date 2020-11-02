<template>
  <div class="row noselect">
    <div class="col-2 sticky-top right-menu">
      <div class="card mt-3">
        <div class="card-body">
          <div class="row">
            <div class="col">
              <button class="btn btn-default btn-block" @click="previousPage">
                <i class="fas fa-arrow-left"></i> 上一張
              </button>
            </div>
            <div class="col">
              <button class="btn btn-default btn-block" @click="nextPage">
                下一張 <i class="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="card mt-3">
        <div class="card-body">
          <button class="btn btn-default btn-block"
            @click="$router.push('/image-labeler')"><i class="fas fa-undo"></i> 放棄修改並回到列表</button>
          <button class="btn btn-info btn-block" @click="scale += 2">
            <i class="fas fa-search-plus"></i> 放大
          </button>
          <button class="btn btn-info btn-block"
            @click="((scale - 2) > 1) ? scale -= 2 : scale = 2">
            <i class="fas fa-search-minus"></i> 縮小
          </button>
          <button class="btn btn-success btn-block" @click="save">
            <i class="fas fa-save"></i> 儲存
          </button>
          <button class="btn btn-success btn-block" @click="saveAndBack">
            <i class="fas fa-save"></i> 儲存並回到列表
          </button>
        </div>
      </div>
      <div class="card mt-3">
        <div class="card-header">
          <h3 class="card-title">標籤</h3>

          <div class="card-tools">
            <button type="button" class="btn btn-tool" data-card-widget="collapse">
              <i class="fas fa-minus"></i>
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <ul class="nav nav-pills flex-column">
            <li class="nav-item" v-for="(item, index) in labels" :key="'labels' + index">
              <div class="input-group">
                <div class="input-group-prepend" @click="changeLabelColor(item)">
                  <span class="input-group-text" :style="{'background-color': item.color}">
                    <i class="far fa-circle" :style="{'color': item.color}"></i>
                  </span>
                </div>
                <select class="form-control" v-model="item.name">
                  <option
                    :value="item.name">
                    {{ item.name }}
                  </option>
                  <option disabled>--------</option>
                  <option v-for="(item, index) in $store.state.ImageLabeler.labels"
                    :key="index"
                    :value="item">
                    {{ item }}
                  </option>
                </select>
                <div class="input-group-append">
                  <span class="input-group-text" @click.prevent="removeLabel(index)">
                    <i class="fas fa-trash text-danger"></i>
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col-10 mt-1">
      檔案位置：<span>{{ meta.path }}</span>
      <hr>
      <span class="mr-2">滑鼠位置：[{{ Math.round(mouseX) }}, {{ Math.round(mouseY) }}]</span>
      <span class="mr-2">圖片縮放： x{{ zoom }}</span>
      <span class="mr-2">
        圖片寬高：
        [{{ Math.round(Number.parseFloat(imageSize.width)) }},
         {{ Math.round(Number.parseFloat(imageSize.height)) }}]
      </span>
      <span class="mr-2">圖片原始寬高：[{{ imageWidth }}, {{ imageHeight }}]</span>
      <!-- <span class="mr-2" v-if="viewerBounding">
        圖片基準：[{{ viewerBounding.x }}, {{ viewerBounding.y }}]</span> -->
      <hr>
      <div>
        <div class="position-relative align-middle overflow-hidden"
          :style="imageSize">
          <img v-if="image" class="img-fluid cover" :src="image.src" />
          <div class="position-absolute cover"
            @mousemove="mouseMove"
            @mousedown="mouseClick"
            @mouseup="mouseRelease">
            <!--:style="lineXPosition"  :style="lineYPosition"-->
            <div class="position-absolute line1" ></div>
            <div class="position-absolute line2" ></div>
            <div v-for="(item, index) in labels" :key="index"
              class="position-absolute label-box"
              :style="{
                'top': (item.ty * zoom) + 'px',
                'left': (item.lx * zoom) + 'px',
                'height': ((item.by - item.ty) * zoom) + 'px',
                'width': ((item.rx - item.lx) * zoom) + 'px',
                'border-color': item.color,
              }">
              <span class="pr-1"
                :style="{'color': item.color, 'position': 'relative', 'top': '-27px'}">
                {{ item.name }} <br />
                <!-- [[{{ item.lx}}, {{ item.ty }}], [{{ item.rx }}, {{ item.by }}]] -->
              </span>
            </div>
            <div v-show="isClickDown"
              class="position-absolute label-box overflow-hidden"
              :style="{
                'top': (newLabel.ty * zoom) + 'px',
                'left': (newLabel.lx * zoom) + 'px',
                'height': ((newLabel.by - newLabel.ty) * zoom) + 'px',
                'width': ((newLabel.rx - newLabel.lx) * zoom) + 'px',
              }">New</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  data() {
    return {
      indxe: 0,
      meta: {},
      image: null,
      imageName: '',
      imageHeight: 0,
      imageWidth: 0,
      mousePageX: 0,
      mousePageY: 0,
      isClickDown: false,
      newLabelStartPoint: {
        x: 0,
        y: 0,
      },
      newLabel: {
        lx: 0, // left-x
        ty: 0, // top-y
        rx: 0, // right-x
        by: 0, // bottom-y
      },
      scale: 10,
      /**
       * @type {?DOMRect}
       */
      viewer: null,
      viewerBounding: null,
      labels: [
        // {
        //   name: 'test',
        //   lx: 100,
        //   ty: 100,
        //   rx: 150,
        //   by: 200,
        // },
      ],
    };
  },

  beforeRouteUpdate(to, from, next) {
    this.$nextTick(async () => {
      await this.reset();
      await this.init(2);
    });
    next();
  },

  mounted() {
    this.init(1);
    this.hookEvent();
  },

  beforeDestroy() {
    this.unHookEvent();
  },

  computed: {
    imageSize: function imageSize() {
      return {
        height: `${this.imageHeight * this.zoom}px`,
        width: `${this.imageWidth * this.zoom}px`,
      };
    },

    lineXPosition: function lineXPosition() {
      return {
        left: `${this.mouseX * this.zoom - 3}px`,
      };
    },

    lineYPosition: function lineYPosition() {
      return {
        top: `${this.mouseY * this.zoom - 3}px`,
      };
    },

    mouseX: function mouseX() {
      if (this.viewerBounding === null) {
        return 0;
      }

      if (this.mousePageX - this.viewerBounding.x > 0) {
        return Math.round((this.mousePageX - this.viewerBounding.x) / this.zoom);
      }

      return 0;
    },

    mouseY: function mouseY() {
      if (this.viewerBounding === null) {
        return 0;
      }

      if (this.mousePageX - this.viewerBounding.x > 0) {
        return Math.round((this.mousePageY - this.viewerBounding.y) / this.zoom);
      }

      return 0;
    },

    zoom: function zoom() {
      return this.scale / 10;
    },
  },

  methods: {
    init: function init(flag) {
      const instance = this;
      const image = new Image();
      const { item } = this.$attrs;
      // const itemName = this.$store.getters.getImageKeys[this.$attrs.index];
      // const item = this.$store.state.ImageLabeler.images[itemName];
      console.log(flag);
      console.log(item);
      if (item === undefined) {
        this.$swal({
          icon: 'error',
          text: '無法取得圖片資源，請確認是否已匯入圖片。',
        });
        this.$router.push('/image-labeler');
        return;
      }

      image.onload = function imageOnload() {
        instance.imageHeight = this.height;
        instance.imageWidth = this.width;

        instance.image = image;
        instance.updateViewBounding();
        instance.scale = Math.floor((600 / this.height) * 10);
      };

      image.src = item.imageReader.result;
      this.imageName = item.name;

      if (item.labels.length > 0) {
        const labels = JSON.parse(JSON.stringify(item.labels));
        for (let index = 0; index < labels.length; index += 1) {
          const element = labels[index];
          if (element.color === null) {
            element.color = this.getRandomColor();
          }
        }
        this.labels = labels;
      }
      this.meta = item;
    },

    save: function save() {
      const item = { ...this.meta };

      item.imageReader.height = this.imageHeight;
      item.imageReader.width = this.imageWidth;

      this.$store.commit('setImage', {
        ...item,
        labels: this.labels,
        // htmlObject: fileElement,
      });
      this.$swal({
        icon: 'success',
        text: '存檔完成！',
      });
    },

    saveAndBack: function save() {
      this.save();
      this.$router.push('/image-labeler');
    },

    /**
     * @param {MouseEvent} event
     */
    mouseMove: function mouseMove(event) {
      this.mousePageX = event.pageX;
      this.mousePageY = event.pageY;

      if (this.isClickDown) {
        if (this.newLabelStartPoint.x > this.mouseX) {
          this.newLabel.lx = this.mouseX;
          this.newLabel.rx = this.newLabelStartPoint.x;
        } else {
          this.newLabel.lx = this.newLabelStartPoint.x;
          this.newLabel.rx = this.mouseX;
        }

        if (this.newLabelStartPoint.y > this.mouseY) {
          this.newLabel.ty = this.mouseY;
          this.newLabel.by = this.newLabelStartPoint.y;
        } else {
          this.newLabel.ty = this.newLabelStartPoint.y;
          this.newLabel.by = this.mouseY;
        }
      }
    },

    /**
     * @param {MouseEvent} event
     */
    mouseClick: function mouseClick() {
      this.newLabel = {
        lx: this.mouseX,
        ty: this.mouseY,
        rx: this.mouseX,
        by: this.mouseY,
      };
      this.newLabelStartPoint.x = this.mouseX;
      this.newLabelStartPoint.y = this.mouseY;
      this.isClickDown = true;
    },

    /**
     * @param {MouseEvent} event
     */
    mouseRelease: function mouseRelease() {
      this.isClickDown = false;
      this.labels.push({
        name: 'New',
        color: this.getRandomColor(),
        ...this.newLabel,
      });
    },

    getRandomColor: function getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i += 1) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },

    changeLabelColor: function changeLabelcolor(item, value) {
      const label = item;
      if (typeof value === 'string') {
        label.color = value;
      } else {
        label.color = this.getRandomColor();
      }
    },

    removeLabel: function removeLabel(index) {
      if (this.labels.length > index) {
        this.labels.splice(index, 1);
      }
    },

    previousPage: function previousPage() {
      const previousPageNumber = this.$attrs.index - 1;
      if (previousPageNumber < 0) {
        return;
      }
      const previousPageName = this.$store.getters.getImageKeys[previousPageNumber];
      const previousPageImage = this.$store.state.ImageLabeler.images[previousPageName];

      this.$router.push({
        name: 'ImageLabelEditor',
        params: {
          path: previousPageImage.path,
          index: previousPageNumber,
          item: previousPageImage,
        },
      });
    },

    nextPage: function nextPage() {
      const nextPageNumber = this.$attrs.index + 1;
      const nextPageName = this.$store.getters.getImageKeys[nextPageNumber];
      const nextPageImage = this.$store.state.ImageLabeler.images[nextPageName];

      this.$router.push({
        name: 'ImageLabelEditor',
        params: {
          item: nextPageImage,
          path: nextPageImage.path,
          index: nextPageNumber,
        },
      });
    },

    reset: function reset() {
      Object.assign(this.$data, {
        image: null,
        imageName: '',
        imageHeight: 0,
        imageWidth: 0,
        mousePageX: 0,
        mousePageY: 0,
        isClickDown: false,
        labels: [],
      });
    },

    updateViewBounding: function updateViewBounding() {
      this.viewer = this.$el.querySelector('.position-relative');
      this.viewerBounding = this.viewer.getBoundingClientRect();
    },

    handleMenuPush: function handleMenuPush() {
      setTimeout(() => {
        this.updateViewBounding();
      }, 500);
    },

    hookEvent: function hookEvent() {
      window.addEventListener('resize', this.updateViewBounding);
      $(document).on('shown.lte.pushmenu', this.handleMenuPush);
      $(document).on('collapsed.lte.pushmenu', this.handleMenuPush);
    },

    unHookEvent: function unHookEvent() {
      window.removeEventListener('resize', this.updateViewBounding);
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

.line1 {
  left: -6px;
  height: 100%;
  width: 6px;
  background-color: red;
  opacity: 0.5;
}

.line2 {
  top: -6px;
  height: 6px;
  width: 100%;
  background-color: red;
  opacity: 0.5;
}

.label-box {
  border: solid green;
}
</style>
