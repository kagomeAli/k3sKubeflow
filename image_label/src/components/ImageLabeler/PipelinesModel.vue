<template>
  <div>
    <div class="modal" tabindex="-1" :style="{ display: show ? 'block' : 'none' }">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">呼叫pipelines</h5>
          <button type="button" class="close" aria-label="Close" @click="switchModel">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="label-name" class="col-form-label">请输入身份标识符:</label>
            <input type="password" class="form-control -input-password-icon" name="label-name"
              v-model="name" >
            <label class="col-form-label" v-show="noticeTxt">错误标识符</label>
            <label class="col-form-label" v-show="noticePip">成功呼叫pipelines</label>
          </div>
          <div class="form-group">
            <label for="label-name" class="col-form-label">请选择呼叫的pipelines</label>
            <select class="form-control col-form-label" name="public-choice" v-model="pipeid">
              <option class="col-form-label"
                      :value="itm.id + ';' + itm.name"
                      :key="itm.id" v-for="itm in pipeline" >{{itm.name}}</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="switchModel">返回</button>
          <button type="button" class="btn btn-primary" @click="submit">确定</button>
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
      pipeinfo: '',
    };
  },
  computed: {
    show: function show() {
      return this.$attrs.switch === this.secondSwitch;
    },
  },
  created() {
    let pipeline = [];
    axios.get('http://127.0.0.1:30082/getList').then((res) => {
      if (res.status === 200) {
        pipeline = res.data.pipelines;
        this.pipeline = pipeline;
        this.pipename = pipeline[0].name;
        this.pipeid = pipeline[0].id;
        console.log('this.pipeline:', this.pipeline);
      }
    });
  },
  methods: {
    switchModel: function showModel() {
      this.secondSwitch = !this.secondSwitch;
    },
    submit: function submit() {
      const info = this.pipeinfo.split(';');
      if (this.name.length && this.pipeinfo) {
        axios.get(`http://127.0.0.1:30082/?id=${this.name}&pipeid=${info[0]}&pipename=${info[1]}`).then((res) => {
          if (res.data.status * 1 === 200) {
            console.log('成功');
            this.name = '';
            this.noticePip = true;
            setTimeout(() => { this.noticePip = false; this.name = ''; this.switchModel(); }, 3000);
          } else {
            console.log('失败');
            this.noticeTxt = true;
            setTimeout(() => { this.noticeTxt = false; this.name = ''; }, 3000);
          }
        });
      }
    },
    addLabel: function addLabel(name) {
      this.$store.commit('addLabel', name);
    },
  },
};
</script>
