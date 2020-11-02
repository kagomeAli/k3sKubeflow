<template>
  <div class="row noselect">
    <div class="col-2 pt-2 sticky-top right-menu" style="">
      <FileLoader />
      <button class="btn btn-danger btn-block mb-3" @click="showPipelinesModelSwitch">
          <i class="fas fa-brain"></i> 重新訓練
      </button>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            <i class="fas fa-file"></i> 檔案狀態
            <span class="badge bg-primary ml-1">
              {{ $store.getters['ImageLabelerSingleTag/getImageSize'] }}
            </span>
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
              v-for="(item, index) in $store.state.ImageLabelerSingleTag.labels" :key="index">
              <div class="input-group">
                <a href="#" class="form-control nav-link"
                  @click.prevent="selectedLabel = item.name"
                  :class="{'active': selectedLabel === item.name}">
                  <i class="fas fa-tag"></i> {{ item.name + ':' + item.num }}
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
    <SelectLabelModel :switch="$store.state.ImageLabelerSingleTag.showSelectLabelModel" />
    <RemoveLabelModel :switch="$store.state.ImageLabelerSingleTag.showRemoveLabelModel" />
    <PipelinesModel :switch="showPipelinesModel" />
  </div>
</template>

<script>
import ImageList from '../components/ImageLabelerSingleTag/ImageList.vue';
import LabelLoader from '../components/ImageLabelerSingleTag/LabelLoader.vue';
import AddLabelModel from '../components/ImageLabelerSingleTag/AddLabelModel.vue';
import SelectLabelModel from '../components/ImageLabelerSingleTag/SelectLabelModel.vue';
import RemoveLabelModel from '../components/ImageLabelerSingleTag/RemoveLabelModel.vue';
import PipelinesModel from '../components/ImageLabeler/PipelinesModel.vue';

export default {
  data() {
    return {
      selectedMode: 'all',
      selectedLabel: '所有',
      showAddLabelModel: false,
      showPipelinesModel: false,
    };
  },

  components: {
    ImageList,
    LabelLoader,
    FileLoader: () => import(/* webpackChunkName: "ImageLabelerSingleTagVendor" */ '../components/ImageLabelerSingleTag/FileLoader.vue'),
    AddLabelModel,
    SelectLabelModel,
    RemoveLabelModel,
    PipelinesModel,
  },

  computed: {
    preImageItems: function preImageItems() {
      const originList = this.$store.state.ImageLabelerSingleTag.images;
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
            if (LabelElement === this.selectedLabel) {
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
    showPipelinesModelSwitch: function showPipelinesModelSwitch() {
      this.showPipelinesModel = !this.showPipelinesModel;
    },
    showAddLabelModelSwitch: function showAddLabelModelSwitch() {
      this.showAddLabelModel = !this.showAddLabelModel;
    },

    removeLabel: function addLabel(name) {
      this.$store.commit('ImageLabelerSingleTag/removeLabel', name);
    },
  },
};
</script>
