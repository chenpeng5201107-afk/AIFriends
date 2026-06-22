<script setup lang="ts">
import {onBeforeMount, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/view/user/profile/components/icons/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(() => props.photo, (newValue) => {
  myPhoto.value = newValue
})

const fileInputRef:any = useTemplateRef('file-input-ref')
const modalRef:any = useTemplateRef('modal-ref')
const croppieRef:any = useTemplateRef('croppie-ref')
let croppie:any = null

async function open(photo:any) {
  modalRef.value.showModal()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: {
        width: 200,
        height: 200,
        type: 'circle'
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
    url: photo,
  })
}

async function handleCrop() {
  if (!croppie) return

  myPhoto.value = await croppie.result({
    'type':'base64',
    'size':'viewport',
  })

  modalRef.value?.close()
}

function handleFileInputChange(e:any) {
  const file = e.target.files[0]
  e.target.value=''
  if (!file) return
  const reader = new FileReader()
  reader.onload = ()=>{
    open(reader.result)
  }
  reader.readAsDataURL(file)
}

onBeforeUnmount(()=>{
  croppie?.destroy()
})

defineExpose({myPhoto})

</script>

<template>
<div class="flex justify-center" >
  <div class="avatar relative">
    <div v-if="myPhoto" class="w-28 rounded-full ">
      <img :src="myPhoto" alt="">
    </div>
    <div v-else class="w-28 h-28 bg-base-300 rounded-full"></div>
    <div @click="fileInputRef.click()" class="w-28 h-28 rounded-full bg-black/20 absolute left-0 right-0 flex justify-center items-center cursor-pointer">
      <CameraIcon/>
    </div>
  </div>
</div>

<input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="handleFileInputChange"/>

<dialog ref="modal-ref" class="modal">
  <div class="modal-box transition-none">
    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="modalRef.close()">✕</button>

    <div ref="croppie-ref" class="flex flex-col my-4"></div>
    <div class="modal-action">
      <button class="btn" @click="modalRef.close()">取消</button>
      <button class="btn btn-primary" @click="handleCrop">裁剪</button>
    </div>
  </div>
</dialog>
</template>

<style scoped>

</style>