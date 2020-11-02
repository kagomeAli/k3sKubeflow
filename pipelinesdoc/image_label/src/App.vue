<template>
  <div class="wrapper" id="app">
    <TopMenu />
    <LeftMenu />
    <!-- Content Wrapper. Contains page content -->
    <div class="content-wrapper">
      <!-- Main content -->
      <div class="content">
        <div class="container-fluid">
          <keep-alive>
              <router-view v-if="$route.meta.keepAlive" />
          </keep-alive>

          <router-view v-if="!$route.meta.keepAlive" />
        </div><!-- /.container-fluid -->
      </div><!-- /.content -->
    </div>
    <BottomMenu />
  </div>
</template>

<script>
import TopMenu from './components/TopMenu.vue';
import LeftMenu from './components/LeftMenu.vue';
import BottomMenu from './components/BottomMenu.vue';

export default {
  data() {
    return {
    };
  },

  components: {
    TopMenu,
    LeftMenu,
    BottomMenu,
  },

  computed: {
  },

  methods: {
  },
};
</script>

<style lang="scss">
  @import "main";
</style>
