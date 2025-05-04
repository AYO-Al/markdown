官方文档可在[vue](https://cn.vuejs.org/)查看。

vue是开源项目，学习源码可以访问[vue项目地址](https://github.com/vuejs/core)。
# 创建vue3工程

- 目前 `vue-cli` 已处于维护模式，官方推荐基于 [Vite](https://cn.vitejs.dev/) 创建项目。
- `vite`是新一代前端构建工具，`vite`优势如下：
    - 轻量快速的热重载(HMR)，能实现极速的服务启动。
    - 对 `TypeScript`、`JSX`、`CSS`等支持开箱即用。
    - 真正的按需编译，不再等待整个应用编译完成。
    - `webpack` 构建与 `vite` 构建对比如下：

![](image/vue_time_1.png)

![](image/vue_time_2.png)

- 创建vue项目步骤，可查看[官方文档](https://cn.vuejs.org/guide/quick-start.html)

```javascript
// 这一指令将会安装并执行 [create-vue](https://github.com/vuejs/create-vue)，它是 Vue 官方的项目脚手架工具。
$ npm create vue@latest

✔ Project name: … <your-project-name>
✔ Add TypeScript? … No / Yes
✔ Add JSX Support? … No / Yes
✔ Add Vue Router for Single Page Application development? … No / Yes
✔ Add Pinia for state management? … No / Yes
✔ Add Vitest for Unit testing? … No / Yes
✔ Add an End-to-End Testing Solution? … No / Cypress / Nightwatch / Playwright
✔ Add ESLint for code quality? … No / Yes
✔ Add Prettier for code formatting? … No / Yes
✔ Add Vue DevTools 7 extension for debugging? (experimental) … No / Yes

Scaffolding project in ./<your-project-name>...
Done.

// 如果不确定是否要开启某个功能，你可以直接按下回车键选择 `No`。在项目被创建后，通过以下步骤安装依赖并启动开发服务器：
$ cd <your-project-name>
$ npm install
$ npm run dev

```

- 推荐的 IDE 配置是 [Visual Studio Code](https://code.visualstudio.com/) + [Vue - Official 扩展](https://marketplace.visualstudio.com/items?itemName=Vue.volar)。如果使用其他编辑器，参考 [IDE 支持章节](https://cn.vuejs.org/guide/scaling-up/tooling.html#ide-support)。
- 更多工具细节，包括与后端框架的整合，我们会在[工具链指南](https://cn.vuejs.org/guide/scaling-up/tooling.html)进行讨论。
- 要了解构建工具 Vite 更多背后的细节，请查看 [Vite 文档](https://cn.vitejs.dev/)。
- 如果你选择使用 TypeScript，请阅读 [TypeScript 使用指南](https://cn.vuejs.org/guide/typescript/overview.html)。

- 当你准备将应用发布到生产环境时，请运行：

```javascript
npm run build
```

此命令会在 `./dist` 文件夹中为你的应用创建一个生产环境的构建版本。关于将应用上线生产环境的更多内容，请阅读[生产环境部署指南](https://cn.vuejs.org/guide/best-practices/production-deployment.html)。
## 项目结构

```bash
my-vue-project/
├── node_modules/     # 项目依赖的第三方库（npm install 后自动生成）
├── public/           # 静态资源目录（不会被构建工具处理）
├── src/              # 源代码目录（核心开发区域）
├── .gitignore        # Git 忽略文件配置
├── index.html        # 应用入口 HTML 文件
├── package.json      # 项目配置和依赖管理
├── vite.config.js    # Vite 配置文件（构建、插件、代理等）
├── tsconfig.json     # TypeScript 配置（如果选择 TypeScript）
└── README.md         # 项目说明文档
```

- `vite`项目中，`index.html`是项目的入口文件，在项目的最外层。
- 加载 `index.html` 后，`vite` 解析 `<script type="module" src="/src/main.js"></script>` 指向的 `javascript`。
- `vue3` 中通过 `createApp` 函数创建一个应用实例。​

> (1) public/ 目录​​

- ​**​作用​**​：存放无需经过构建工具处理的静态资源（如 `favicon.ico`、`robots.txt` 等）。
- ​**​特点​**​：
    - 文件会直接复制到构建输出目录（如 `dist/`）。
    - 通过 `/文件名` 直接访问（例如 `<img src="/logo.png">`）。

> ​(2) src/ 目录​​

```
src/
├── assets/           # 静态资源（图片、字体、CSS 等，会被构建工具处理）
├── components/       # 可复用的 Vue 组件（如 Button.vue、Header.vue）
├── App.vue           # 根组件（应用入口组件）
├── main.js           # 应用入口文件（初始化 Vue 实例）
└── ...
```

- ​**​`assets/`​**​  
    存放需要经过构建工具处理的静态资源（如 SCSS 文件、图片等）。构建时会优化这些资源（如压缩图片、编译 SCSS 到 CSS）。
    
- ​**​`components/`​**​  
    存放可复用的 Vue 组件。建议按功能或模块划分子目录（如 `components/Button`、`components/Modal`）。
    
- ​**​`App.vue`​**​  
    应用的根组件，所有页面和组件会在此组件内渲染。
    
- ​**​`main.js`​**​  
    应用入口文件，初始化 Vue 实例并挂载到 DOM：

```javascript
// vue中导出分为默认导出和命名导出，命名导出在别的文件导入必须用{}包裹
export default function() { console.log('默认导出') }
export const PI = 3.14
export const sum = (a, b) => a + b

import { createApp } from 'vue'      // 从 Vue 库导入应用创建函数
import App from './App.vue'          // 导入根组件

createApp(App).mount('#app')         // 创建应用实例并挂载到 DOM
```
    

> ​(3) 其他常见目录（按需添加）​​

- ​**​`router/`​**​  
    存放 Vue Router 配置（需手动安装 `vue-router`）：
    
    ```javascript
    // router/index.js
    import { createRouter, createWebHistory } from 'vue-router'
    import Home from '../views/Home.vue'
    
    const routes = [
      { path: '/', component: Home }
    ]
    
    export default createRouter({
      history: createWebHistory(),
      routes
    })
    ```
    
- ​**​`stores/`​**​  
    存放 Pinia 状态管理配置（需手动安装 `pinia`）：
    
    ```javascript
    // stores/counter.js
    import { defineStore } from 'pinia'
    
    export const useCounterStore = defineStore('counter', {
      state: () => ({ count: 0 }),
      actions: {
        increment() { this.count++ }
      }
    })
    ```
    
- ​**​`views/` 或 `pages/`​**​  
    存放页面级组件（如 `Home.vue`、`About.vue`），与路由对应。

- `index.html`

```javascript
// main.js中绑定的DOM
<div id="app"></div> 

// 导入main.js
<script type="module" src="/src/main.js"></script> 
```

> ​配置文件详解​​

> ​**​(1) `vite.config.js`​**​

- ​**​作用​**​：配置 Vite 构建行为（如插件、代理、别名等）。
- ​**​示例​**​：
    
    ```javascript
    import { defineConfig } from 'vite'
    import vue from '@vitejs/plugin-vue'
    
    export default defineConfig({
      plugins: [vue()],
      resolve: {
        alias: {
          '@': '/src'  // 路径别名（在代码中通过 import '@/components/Button.vue' 引用）
        }
      },
      server: {
        proxy: {
          '/api': 'http://localhost:3000'  // 开发服务器代理配置
        }
      }
    })
    ```
    

> ​**​(2) `package.json`​**​

- ​**​作用​**​：定义项目依赖、脚本命令和元信息。
- ​**​关键字段​**​：
    
    ```json
    {
      "scripts": {
        "dev": "vite",          // 启动开发服务器
        "build": "vite build",  // 构建生产环境代码
        "preview": "vite preview" // 预览构建后的应用
      },
      "dependencies": {
        "vue": "^3.4.0"         // 项目依赖
      },
      "devDependencies": {
        "vite": "^5.0.0",       // 开发依赖
        "@vitejs/plugin-vue": "^4.5.0"
      }
    }
    ```

> 环境变量文件​​

- ​**​`.env`​**​  : 存放环境变量（需以 `VITE_` 前缀开头才能在代码中访问）：
    
    ```
    VITE_API_URL=https://api.example.com
    ```
    
- ​**​代码中访问​**​：
    
    ```javascript
    const apiUrl = import.meta.env.VITE_API_URL
    ```
## 简单示例

> App.vue

```javascript
// vue文件里写三种标签

<template>
    <!-- html结构 -->
     <div class="app">
        <h1>你好啊！</h1>
        
     </div>
     <!-- 使用组件 -->
     <person/> 
</template>

<script lang="ts">
    // js代码或ts
    import person from "./components/Person.vue";
    export default {
        name: 'App',
        components:{person} // 注册组件
        
    }
</script>

<style>
    /* 样式 */
    .app {
        background-color: aqua;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
</style>

```

1. `export default`作用

| 类型           | 语法                   | 特点            |
| ------------ | -------------------- | ------------- |
| ​**​默认导出​**​ | `export default ...` | 一个模块只能有一个默认导出 |
| ​**​命名导出​**​ | `export const ...`   | 可导出多个，按名称引用   |

2. `lang="ts"` 的作用​​

- ​**​启用 TypeScript​**​：告诉 Vue 编译器此 `<script>` 块内的代码使用 TypeScript 语法
- ​**​类型检查​**​：会触发 TypeScript 的类型系统验证（需要项目中已配置 `tsconfig.json`）
- ​**​VS Code 支持​**​：结合 Volar 插件可获得完善的 TS 代码提示

 3. `name: 'App'` 的作用​​

- ​**​组件标识​**​：定义当前组件在 DevTools 中显示的名称
- ​**​递归组件​**​：当组件内部调用自身时需要依赖 `name` 属性
- ​**​`<keep-alive>` 缓存​**​：在 `include/exclude` 配置中通过 `name` 指定要缓存的组件

> components/Person.vue

```javascript
// 以下方式是用vue2语法定义

<template>
    <!-- html结构 -->
     <div class="person">
        <h2>姓名：{{ name }}</h2>
        <h2>年龄：{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeage">修改年龄</button>
        <button @click="showTel">显示联系方式</button>
     </div>
</template>

<script lang="ts">
    // js代码或ts
    export default {
        // 选项式API
        name: 'person',
        // 变量定义
        data(){
            return {
                name : "kelly",
                age: 18,
                tel: '12312312313'
            }
        },
        // 方法定义
        methods: {
            changeName(){
                this.name = "zhang-san"
            },
            changeage(){
                this.age += 1
            },
            showTel(){
                alert(this.tel)
            }
        }
    }
</script>

<style>
    /* 样式 */
    .person {
        background-color: aqua;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
</style>
```
# vue3核心语法
## OptionsAPI与CompositionAPI

- `vue2` 的 `API` 设计是 `Options`(配置)风格的。
- `vue3` 的 `API` 设计是 `Composition`(组合)风格的。

## Options API 的弊端

`Options`类型的 `API`，数据、方法、计算属性等，是分散在：`data`、`methods`、`computed`中的，若想新增或者修改一个需求，就需要分别修改：`data`、`methods`、`computed`，不便于维护和复用。

<img src="image/tmp1746255652446_vue_time_3.gif" alt="2.gif" style="zoom:70%;border-radius:20px" /><img src="image/tmp1746255792234_vue_time_3.gif" alt="1.gif" style="zoom:70%;border-radius:20px" />


## Composition API 的优势

可以用函数的方式，更加优雅的组织代码，让相关功能的代码更加有序的组织在一起。

<img src="image/tmp1746255888105_vue_time_3.gif" alt="4.gif" style="height:300px;border-radius:10px" /><img src="image/vue_time_3.gif" alt="3.gif" style="height:300px;border-radius:10px" />

> 说明：以上四张动图原创作者：大帅老猿
## setup

`setup`是`Vue3`中一个新的配置项，值是一个函数，它是 `Composition API` **“表演的舞台**_**”**_，组件中所用到的：数据、方法、计算属性、监视......等等，均配置在`setup`中。

特点如下：

- `setup`函数返回的对象中的内容，可直接在模板中使用。
- `setup`中访问`this`是`undefined`。
- `setup`函数会在`beforeCreate`之前调用，它是“领先”所有钩子执行的。

```vue
<template>
    <!-- html结构 -->
     <div class="person">
        <h2>姓名：{{ name }}</h2>
        <h2>年龄：{{ age }}</h2>
        <h2>{{ b }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeage">修改年龄</button>
        <button @click="showTel">显示联系方式</button>
     </div>
</template>

<script lang="ts">
    // js代码或ts
    export default {
        name: 'person', // 如果不指定默认为文件名
        // setup(){
            // 数据
            // let tel = '123123123131' // 此时的tel不是响应式的，函数修改对应变量后外部引用不会改变

            // 方法
        
            // function showTel(){
            //     alert(tel)
            // }

            // 暴露数据和函数，模板中才能使用
            // return {a:name,age,changeName,changeage,showTel}
            // 也可以直接返回渲染函数指定渲染的内容
            // 简写（箭头函数） ()=> '哈哈'
            // return function(){
            //     return '哈哈'
            // }
        // }

    }
</script>

<!-- setup语法糖：默认该标签内的都是setup -->
<!-- 该文件内的所有script必须是同一种语言 -->
 <!-- 同一个文件的setup必须唯一 -->
<!-- <script lang="ts" setup name="Person123"> -->
 <script lang="ts" setup>
    let b = 666
    let name = '张三'  //
            let age = 18
            let tel = '123123123131' // 此时的tel不是响应式的，函数修改对应变量后外部引用不会改变

            // 方法
            function changeName() {
                name = 'zhang-san'
            }

            function changeage(){
                age += 1
            }

            function showTel(){
                alert(tel)
            }
</script>

<style>
    /* 样式 */
    .person {
        background-color: aqua;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
</style>
```

- 如果想直接在 `setup` 语法糖中指定组件名：

```node
// 下载对应插件
npm i vite-plugin-vue-setup-extend -D

// vite.config.js文件中配置插件
import VueSetup from 'vite-plugin-vue-setup-extend'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    VueSetup
  ],
```

### setup 与 Options API 的关系

- `Vue2` 的配置（`data`、`methos`......）中**可以访问到** `setup`中的属性、方法。
- 但在`setup`中**不能访问到**`Vue2`的配置（`data`、`methos`......）。
- 如果与`Vue2`冲突，则`setup`优先。
## ref创建响应式数据

- **作用：**定义响应式变量。
- **语法：**`let xxx = ref(初始值)`。
- **返回值：**一个`RefImpl`的实例对象，简称`ref对象`或`ref`，`ref`对象的`value`**属性是响应式的**。

- **注意点：**

    - `JS`中操作数据需要：`xxx.value`，但模板中不需要`.value`，直接使用即可。
    - 对于`let name = ref('张三')`来说，`name`不是响应式的，`name.value`是响应式的。

```vue
<template>
  <div class="person">
    <h2>姓名：{{name}}</h2>
    <h2>年龄：{{age}}</h2>
    <button @click="changeName">修改名字</button>
    <button @click="changeAge">年龄+1</button>
    <button @click="showTel">点我查看联系方式</button>
  </div>
</template>

<script setup lang="ts" name="Person">
  import {ref} from 'vue'
  // name和age是一个RefImpl的实例对象，简称ref对象，它们的value属性是响应式的。
  let name = ref('张三')
  let age = ref(18)
  // tel就是一个普通的字符串，不是响应式的
  let tel = '13888888888'

  function changeName(){
    // JS中操作ref对象时候需要.value
    name.value = '李四'
    console.log(name.value)

    // 注意：name不是响应式的，name.value是响应式的，所以如下代码并不会引起页面的更新。
    // name = ref('zhang-san')
  }
  function changeAge(){
    // JS中操作ref对象时候需要.value
    age.value += 1 
    console.log(age.value)
  }
  function showTel(){
    alert(tel)
  }
</script>

```
## reactive 创建：对象类型的响应式数据

- **作用：**定义一个**响应式对象**（基本类型不要用它，要用`ref`，否则报错）
- **语法：**`let 响应式对象= reactive(源对象)`。
- **返回值：**一个`Proxy`的实例对象，简称：响应式对象。
- **注意点：**`reactive`定义的响应式数据是“深层次”的。

```vue
<template>
  <div class="person">
    <h2>汽车信息：一台{{ car.brand }}汽车，价值{{ car.price }}万</h2>
    <h2>游戏列表：</h2>
    <ul>
      <!-- v-for="i in games"​:Vue 的 ​​循环渲染指令​​。-->
      <!-- :key="g.id":为每个元素绑定 ​​唯一标识​​，优化虚拟 DOM 的更新效率。-->
      <li v-for="g in games" :key="g.id">{{ g.name }}</li>
    </ul>
    <h2>测试：{{obj.a.b.c.d}}</h2>
    <button @click="changeCarPrice">修改汽车价格</button>
    <button @click="changeFirstGame">修改第一游戏</button>
    <button @click="test">测试</button>
  </div>
</template>

<script lang="ts" setup name="Person">
import { reactive } from 'vue'

// 数据
let car = reactive({ brand: '奔驰', price: 100 })
let games = reactive([
  { id: 'ahsgdyfa01', name: '英雄联盟' },
  { id: 'ahsgdyfa02', name: '王者荣耀' },
  { id: 'ahsgdyfa03', name: '原神' }
])
let obj = reactive({
  a:{
    b:{
      c:{
        d:666
      }
    }
  }
})

function changeCarPrice() {
  car.price += 10
}
function changeFirstGame() {
  games[0].name = '流星蝴蝶剑'
}
function test(){
  obj.a.b.c.d = 999
}
</script>
```
## ref 创建：对象类型的响应式数据

- 其实`ref`接收的数据可以是：**基本类型**、**对象类型**。
- 若`ref`接收的是对象类型，内部其实也是调用了`reactive`函数。

```vue
<template>
  <div class="person">
    <h2>汽车信息：一台{{ car.brand }}汽车，价值{{ car.price }}万</h2>
    <h2>游戏列表：</h2>
    <ul>
      <li v-for="g in games" :key="g.id">{{ g.name }}</li>
    </ul>
    <h2>测试：{{obj.a.b.c.d}}</h2>
    <button @click="changeCarPrice">修改汽车价格</button>
    <button @click="changeFirstGame">修改第一游戏</button>
    <button @click="test">测试</button>
  </div>
</template>

<script lang="ts" setup name="Person">
import { ref } from 'vue'

// 数据
let car = ref({ brand: '奔驰', price: 100 })
let games = ref([
  { id: 'ahsgdyfa01', name: '英雄联盟' },
  { id: 'ahsgdyfa02', name: '王者荣耀' },
  { id: 'ahsgdyfa03', name: '原神' }
])
let obj = ref({
  a:{
    b:{
      c:{
        d:666
      }
    }
  }
})

console.log(car)

function changeCarPrice() {
  car.value.price += 10
}
function changeFirstGame() {
  games.value[0].name = '流星蝴蝶剑'
}
function test(){
  obj.value.a.b.c.d = 999
}
</script>
```

## ref 对比 reactive

宏观角度看：

> 1. `ref`用来定义：**基本类型数据**、**对象类型数据**；
>
> 2. `reactive`用来定义：**对象类型数据**。

- 区别：

> 1. `ref`创建的变量必须使用`.value`（可以使用`Vue - Official`插件自动添加`.value`）。
>
>    <img src="image/vue_time_3.png" alt="自动补充value" style="zoom:50%;border-radius:20px" /> 
>
> 2. `reactive`重新分配一个新对象，会**失去**响应式（可以使用`Object.assign`去整体替换）。


- 使用原则：

> 1. 若需要一个基本类型的响应式数据，必须使用`ref`。
> 2. 若需要一个响应式对象，层级不深，`ref`、`reactive`都可以。
> 3. 若需要一个响应式对象，且层级较深，推荐使用`reactive`。

## toRefs 与 toRef

- 作用：将一个响应式对象中的每一个属性，转换为`ref`对象。
- 备注：`toRefs`与`toRef`功能一致，但`toRefs`可以批量转换。
- 语法如下：

```vue
<template>
  <div class="person">
    <h2>姓名：{{person.name}}</h2>
    <h2>年龄：{{person.age}}</h2>
    <h2>性别：{{person.gender}}</h2>
    <button @click="changeName">修改名字</button>
    <button @click="changeAge">修改年龄</button>
    <button @click="changeGender">修改性别</button>
  </div>
</template>

<script lang="ts" setup name="Person">
  import {ref,reactive,toRefs,toRef} from 'vue'

  // 数据
  let person = reactive({name:'张三', age:18, gender:'男'})
	
  // 通过toRefs将person对象中的n个属性批量取出，且依然保持响应式的能力
  let {name,gender} =  toRefs(person)
	
  // 通过toRef将person对象中的gender属性取出，且依然保持响应式的能力
  let age = toRef(person,'age')

  // 方法
  function changeName(){
    name.value += '~'
  }
  function changeAge(){
    age.value += 1
  }
  function changeGender(){
    gender.value = '女'
  }
</script>
```
## computed
作用：根据已有数据计算出新数据（和`Vue2`中的`computed`作用一致）。

<img src="image/vue_time_3.png" style="zoom:20%;" />  

```vue
<template>
  <div class="person">
   <!--v-model: 双向绑定-->
    姓：<input type="text" v-model="firstName"> <br>
    名：<input type="text" v-model="lastName"> <br>
    全名：<span>{{fullName}}</span> <br>
    <button @click="changeFullName">全名改为：li-si</button>
  </div>
</template>

<script setup lang="ts" name="App">
  import {ref,computed} from 'vue'

  let firstName = ref('zhang')
  let lastName = ref('san')

  // 计算属性——只读取，不修改，返回的也是ref类型
  /* let fullName = computed(()=>{
    return firstName.value + '-' + lastName.value
  }) */


  // 计算属性——既读取又修改
  let fullName = computed({
    // 读取
    get(){
      return firstName.value + '-' + lastName.value
    },
    // 修改
    set(val){
      console.log('有人修改了fullName',val)
      firstName.value = val.split('-')[0]
      lastName.value = val.split('-')[1]
    }
  })

  // 调用set方法并传参
  function changeFullName(){
    fullName.value = 'li-si'
  } 
</script>
```
## watch

- 作用：监视数据的变化（和`Vue2`中的`watch`作用一致）
- 特点：`Vue3`中的`watch`只能监视以下**四种数据**：

> 1. `ref`定义的数据。
> 2. `reactive`定义的数据。
> 3. 函数返回一个值（`getter`函数）。
> 4. 一个包含上述内容的数组。

我们在`Vue3`中使用`watch`的时候，通常会遇到以下几种情况：

> 情况一：监视【ref】定义的【基本类型】数据

- 监视`ref`定义的【基本类型】数据：直接写数据名即可，监视的是其`value`值的改变。

```vue
<template>
    <div class="person">
      <h1>情况一：监视【ref】定义的【基本类型】数据</h1>
      <h1>{{ sum  }}</h1>
      <button @click="changeSum">增加值</button>
    </div>
  </template>
    
  <script setup lang="ts" name="App">
    import {ref, watch} from 'vue'
    let sum = ref(0)

    function changeSum(){
        sum.value += 1
    }

    // watch(谁？,回调函数)：情况1:监视【ref】定义的【基本类型】数据
    // 返回的值即是取消监控函数
    const stopWatch = watch(sum,(newValue,oldValue)=>{
        console.log("sum变化了",newValue,oldValue)
        if(newValue >= 10){
          stopWatch()
        }
    })
     
  </script>
```

> 情况二：监视【ref】定义的【对象类型】数据

- 监视`ref`定义的【对象类型】数据：直接写数据名，监视的是对象的【地址值】，若想监视对象内部的数据，要手动开启深度监视。

```vue
<template>
    <div class="person">
      <h1>情况二：监视【ref】定义的【对象类型】数据</h1>
      <h1>{{ person.name }},{{ person.age }}</h1>
      <button @click="changeName">修改名字</button>
      <button @click="changeAge">修改年龄</button>
      <button @click="changePer">修改人</button>
    </div>
  </template>
    
  <script setup lang="ts" name="App">
    import {ref, watch} from 'vue'
    let person = ref({
      name: 'zhang-san',
      age : 18
    })

    function changeName(){
      person.value.name += '~'
    }

    function changeAge(){
        person.value.age += 1
    }

    function changePer(){
      person.value = {name:"zhang",age:19  }
    }

    /* watch(谁？,回调函数,watch配置对象)：情况2:监视【ref】定义的【对象类型】数据。监视的是对象的地址值，若想监视对象内部属性的变化，需要手动开启深度监视
    
    监视，情况二：监视【ref】定义的【对象类型】数据，监视的是对象的地址值，若想监视对象内部属性的变化，需要手动开启深度监视
    watch的第一个参数是：被监视的数据
    watch的第二个参数是：监视的回调
    watch的第三个参数是：配置对象（deep、immediate等等.....） 
  */
    watch(person,(newValue,oldValue)=>{
      console.log('person变化了',newValue,oldValue)
    },{deep:true,immediate:true})
     
  </script>
```

> 注意：
> 
> * 若修改的是`ref`定义的对象中的属性，`newValue` 和 `oldValue` 都是新值，因为它们是同一个对象。
>
> * 若修改整个`ref`定义的对象，`newValue` 是新值， `oldValue` 是旧值，因为不是同一个对象了。

> 情况三：监视【reactive】定义的【对象类型】数据，且默认开启了深度监视

- 监视`reactive`定义的【对象类型】数据，且默认开启了深度监视。

```vue
<template>
    <div class="person">
      <h1>情况三：监视【reactive】定义的【对象类型】数据，且默认开启了深度监视</h1>
      <h1>{{ person.name }},{{ person.age }}</h1>
      <button @click="changeName">修改名字</button>
      <button @click="changeAge">修改年龄</button>
      <button @click="changePer">修改人</button>
    </div>
  </template>
    
  <script setup lang="ts" name="App">
    import {reactive, watch} from 'vue'
    let person = reactive({
      name: 'zhang-san',
      age : 18
    })

    function changeName(){
      person.name += '~'
    }

    function changeAge(){
        person.age += 1
    }

    function changePer(){
      Object.assign(person,{name:"zhang",age:19  })
    }

    // watch(谁？,回调函数)：情况三：监视【reactive】定义的【对象类型】数据，且默认开启了深度监视
    watch(person,(newValue,oldValue)=>{
      console.log('person变化了',newValue,oldValue)
    })
     
  </script>
```

> 情况四：监视`ref`或`reactive`定义的【对象类型】数据中的**某个属性**

监视`ref`或`reactive`定义的【对象类型】数据中的**某个属性**，注意点如下：

1. 若该属性值**不是**【对象类型】，需要写成函数形式。
2. 若该属性值是**依然**是【对象类型】，可直接编，也可写成函数，建议写成函数。

结论：监视的要是对象里的属性，那么最好写函数式，注意点：若是对象监视的是地址值，需要关注对象内部，需要手动开启深度监视。

```vue
<template>
    <div class="person">
      <h1>情况四：监视ref或reactive定义的【对象类型】数据中的某个属性</h1>
      <h1>姓名：{{ person.name }}</h1>
      <h1>年龄：{{ person.age }}</h1>
      <h1>车：{{ person.car.c1 }} {{ person.car.c2 }}</h1>
      <button @click="changeName">修改名字</button>
      <button @click="changeAge">修改年龄</button>
      <button @click="changeC1">修改第一台车</button>
      <button @click="changeC2">修改第二台车</button>
      <button @click="changePer">修改人</button>
    </div>
  </template>
    
  <script setup lang="ts" name="App">
  import {reactive, toRef, watch} from 'vue'
  let person = reactive({
    name: '章三',
    age: 18,
    car:{
      c1:'奔驰',
      c2:'宝马'
  }
  })
  
  function changeName(){
      person.name += '~'
    }

    function changeAge(){
        person.age += 1
    }

    function changePer(){
      Object.assign(person,{name:"zhang",age:19,car:{c1:"小米su7"}})
    }

    function changeC1(){
      person.car.c1 = '奥迪'
    }
    function changeC2(){
      person.car.c2 = '大众'
    }

    watch(()=>person.name,(newValue,oldValue)=>{
      console.log("person name改变了",newValue,oldValue)
    })

       // 监视的还是一个对象，可以直接写，也可以写成函数式
    watch(()=>person.car,(newValue,oldValue)=>{
      console.log("person name改变了",newValue,oldValue)
    },{deep:true})
     
  </script>
```

> 情况五：监视上述多个数据

```vue
watch([()=>person.name,person.car],(newValue,oldValue)=>{
      console.log("person name和car改变了",newValue,oldValue)
    })
```
## watchEffect

* 官网：立即运行一个函数，同时响应式地追踪其依赖，并在依赖更改时重新执行该函数。

* `watch`对比`watchEffect`

>   1. 都能监听响应式数据的变化，不同的是监听数据变化的方式不同
  >
  > 2. `watch`：要明确指出监视的数据
  >
  > 3. `watchEffect`：不用明确指出监视的数据（函数中用到哪些属性，那就监视哪些属性）。

```vue
<template>
  <div class="person">
    <h1>需求：在水温大于60或水位大于80的时候给服务器发送请求</h1>
    <h1>水温：{{ temp }}</h1>
    <h1>水位：{{ height }}</h1>
    <button @click="changeTemp">增加温度</button>
    <button @click="changeHeight">增加水位</button>
  </div>
</template>
  
<script setup lang="ts" name="App">
  import {ref, watch,watchEffect} from 'vue'
  let temp = ref(10)
  let height = ref(0)

  function changeTemp(){
    temp.value += 10
  }
  function changeHeight(){
    height.value += 10
  }
  // watch实现
  // watch([temp,height],(value)=>{
  //   let [newTemp,newHight] = value
  //   if (newTemp > 60 || newHight > 80) {
  //       console.log("给服务器发请求",newTemp,newHight )
  //   }
  // })

  watchEffect((value)=>{

    if (temp.value > 60 || height.value > 80) {
        console.log("给服务器发请求",temp.value,height.value )
    }
  })
   
</script>
```
## 标签中的ref属性

作用：用于注册模板引用。

> * 用在普通`DOM`标签上，获取的是`DOM`节点。
>
> * 用在组件标签上，获取的是组件实例对象。

用在普通`DOM`标签上：

```vue
<template>
  <div class="person">
    <h1 ref="title1">尚硅谷</h1>
    <h2 ref="title2">前端</h2>
    <h3 ref="title3">Vue</h3>
    <input type="text" ref="inpt"> <br><br>
    <button @click="showLog">点我打印内容</button>
  </div>
</template>

<script lang="ts" setup name="Person">
  import {ref} from 'vue'
	
  let title1 = ref()
  let title2 = ref()
  let title3 = ref()

  function showLog(){
    // 通过id获取元素
    const t1 = document.getElementById('title1')
    // 打印内容
    console.log((t1 as HTMLElement).innerText)
    console.log((<HTMLElement>t1).innerText)
    console.log(t1?.innerText)
    
		/************************************/
		
    // 通过ref获取元素
    console.log(title1.value)
    console.log(title2.value)
    console.log(title3.value)
  }
</script>
```

用在组件标签上：

```vue
<!-- 父组件App.vue -->
<template>
  <Person ref="ren"/>
  <button @click="test">测试</button>
</template>

<script lang="ts" setup name="App">
  import Person from './components/Person.vue'
  import {ref} from 'vue'

  let ren = ref()

  function test(){
    console.log(ren.value.name)
    console.log(ren.value.age)
  }
</script>


<!-- 子组件Person.vue中要使用defineExpose暴露内容 -->
<script lang="ts" setup name="Person">
  import {ref,defineExpose} from 'vue'
	// 数据
  let name = ref('张三')
  let age = ref(18)
  /****************************/
  /****************************/
  // 使用defineExpose将组件中的数据交给外部
  defineExpose({name,age})
</script>
```
## props

- **Props​**​ 是组件之间传递数据的核心机制，用于父组件向子组件传递数据。

```typescript
// index.ts
// 定义一种接口，用于限制person对象的具体属性
export interface PersonInter {
    id:string,
    name:string,
    age:number
    // x?:number // 可选
}

// 自定义类型
// export type Persons = Array<PersonInter>
export type Persons = PersonInter[]
```

```vue
<!-- App.vue -->
<template>
     <!-- <person a="哈哈" :list="personList"/>  -->
      <!-- v-if 判断表达式是否成立，不成立销毁组件及状态 -->
       <!-- v-show逻辑一样，但不销毁组件，只是通过display让组件不显示 -->
     <person a="哈哈" v-if="a" v-show="a"/> 

</template>

<script lang="ts" name="App" setup>
    import person from "./components/Person.vue";
    import { type Persons } from "@/types";
    import { reactive } from "vue";

    let personList = reactive<Persons>([
        {id:'1',name:'王五',age:10},
        {id:'2',name:'李四',age:20},
    ])
</script>

<style>
    /* 样式 */
    .app {
        background-color: aqua;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
</style>
```

```vue
<!--Person.vue-->
<template>
  <div class="person">

    <ul>
      <li v-for="i in list" :key="i.id">{{ i }}</li>
    </ul>
  
  </div>
</template>
  
<script setup lang="ts" name="App">
  // define开头都属于宏函数可以不导入使用 
  import { defineProps,withDefaults } from 'vue';
  import { type Persons } from '@/types';

  // 仅接受变量
  // defineProps(['a','list'])

  // 接收加限制
  // defineProps<{list:Persons}>()

  // 接收加限制加必要性加默认值
   withDefaults(defineProps<{list?:Persons}>(),{
    list:()=>[{id:'1',name:'zhangsan',age:19}]
   })



  // 接收加保存
  // let x = defineProps(['a','list'])
  // console.log(x.a)

</script>

<!-- scoped：定义局部样式 -->
<style scoped>
  .person {
    background-color: aqua;
  }
</style>

```
## 生命周期

> 创建阶段：`setup`
  >
  > 挂载阶段：`onBeforeMount`、`onMounted`
  >
  > 更新阶段：`onBeforeUpdate`、`onUpdated`
  >
  > 卸载阶段：`onBeforeUnmount`、`onUnmounted`

* 常用的钩子：`onMounted`(挂载完毕)、`onUpdated`(更新完毕)、`onBeforeUnmount`(卸载之前)

* 示例代码：

  ```vue
  <template>
    <div class="person">
      <h2>当前求和为：{{ sum }}</h2>
      <button @click="changeSum">点我sum+1</button>
    </div>
  </template>
  
  <!-- vue3写法 -->
  <script lang="ts" setup name="Person">
    import { 
      ref, 
      onBeforeMount, 
      onMounted, 
      onBeforeUpdate, 
      onUpdated, 
      onBeforeUnmount, 
      onUnmounted 
    } from 'vue'
  
    // 数据
    let sum = ref(0)
    // 方法
    function changeSum() {
      sum.value += 1
    }
    console.log('setup')
    // 生命周期钩子
    onBeforeMount(()=>{
      console.log('挂载之前')
    })
    onMounted(()=>{
      console.log('挂载完毕')
    })
    onBeforeUpdate(()=>{
      console.log('更新之前')
    })
    onUpdated(()=>{
      console.log('更新完毕')
    })
    onBeforeUnmount(()=>{
      console.log('卸载之前')
    })
    onUnmounted(()=>{
      console.log('卸载完毕')
    })
  </script>
  ```
## 自定义Hooks

- 下载axios包

```node
npm i axios
```