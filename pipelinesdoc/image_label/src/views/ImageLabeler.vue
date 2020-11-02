<template>
  <div class="row noselect">
    <div class="col-2 pt-2 sticky-top right-menu" style="">
      <FileLoader />
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            <i class="fas fa-file"></i> 檔案狀態
            <span class="badge bg-primary ml-1">{{ $store.getters.getImageSize }}</span>
          </h3>

          <div class="card-tools">
            <button type="button" class="btn btn-tool" data-card-widget="collapse">
              <i class="fas fa-minus"></i>
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <ul class="nav nav-pills flex-column">
            <li class="nav-item">
              <a href="#" class="nav-link" :class="{'active': selectedMode === 'all'}"
                @click.prevent="selectedMode = 'all'">
                <i class="fas fa-check-double fa-fw"></i> 所有圖片
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link" :class="{'active': selectedMode === 'tagged'}"
                @click.prevent="selectedMode = 'tagged'">
                <i class="fas fa-check-square fa-fw"></i> 已加標籤
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link" :class="{'active': selectedMode === 'untagged'}"
                @click.prevent="selectedMode = 'untagged'">
                <i class="fas fa-inbox fa-fw"></i> 未加標籤
              </a>
            </li>
          </ul>
        </div>
        <!-- /.card-body -->
      </div>
      <button class="btn btn-success btn-block mb-3" @click="showAddLabelModelSwitch">
          <i class="fas fa-plus"></i> 新增標籤
      </button>
      <LabelLoader />
      <div class="card">
        <div class="card-header">
          <h3 class="card-title"><i class="fas fa-tags"></i> 標籤</h3>

          <div class="card-tools">
            <button type="button" class="btn btn-tool" data-card-widget="collapse">
              <i class="fas fa-minus"></i>
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <ul class="nav nav-pills flex-column">
            <li class="nav-item">
              <a href="#" class="nav-link" @click.prevent="selectedLabel = '所有'"
                :class="{'active': selectedLabel === '所有'}">
                <i class="fas fa-check-double text-success"></i> 所有
              </a>
            </li>
            <li class="nav-item"
              v-for="(item, index) in $store.state.ImageLabeler.labels" :key="index">
              <div class="input-group">
                <a href="#" class="form-control nav-link"
                  @click.prevent="selectedLabel = item"
                  :class="{'active': selectedLabel === item}">
                  <i class="fas fa-tag"></i> {{ item }}
                </a>
                <div class="input-group-append">
                  <span class="input-group-text" @click.prevent="removeLabel(index)">
                    <i class="fas fa-trash text-danger"></i>
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <!-- /.card-body -->
      </div>
    </div>
    <div class="col-10">
      <ImageList :images="imageItems" />
    </div>
    <AddLabelModel :switch="showAddLabelModel" />
  </div>
</template>

<script>
import ImageList from '../components/ImageLabeler/ImageList.vue';
import LabelLoader from '../components/ImageLabeler/LabelLoader.vue';
import AddLabelModel from '../components/ImageLabeler/AddLabelModel.vue';

export default {
  data() {
    return {
      selectedMode: 'all',
      selectedLabel: '所有',
      showAddLabelModel: false,
    };
  },

  components: {
    ImageList,
    LabelLoader,
    FileLoader: () => import(/* webpackChunkName: "ImageLabelerVendor" */ '../components/ImageLabeler/FileLoader.vue'),
    AddLabelModel,
  },

  computed: {
    preImageItems: function preImageItems() {
      const originList = this.$store.state.ImageLabeler.images;
      const filePath = [];
      const list = [];

      switch (this.selectedMode) {
        case 'tagged':
          Object.keys(originList).forEach((element) => {
            const item = originList[element];
            if (item.labels.length > 0) {
              if (filePath.indexOf(item.path) < 0) {
                list.push(item);
                filePath.push(item.path);
              }
            }
          });
          break;

        case 'untagged':
          Object.keys(originList).forEach((element) => {
            const item = originList[element];
            if (item.labels.length === 0) {
              if (filePath.indexOf(item.path) < 0) {
                list.push(item);
                filePath.push(item.path);
              }
            }
          });
          break;

        default:
          Object.keys(originList).forEach((element) => {
            const item = originList[element];
            list.push(item);
            filePath.push(item.path);
          });
          break;
      }
      return list;
    },
    imageItems: function imageItems() {
      const originList = this.preImageItems;
      const filePath = [];
      let list = [];

      if (this.selectedLabel !== '所有') {
        for (let index = 0; index < originList.length; index += 1) {
          const item = originList[index];
          let passFlag = false;
          for (let labelIndex = 0; labelIndex < item.labels.length; labelIndex += 1) {
            const LabelElement = item.labels[labelIndex];
            if (LabelElement.name === this.selectedLabel) {
              passFlag = true;
              break;
            }
          }
          if (passFlag) {
            if (filePath.indexOf(item.path) < 0) {
              list.push(item);
              filePath.push(item.path);
            }
          }
        }
      } else {
        list = originList;
      }

      return list;
    },
  },

  methods: {
    showAddLabelModelSwitch: function showAddLabelModelSwitch() {
      this.showAddLabelModel = !this.showAddLabelModel;
    },

    removeLabel: function addLabel(name) {
      this.$store.commit('removeLabel', name);
    },
  },
};
</script>
