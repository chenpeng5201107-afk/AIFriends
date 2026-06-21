<script setup lang="ts">
import {nextTick, onBeforeMount, ref, useTemplateRef} from "vue";
import {watch} from "vue";
import CameraIcon from "@/view/user/profile/components/icons/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)
const fileinput = useTemplateRef('fileinput')
const modalref = useTemplateRef('modalref')
const croppieref = useTemplateRef('croppie-ref')
let croppie:any= null

// 安全的点击处理
const handleAvatarClick = () => {
  fileinput.value?.click() // 使用可选链
}

const handleClose = () => {
  modalref.value?.close()
}

watch(()=>props.photo,newVal=>{
  myPhoto.value = newVal
})

async function crop() {
  if(!croppie) return

  myPhoto.value = await croppie.result({
    'type':'base64',
    'size':'viewport',
  })

  modalref.value?.close()
}

async function open(result:any){
  modalref.value?.showModal()
  await nextTick()

  if(!croppie) {
    croppie = new Croppie(croppieref.value as HTMLElement, {
      viewport: {
        width: 200,
        height: 200,
        type: 'square'
      },
      boundary: {
        width: 300,
        height: 300
      },
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: result,
  })
}

function onFileChange(e:any){
  const file = e.target.files[0]
  e.target.value = ''
  if ( !file) return

  const reader = new FileReader()
  reader.onload = ()=>{
    open(reader.result)
  }
  reader.readAsDataURL(file)
}

onBeforeMount(()=>{
  croppie?.destroyed()
})

defineExpose({
  myPhoto,
})

</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="rounded-full w-28">
        <img :src="myPhoto" alt="">
      </div>
      <div @click="handleAvatarClick" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
  </div>

  <input ref="fileinput" type="file" accept="image/*" class="hidden" @change="onFileChange">

  <dialog ref="modalref" class="modal">
    <div class="modal-box transition-none">
      <button @click="handleClose" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">✕</button>

      <div ref="croppie-ref" class="flex flex-col justify-center my-4 "></div>

      <div class="modal-action">
        <button @click="handleClose" class="btn">取消</button>
        <button @click="crop" class="btn btn-neutral">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>