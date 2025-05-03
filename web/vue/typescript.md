
```typescript
// 定义一种接口，用于限制person对象的具体属性
export interface PersonInter {
    id:string,
    name:string,
    age:number
}

// 自定义类型
// export type Persons = Array<PersonInter>
export type Persons = PersonInter[]
```

```vue
<template>
  <div class="person">
    <h1 ref="temp">title2</h1>
  
  </div>
</template>
  
<script setup lang="ts" name="App">
  import {ref} from 'vue'
   /* 
   '@': fileURLToPath(new URL('./src', import.meta.url))
   vite.config.js中配置的路径别名
   */
  import { type PersonInter,type Persons } from '@/types'
  let person:PersonInter = {
    id:'1',
    name:'123',
    age:12
  }

  let personList:Persons = [
    {id:'1',name:'王五',age:10},
    {id:'2',name:'李四',age:20},
  ]

</script>

<!-- scoped：定义局部样式 -->
<style scoped>
  .person {
    background-color: aqua;
  }
</style>
```