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
      @click="exportLabelsXML"
      :disabled="isLoading">
        <span class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true"
          v-show="isLoading" />
        <i class="fas fa-download" v-show="!isLoading"></i> 匯出XML記錄
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
import xmlConvert from 'xml-js';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

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
      this.totalXml = 0;
      this.loadedXml = 0;
      this.folderFiles = [];
      this.folderScanTimer = null;
      this.folderScanCurrentPosition = 0;
      clearInterval(this.folderScanTimer);

      this.$store.commit('clearImages');
      this.$store.commit('clearXmlData');
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
          });

          this.totalImage += 1;
        } else if (fileElement.type.indexOf('text/xml') === 0) {
          this.totalXml += 1;

          const fileReader = new FileReader();
          fileReader.onload = (event) => {
            try {
              const xmlString = xmlConvert.xml2json(event.target.result, { compact: true });
              const result = JSON.parse(xmlString);
              this.$store.commit('setXmlData', {
                path: fileElement.webkitRelativePath,
                name: fileElement.name,
                result,
              });
            } catch (error) {
              // eslint-disable-next-line no-console
              console.error(error);
            }

            this.loadedXml += 1;

            if (this.loadedXml === this.totalXml) {
              this.importXML();
            }
          };

          fileReader.readAsText(fileElement);
        }
      }
      if (Object.keys(imageFiles).length > 0) {
        this.$store.commit('setImages', imageFiles);
      }
    },

    importXML: function importXML() {
      const keys = Object.keys(this.$store.state.ImageLabeler.xmlData);
      const imageKeys = Object.keys(this.$store.state.ImageLabeler.images);

      for (let index = 0; index < keys.length; index += 1) {
        const result = [];
        const element = this.$store.state.ImageLabeler.xmlData[keys[index]];

        /**
         * @type {string}
         */
        // eslint-disable-next-line no-underscore-dangle
        const imagePath = element.result.annotation.path._text;
        const imageKeyIndex = imageKeys.indexOf(imagePath.replace('./', ''));

        if (imageKeyIndex > -1) {
          const imageElement = {
            ...this.$store.state.ImageLabeler.images[imageKeys[imageKeyIndex]],
          };

          let data = [];

          if (Array.isArray(element.result.annotation.object)) {
            data = [...element.result.annotation.object];
          } else {
            data.push({ ...element.result.annotation.object });
          }

          for (let dataIndex = 0; dataIndex < data.length; dataIndex += 1) {
            const item = data[dataIndex];
            result.push(this.convertXMLLabelToObject(item));
          }

          imageElement.labels = result;

          this.$store.commit('setImage', {
            ...imageElement,
          });
          this.$store.commit('setImageContentSize', {
            path: imageElement.path,
            // eslint-disable-next-line no-underscore-dangle
            width: element.result.annotation.size.width._text,
            // eslint-disable-next-line no-underscore-dangle
            height: element.result.annotation.size.height._text,
          });
        }
      }
    },

    convertXMLLabelToObject: function convertXMLLabelToObject(item) {
      // eslint-disable-next-line no-underscore-dangle
      const xmin = parseInt(item.bndbox.xmin._text, 10);
      // eslint-disable-next-line no-underscore-dangle
      const xmax = parseInt(item.bndbox.xmax._text, 10);
      // eslint-disable-next-line no-underscore-dangle
      const ymin = parseInt(item.bndbox.ymin._text, 10);
      // eslint-disable-next-line no-underscore-dangle
      const ymax = parseInt(item.bndbox.ymax._text, 10);
      const data = {
        // eslint-disable-next-line no-underscore-dangle
        name: item.name._text,
        color: null,
        lx: Number.isNaN(xmin) ? 0 : xmin,
        ty: Number.isNaN(ymin) ? 0 : ymin,
        rx: Number.isNaN(xmax) ? 0 : xmax,
        by: Number.isNaN(ymax) ? 0 : ymax,
      };

      return data;
    },

    exportXML: function exportXML(item) {
      const element = item;
      const options = { compact: true, ignoreComment: true, spaces: 4 };
      const objects = [];
      for (let index = 0; index < element.labels.length; index += 1) {
        const labelElement = element.labels[index];
        objects.push({
          name: labelElement.name,
          pose: 'Unspecified',
          truncated: 0,
          difficult: 0,
          bndbox: {
            xmin: labelElement.lx,
            ymin: labelElement.ty,
            xmax: labelElement.rx,
            ymax: labelElement.by,
          },
        });
      }
      const result = xmlConvert.json2xml({
        annotation: {
          filename: element.name,
          path: `./${element.path}`,
          source: {
            database: 'UnKnown',
          },
          size: {
            width: element.imageReader.width,
            height: element.imageReader.height,
            depth: 1,
          },
          segmented: 0,
          object: objects,
        },
      }, options);

      return result;
    },

    exportLabelsXML: function exportLabelsXML() {
      // this.isLoading = true;
      const keys = Object.keys(this.$store.state.ImageLabeler.images);
      const zip = new JSZip();
      const data = [];
      for (let index = 0; index < keys.length; index += 1) {
        const element = this.$store.state.ImageLabeler.images[keys[index]];
        if (element.labels.length > 0) {
          data.push({
            filename: `${element.name.split('.')[0]}.xml`,
            content: this.exportXML(element),
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
          saveAs(content, 'labels-xml.zip');
        });
      }
    },
  },
};
</script>
