<template>
  <div>
    <input style="display: none" type="file" @change="loadFile"/>
    <button class="btn btn-info btn-block mb-3"
      @click="selectFile">
        <i class="fas fa-folder-open"></i> 匯入標籤
    </button>
    <button class="btn btn-info btn-block mb-3"
      @click="exportJSON">
        <i class="fas fa-download"></i> 匯出標籤
    </button>
  </div>
</template>

<script>
import { saveAs } from 'file-saver';

export default {
  data() {
    return {
      worker: null,
    };
  },

  mounted() {
    this.worker = this.$worker.create([
      {
        message: 'loadLabel',
        func: (fileElement) => {
          // eslint-disable-next-line no-restricted-globals
          // const workerScope = self;

          // eslint-disable-next-line no-undef
          const fileReader = new FileReaderSync();
          const result = fileReader.readAsText(fileElement);
          try {
            const jsonResult = JSON.parse(result);
            return jsonResult;
          } catch (error) {
            // eslint-disable-next-line no-console
            console.error(error);
            return [];
          }
        },
      },
    ]);
  },

  computed: {
  },

  methods: {
    /**
     * @param {Event} event
     */
    selectFile: function selectFile(event) {
      if (event instanceof Event) {
        this.$el.querySelector('input').click();
      }
    },

    /**
     * @param {array} args
     */
    loadFile: function loadFile(...args) {
      if (typeof args !== 'object' || args.length < 1) {
        return;
      }

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

        for (let index = 0; index < fileList.length; index += 1) {
          /**
           * @type {File}
           */
          const fileElement = fileList[index];

          if (fileElement.type.indexOf('application/json') === 0) {
            this.worker.postMessage('loadLabel', [fileElement])
              .then((response) => {
                for (let responseIndex = 0; responseIndex < response.length; responseIndex += 1) {
                  const label = response[responseIndex];

                  this.$store.commit('addLabel', label);
                }
              })
              // eslint-disable-next-line no-console
              .catch(console.error);
          }
        }
      }
    },

    exportJSON: function exportJSON() {
      const labels = JSON.stringify(this.$store.state.ImageLabeler.labels);
      const blob = new Blob([labels], { type: 'application/json;charset=utf-8' });
      saveAs(blob, 'labels.json');
    },
  },
};
</script>
