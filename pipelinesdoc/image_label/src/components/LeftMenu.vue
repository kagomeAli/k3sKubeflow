<template>
  <!-- Main Sidebar Container -->
  <aside class="main-sidebar sidebar-dark-primary elevation-4">
    <!-- Brand Logo -->
    <router-link to="/" class="brand-link">
      <img src="../assets/logo-mini.png"
        alt="Logo-Mini"
        class="brand-image img-circle elevation-3"
        style="opacity: 1">
      <span class="brand-text font-weight-light">資訊工業策進會</span>
    </router-link>

    <!-- Sidebar -->
    <div class="sidebar">
      <!-- Sidebar Menu -->
      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column"
          data-widget="treeview"
          role="menu"
          data-accordion="false">
          <li class="nav-item has-treeview">
            <router-link to="/" class="nav-link" exact="">
              <i class="nav-icon fas fa-home"></i>
              <p>
                首頁
              </p>
            </router-link>
          </li>
          <li v-show="false" class="nav-item has-treeview">
            <router-link to="/image-labeler" class="nav-link">
              <i class="nav-icon fas fa-tags"></i>
              <p>
                影像標註工具
              </p>
            </router-link>
          </li>
          <li class="nav-item has-treeview">
            <router-link to="/image-labeler-single-tag" class="nav-link">
              <i class="nav-icon fas fa-tag"></i>
              <p>
                影像單一類別標註工具
              </p>
            </router-link>
          </li>
          <li class="nav-item has-treeview">
            <router-link to="/pipelines" class="nav-link">
              <i class="nav-icon fas fa-tag"></i>
              <p>
                Pipelines 运行状态列表
              </p>
            </router-link>
          </li>
        </ul>
      </nav>
      <!-- /.sidebar-menu -->
    </div>
    <!-- /.sidebar -->
  </aside>
</template>
