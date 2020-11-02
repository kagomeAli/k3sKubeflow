<template>
  <div>
    <input style="display: none" type="file" webkitdirectory mozdirectory @change="loadFolder"/>
    <button class="btn btn-primary btn-block mb-3"
      @click="selectFolder"
      :disabled="isLoading">
        <span class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
          v-show="isLoading" />
        <i class="fas fa-folder-open" v-show="!isLoading"></i> 匯入圖片資料夾
    </button>
    <button class="btn btn-success btn-block mb-3"
      @click="exportJsonFiles"
      :disabled="isLoading">
        <span class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
          v-show="isLoading" />
        <i class="fas fa-download" v-show="!isLoading"></i> 匯出JSON記錄
    </button>
    <button class="btn btn-success btn-block mb-3"
            @click="upZip"
            :disabled="isLoading">
        <span class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
              v-show="isLoading" />
      <i class="fas fa-fan" v-show="!isLoading"></i> 解压lable文件
    </button>
    <div class="progress mt-1 mb-2" v-show="isLoading || true">
      <div class="progress-bar bg-info"
        role="progressbar"
        :style="{'width': loadingPercent}" />
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import _ from 'lodash';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import axios from 'axios';

export default {
  data() {
    return {
      totalImage: 0,
      loadedImage: 0,
      totalXml: 0,
      loadedXml: 0,
      folderFiles: [],
      folderScanTimer: null,
      folderScanCurrentPosition: 0,
      folderScanFrequency: 40,
    };
  },

  mounted() {
  },

  beforeDestroy() {
    clearInterval(this.folderScanTimer);
  },

  computed: {
    isLoading: function isLoading() {
      // return (this.loadedImage !== this.totalImage) || (this.loadedXml !== this.totalXml);
      return (this.folderFiles.length !== this.folderScanCurrentPosition);
    },
    loadingPercent: function loadingPercent() {
      // const percent = ((this.loadedImage / (this.totalImage < 1 ? 1 : this.totalImage)) * 100);
      const total = (this.folderFiles.length < 1 ? 1 : this.folderFiles.length);
      const percent = ((this.folderScanCurrentPosition / total) * 100);
      return `${Math.round(percent)}%`;
    },
  },

  methods: {
    /**
     * @param {Event} event
     */
    selectFolder: function selectFolder(event) {
      if (event instanceof Event) {
        this.$el.querySelector('input').click();
      }
    },

    reset: function reset() {
      this.totalImage = 0;
      this.loadedImage = 0;
      this.totalJson = 0;
      this.loadedJson = 0;
      this.folderFiles = [];
      this.folderScanTimer = null;
      this.folderScanCurrentPosition = 0;
      clearInterval(this.folderScanTimer);

      this.$store.commit('ImageLabelerSingleTag/clearImages');
      this.$store.commit('ImageLabelerSingleTag/clearJsonData');
    },

    /**
     * @param {array} args
     */
    loadFolder: function loadFolder(...args) {
      if (typeof args !== 'object' || args.length < 1) {
        return;
      }

      this.reset();

      /**
       * @type {Event}
       */
      const element = args[0];

      if (element instanceof Event) {
        /**
         * @type {FileList}
         */
        const fileList = element.target.files;

        if (fileList.length < 1) {
          return;
        }

        this.folderFiles = fileList;
        this.folderScanTimer = setInterval(this.scanFolder.bind(this), 20);
      }
    },

    scanFolder: function scanFolder() {
      const fileList = this.folderFiles;
      const currentPosition = this.folderScanCurrentPosition;
      const nextPosition = this.folderScanCurrentPosition + this.folderScanFrequency;
      const imageFiles = {};
      const imageJson = {};

      if (currentPosition >= fileList.length) {
        clearInterval(this.folderScanTimer);
      }

      for (let index = currentPosition;
        (index < nextPosition) && (index < fileList.length); index += 1) {
        /**
         * @type {File}
         */
        const fileElement = fileList[index];
        this.folderScanCurrentPosition += 1;

        if (fileElement.type.indexOf('image/jpeg') === 0
          || fileElement.type.indexOf('image/png') === 0) {
          this.$set(imageFiles, fileElement.webkitRelativePath, {
            path: fileElement.webkitRelativePath,
            name: fileElement.name,
            imageReader: {
              result: null,
              width: 0,
              height: 0,
            },
            labels: [],
            htmlFileObject: fileElement,
            selected: false,
          });

          this.$set(imageJson, fileElement.webkitRelativePath, {
            flags: {},
            shapes: [],
            imagePath: `.\\${fileElement.webkitRelativePath}`,
            imageData: null,
            imageWidth: null,
            imageHeight: null,
          });

          this.totalImage += 1;
        } else if (fileElement.type.indexOf('application/json') === 0) {
          this.totalJson += 1;

          const fileReader = new FileReader();
          fileReader.onload = (event) => {
            try {
              const result = JSON.parse(event.target.result);
              this.$store.commit('ImageLabelerSingleTag/setJsonData', {
                path: fileElement.webkitRelativePath,
                name: fileElement.name,
                result,
              });
            } catch (error) {
              // eslint-disable-next-line no-console
              console.error(error);
            }

            this.loadedJson += 1;

            if (this.loadedJson === this.totalJson) {
              this.importJSON();
            }
          };

          fileReader.readAsText(fileElement);
        }
      }
      if (Object.keys(imageFiles).length > 0) {
        this.$store.commit('ImageLabelerSingleTag/setImages', imageFiles);
        this.$store.commit('ImageLabelerSingleTag/setJsonDatas', imageJson);
      }
    },

    importJSON: function importJSON() {
      const keys = Object.keys(this.$store.state.ImageLabelerSingleTag.jsonData);
      const imageKeys = Object.keys(this.$store.state.ImageLabelerSingleTag.images);

      for (let index = 0; index < keys.length; index += 1) {
        let result = [];
        const element = this.$store.state.ImageLabelerSingleTag.jsonData[keys[index]];

        /**
         * @type {string}
         */
        // eslint-disable-next-line no-underscore-dangle
        const { imagePath } = element;

        if (imagePath !== undefined) {
          const imageKeyIndex = imageKeys.indexOf(imagePath.replace('./', ''));

          if (imageKeyIndex > -1) {
            const imageElement = {
              ...this.$store.state.ImageLabelerSingleTag.images[imageKeys[imageKeyIndex]],
            };

            const flagsKeys = Object.keys(element.flags);

            for (let flagIndex = 0; flagIndex < flagsKeys.length; flagIndex += 1) {
              const flag = flagsKeys[flagIndex];
              const flagValue = element.flags[flagsKeys[flagIndex]];

              if (flagValue) {
                result = [flag];
              }
            }

            imageElement.labels = result;

            this.$store.commit('setImage', {
              ...imageElement,
            });
          }
        }
      }
    },

    readFileAsync: function readFileAsync(file) {
      return new Promise((resolve, reject) => {
        const fileReader = new FileReader();

        fileReader.onload = () => {
          resolve(fileReader.result);
        };

        fileReader.onerror = reject;

        fileReader.readAsDataURL(file);
      });
    },

    getImageSizeAsync: function getImageSizeAsync(dataUrl) {
      return new Promise((resolve, reject) => {
        const img = new Image();

        img.onload = () => {
          resolve({
            width: img.width,
            height: img.height,
          });
        };

        img.onerror = reject;

        img.src = dataUrl;
      });
    },

    exportJSON: async function exportJSON(item) {
      const element = item;
      const flags = {};
      let imageWidth = 0;
      let imageHeight = 0;
      const num = {};

      if (Object.prototype.hasOwnProperty.call(
        this.$store.state.ImageLabelerSingleTag.jsonData,
        element.path,
      )) {
        const jsonData = this.$store.state.ImageLabelerSingleTag.jsonData[element.path];
        const editorLabels = this.$store.state.ImageLabelerSingleTag.labels;

        // flags form existed.
        for (let index = 0; index < jsonData.flags.length; index += 1) {
          const flag = jsonData.flags[index];
          flags[flag] = false;
        }

        // flags form editor list.
        for (let index = 0; index < editorLabels.length; index += 1) {
          const label = editorLabels[index];
          flags[label] = false;
          num[label.name] = label.num;
        }

        // set select flags
        for (let index = 0; index < element.labels.length; index += 1) {
          const label = element.labels[index];
          flags[label] = true;
        }
      }

      if (element.imageReader.result === null) {
        const imageDataUrl = await this.readFileAsync(element.htmlFileObject);
        const imgageSize = await this.getImageSizeAsync(imageDataUrl);
        imageWidth = imgageSize.width;
        imageHeight = imgageSize.height;
      } else {
        imageWidth = element.imageReader.width;
        imageHeight = element.imageReader.height;
      }

      return Promise.resolve({
        element,
        data: {
          flags,
          num,
          shapes: [],
          imagePath: `.\\${element.path}`,
          imageData: null,
          imageWidth,
          imageHeight,
        },
      });
    },
    upZip: function upZip() {
      this.$swal.showLoading();
      this.$swal({
        title: '请求发送中',
        text: '請稍候...',
        icon: 'info',
        allowOutsideClick: false,
        allowEscapeKey: false,
      });
      axios.get('http://127.0.0.1:30082/upzip').then((res) => {
        console.log(res);
        if (res.data && res.data.status * 1 === 200) {
          this.$swal({
            title: '请求发送成功',
            icon: 'success',
          });
        } else {
          this.$swal({
            title: '輸出錯誤',
            text: 'export error: 解压出错/文件不存在',
            icon: 'error',
          });
        }
      });
    },
    exportJsonFiles: function exportJsonFiles() {
      // this.isLoading = true;
      this.$swal({
        title: '資料準備中',
        text: '請稍候...',
        icon: 'info',
        allowOutsideClick: false,
        allowEscapeKey: false,
      });
      this.$swal.showLoading();

      const keys = this.$store.getters['ImageLabelerSingleTag/getImageKeys'];
      const zip = new JSZip();
      const queue = [];
      const data = [];
      for (let index = 0; index < keys.length; index += 1) {
        const element = this.$store.state.ImageLabelerSingleTag.images[keys[index]];

        if (this.$store.state.ImageLabelerSingleTag.labels.length > 0) {
          queue.push(this.exportJSON(element));
        }
      }

      // TODO: download delay for demo
      queue.push(new Promise((resolve) => {
        setTimeout(() => {
          resolve();
        }, 1000);
      }));

      Promise.all(queue).then((results) => {
        for (let index = 0; index < results.length; index += 1) {
          const result = results[index];
          if (result) {
            data.push({
              filename: `${result.element.name.split('.')[0]}.json`,
              content: JSON.stringify(result.data),
            });
          }
        }

        if (data.length > 0) {
          for (let index = 0; index < data.length; index += 1) {
            const element = data[index];
            zip.file(element.filename, element.content);
          }
          zip.generateAsync({ type: 'blob' }).then((content) => {
            // see FileSaver.js
            // this.isLoading = false;
            saveAs(content, 'labels-json.zip');
            this.$swal.hideLoading();
            this.$swal({
              title: '輸出成功',
              icon: 'success',
            });
            axios.get('http://127.0.0.1:30082/upzip').then((res) => {
              console.log('结果：', res);
            });
          });
        } else {
          this.$swal.hideLoading();
          this.$swal({
            title: '無資料可輸出',
            icon: 'info',
          });
        }
      }).catch((reason) => {
        this.$swal.hideLoading();
        this.$swal({
          title: '輸出錯誤',
          text: `export error: ${reason}`,
          icon: 'error',
        });
      });
    },
  },
};
</script>
