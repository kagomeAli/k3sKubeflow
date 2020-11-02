<template>
  <div>
    <div class="modal" tabindex="-1" :style="{ display: show ? 'block' : 'none' }">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">新增</h5>
          <button type="button" class="close" aria-label="Close" @click="switchModel">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="label-name" class="col-form-label">標籤：</label>
            <input type="text" class="form-control" name="label-name"
              v-model="name" @keypress.enter="submit">
          </div>
          <div class="form-group">
            <label for="label-num" class="col-form-label">数值：</label>
            <input type="text" class="form-control" name="label-num"
                   v-model="num">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="switchModel">取消</button>
          <button type="button" class="btn btn-primary" @click="submit">增加</button>
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
      name: '',
      num: '',
      secondSwitch: true,
    };
  },
  computed: {
    show: function show() {
      return this.$attrs.switch === this.secondSwitch;
    },
  },
  methods: {
    switchModel: function showModel() {
      this.secondSwitch = !this.secondSwitch;
    },
    submit: function submit() {
      if (this.name.length > 0 && this.num) {
        this.addLabel({ name: this.name, num: this.num });
      }
      this.switchModel();
      this.name = '';
      this.num = '';
    },
    addLabel: function addLabel(name) {
      this.$store.commit('ImageLabelerSingleTag/addLabel', name);
    },
  },
};
</script>
