<template>
  <div>
    <div class="modal" tabindex="-1" :style="{ display: show ? 'block' : 'none' }">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-center">呼叫pipelines</h5>
            <button type="button" class="close" aria-label="Close" @click="switchModel">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div >
            <div class="table-responsive">
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
                <tr class="active">
                  <td>{{pipeInfo.name }}</td>
                  <td>{{pipeInfo.status }}</td>
                  <td>{{pipeInfo.resource_references && pipeInfo.resource_references[1].name }}</td>
                  <td>{{pipeInfo.created_at}}</td>
                </tr>
                </tbody>
              </table>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="switchModel">返回</button>
            <button type="button" class="btn btn-primary" @click="refreshPipelines">刷新</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop show" :style="{ display: show ? 'block' : 'none' }"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      secondSwitch: true,
      noticeTxt: false,
      noticePip: false,
      pipeline: [],
      selectPipeline: '',
      pipename: '',
      pipeid: '',
      pipeInfo: {},
    };
  },
  computed: {
    show: function show() {
      return this.$attrs.switch === this.secondSwitch;
    },
  },
  mounted() {
    this.refreshPipelines(0);
  },
  methods: {
    switchModel: function showModel() {
      this.secondSwitch = !this.secondSwitch;
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
        this.$swal.showLoading();
      }
      axios.get('http://127.0.0.1:30082/allexp').then((res) => {
        this.$swal.hideLoading();
        console.log(res);
        if (res.data && res.data.name) {
          this.pipeInfo = res.data;
          console.log('成功');
        } else {
          console.log('失败');
          this.noticeTxt = true;
        }
      });
    },
    addLabel: function addLabel(name) {
      this.$store.commit('addLabel', name);
    },
  },
};
</script>
