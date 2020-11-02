# III-Image-Label

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run dev
```

### Compiles and minifies for production
```
npm run build
```

### Start HTTP Server
```
npm run serve
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Required Skills

* Javascript (ES6)
* Vue (Javascript Front-end Framework)
* HTML 5
* CSS 3


## Project Dependencies

* Node.js
* npm
	* Webpack
	* Vue
		* Vuex
		* Vue Router
		* Vue-cli
	* Bootstrap
	* lodash
	* Admin-lte
	* file-saver
	* ... see other on package.json


## Project Architecture
```
┌─────────────────┐  
│ III-Image-Label │ -> Browser Appclication
├─────────────────┤
│     Express     │ -> Http server
├─────────────────┤
│     Node.js     │ -> Runtime Engine
├─────────────────┤
│     Host OS     │
└─────────────────┘
```
```
┌──────┬───────────┬─────────┬────────┐
│ Vuex │ VueRouter │         │        │
├──────┴───────────┤         │        │
│       Vue        │  HTML5  │  CSS3  │ -> Front-end
├──────────────────┤         │        │
│    Javascript    │         │        │
├──────────────────┴─────────┴────────┤
│               Webpack               │ -> Bundler
├─────────────────────────────────────┤
│                         ┌───────────┤ 
│               Node.js   │    NPM    │ -> Bundler Runtime Engine
├─────────────────────────┴───────────┤
│           III-Image-Label           │
└─────────────────────────────────────┘
```

## Flow
```
Start (main.js) -> Boot-up Vue (Load vuex & vue-router and etc.) 
-> Route detect -> Render Page -> Vue Lifecycle
```

## Floder Structure
```
./src
├── App.vue -> Entry point. (Vue Component)
├── assets -> Static files. (like images)
│   ├── logo-mini.png
│   ├── logo.png
│   └── vueLogo.png
├── components -> Vue Components.
│   ├── BottomMenu.vue -> Page Footer.
│   ├── ImageLabeler
│   │   ├── AddLabelModel.vue -> Dialog for add label function.
│   │   ├── FileLoader.vue -> Component for load image & import/export xml file.
│   │   ├── ImageList.vue -> Component for listing images.
│   │   ├── ImageViewer.vue -> Component for render image (use for list).
│   │   └── LabelLoader.vue -> Component for import labels (json file).
│   ├── ImageLabelerSingleTag
│   │   ├── AddLabelModel.vue -> Dialog for add label function.
│   │   ├── FileLoader.vue -> Component for load image & import/export json file.
│   │   ├── ImageList.vue -> Component for listing images.
│   │   ├── ImageViewer.vue -> Component for render image (use for list).
│   │   ├── LabelLoader.vue -> Component for import labels (json file).
│   │   ├── RemoveLabelModel.vue -> Dialog for remove labels function.
│   │   └── SelectLabelModel.vue -> Dialog for set labels function.
│   ├── LeftMenu.vue -> Page left menu.
│   └── TopMenu.vue -> Page top menu.
├── main.js -> Entry point.
├── main.scss -> CSS Entry point.
├── router -> Vue Router files.
│   └── index.js -> Router rules.
├── store -> Vuex files.
│   ├── index.js -> Main store.
│   └── modules
│       ├── imageLabeler.js -> Store for Image Label Editor.
│       └── imageLabelerSingleTag.js -> Store for Image Label Single Tag Editor.
└── views -> Vue Pages
    ├── Home.vue -> Welcome page
    ├── ImageLabelEditor.vue -> Image Label Editor - Editor page.
    ├── ImageLabeler.vue -> Image Label Editor - Image list page.
    └── imageLabelerSingleTag.vue -> Image Label Editor Single Tag - Image list & Editor page.
```

## View Structure
```
┌─────┬──────────────────────────┐
│     │            1             │
│     ├──────────────────────────┤
│     │                          │
│     │                          │
│  2  │            4             │
│     │                          │
│     │                          │
│     ├──────────────────────────┤
│     │            3             │
└─────┴──────────────────────────┘
App.vue
├── TopMenu.vue *1
├── LeftMenu.vue *2
├── BottomMenu.vue *3
└── <router-view> *4
    ├── Home.vue
    ├── ImageLabeler.vue
    ├── ImageLabelEditor.vue
    └── imageLabelerSingleTag.vue
```
