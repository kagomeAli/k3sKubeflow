<template>
  <div class="home row pt-2 text-center">
    <div class="title titlehei">
<!--      <div class="title text-center">
        最近10条pipeline状态
      </div>-->
      <div class="text-right">
        <button type="button" class="btn btn-primary" @click="refreshPipelines">
          刷新
        </button>
      </div>
    </div>
    <table class="table">
      <thead>
      <tr>
        <th>run name</th>
        <th>status</th>
        <th>pipeline version</th>
        <th>start time</th>
      </tr>
      </thead>
      <tbody>
      <tr class="active" v-for="(item,index) in dataList" v-bind:key="index">
        <td>{{item.name }}</td>
        <td>{{item.status }}</td>
        <td>{{item.resource_references && item.resource_references[1].name }}</td>
        <td>{{item.created_at}}</td>
      </tr>
      </tbody>
    </table>
    <nav aria-label="Page navigation" v-show="pipelineData.length">
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
import axios from 'axios';

export default {
  name: 'Pipelines',
  data() {
    return {
      pipelineData: [],
      page: 0,
      prePage: 10,
      prePageList: [10, 15, 20, 100],
    };
  },
  components: {
  },
  computed: {
    totalPages: function totalPages() {
      const pages = Math.ceil(this.pipelineData.length / this.prePage);
      return pages;
    },
    dataList: function images() {
      const start = (this.page * this.prePage);
      const end = ((this.page + 1) * this.prePage);
      const keys = this.pipelineData.slice(start, end);
      console.log('keys', keys);
      return keys;
    },
  },
  mounted() {
    this.refreshPipelines(0);
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
    refreshPipelines: function refreshPipelines(index = 2) {
      if (index) {
        this.$swal({
          title: '資料準備中',
          text: '請稍候...',
          icon: 'info',
          allowOutsideClick: false,
          allowEscapeKey: false,
        });
        this.pipelineData = [];
        this.$swal.showLoading();
      }
      axios.get('http://10.43.235.160:8882/allexp').then((res) => {
        this.$swal.hideLoading();
        console.log(res);
        if (res && res.status === 200) {
          this.pipelineData = res.data.pipelines;
          console.log('成功');
        } else {
          console.log('失败');
          this.noticeTxt = true;
        }
      });
    },
  },
};
</script>
<style lang="scss" scoped>
.titlehei {
  height: 50px;
  background-color: 'white';
  width: 100%;
  // line-height: 40px;
}
</style>
