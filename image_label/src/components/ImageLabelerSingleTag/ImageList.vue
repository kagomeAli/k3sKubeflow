<template>
  <div class="home pt-2">
    <div v-show="$store.getters['ImageLabelerSingleTag/getImageSize'] == 0">
      <h3>請先匯入圖片</h3>
    </div>
    <div class="row" v-if="images.length > 0">
      <div class="col-12 pb-2">
        <div class="card">
          <div class="card-body">
            <span class="badge badge-secondary">
              {{ $store.getters['ImageLabelerSingleTag/countSelected'] }}
            </span> 張 圖片已選擇 ｜
            <button class="btn btn-success" @click="switchSelectLabelModel">設置標籤</button> |
            <button class="btn btn-danger" @click="switchRemoveLabelModel">移除標籤</button>
            | <button class="btn btn-secondary" @click="selectAllImage(true)">全部選取</button>
            | <button class="btn btn-secondary" @click="selectAllImage(false)">取消選取</button>
          </div>
        </div>
      </div>
    </div>
    <div class="row" v-if="images.length > 0">
      <div class="col-3 pb-2"
        v-for="(item, index) in images" :key="`ListImage${index}`">
        <div class="card">
          <div class="card-header"
            @click="switchSelected(item, index)"
            :class="{'bg-primary': item.selected}"
            style="overflow:hidden; white-space: nowrap; text-overflow: ellipsis; cursor: pointer;">
            <i class="fas fa-check-circle" v-if="item.selected"></i>
            <i class="far fa-circle" v-if="!item.selected"></i>
            {{ item.path }}
          </div>
          <div class="card-body text-center" @click="switchSelected(item, index)"
            style="cursor: pointer;">
            <ImageView :image="item"/>
          </div>
          <div class="card-footer d-flex" style="overflow-x: scroll;">
            <div class="mr-1"><i class="fas fa-tag"></i></div>
            <div v-for="(labelItem, labelIndex) in item.labels" class="mr-1 h4"
              :key="`label-${index}-${labelIndex}`">
              <span class="badge badge-secondary">{{ labelItem }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <nav aria-label="Page navigation" v-show="images.length">
      <ul class="pagination">
        <li class="page-item">
          <a class="page-link" href="#" @click.prevent="previousPage">上一頁</a>
        </li>
        <li class="page-item">
          <select class="form-control" v-model="prePage">
            <option
              :value="prePage">
              每頁 {{ prePage }} 個
            </option>
            <option disabled>--------</option>
            <option v-for="(item, index) in prePageList"
              :key="index"
              :value="item">
              每頁 {{ item }} 個
            </option>
          </select>
        </li>
        <li class="page-item">
          <select class="form-control" v-model="page">
            <option
              :value="page">
              第 {{ page + 1 }} 頁
            </option>
            <option disabled>--------</option>
            <option v-for="(item, index) in totalPages"
              :key="index"
              :value="item - 1">
              第 {{ item }}頁
            </option>
          </select>
        </li>
        <li class="page-item">
          <a class="page-link" href="#" @click.prevent="nextPage">下一頁</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import ImageView from './ImageViewer.vue';

export default {
  name: 'ImageList',

  components: {
    ImageView,
  },

  mounted() {
  },

  data() {
    return {
      page: 0,
      prePage: 24,
      prePageList: [4, 8, 12, 24, 48],
      worker: null,
    };
  },

  computed: {
    totalPages: function totalPages() {
      const keys = Object.keys(this.$attrs.images);
      const pages = Math.ceil(keys.length / this.prePage);
      return pages;
    },

    images: function images() {
      const start = (this.page * this.prePage);
      const end = ((this.page + 1) * this.prePage);
      const keys = Object.keys(this.$attrs.images).slice(start, end);
      const list = [];

      for (let index = 0; index < keys.length; index += 1) {
        const element = keys[index];
        list.push(this.$attrs.images[element]);
      }

      return list;
    },
  },

  methods: {
    previousPage: function previousPage() {
      if (this.page > 0) {
        this.page -= 1;
      }
    },

    nextPage: function nextPage() {
      if (this.page < this.totalPages - 1) {
        this.page += 1;
      }
    },

    switchSelected: function gotoEdiort(item) {
      this.$store.commit('ImageLabelerSingleTag/setSelected', {
        ...item,
        selected: !item.selected,
      });
    },

    switchSelectLabelModel: function switchSelectLabelModel() {
      this.$store.commit('ImageLabelerSingleTag/switchSelectLabelModel');
    },

    switchRemoveLabelModel: function switchRemoveLabelModel() {
      this.$store.commit('ImageLabelerSingleTag/switchRemoveLabelModel');
    },

    selectAllImage: function selectAllImage(payload) {
      this.$store.commit('ImageLabelerSingleTag/setSelectedAll', payload);
    },
  },
};
</script>
