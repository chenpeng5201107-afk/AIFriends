<script setup lang="ts">
import {onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/view/user/profile/components/icons/CameraIcon.vue";
import Croppie from "croppie";
import 'croppie/croppie.css'

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, (newValue) => {
  myBackgroundImage.value = newValue
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
        width: 300,
        height: 500,
        type: 'square'
      },
      boundary: {
        width: 600,
        height: 700
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

  myBackgroundImage.value = await croppie.result({
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

defineExpose({myBackgroundImage})

</script>

<template>
<fieldset class="fieldset">
  <label class="label text-base">背景图片</label>
 <div class="avatar relative">
   <div v-if="myBackgroundImage" class="w-15 h-25 rounded-box">
     <img :src="myBackgroundImage" alt="">
   </div>
   <div v-else class="w-15 h-25 rounded-box bg-base-300"></div>
   <div @click="fileInputRef.click()" class="w-15 h-25 rounded-box absolute left-0 top-0 bg-black/20 flex justify-center items-center cursor-pointer">
     <CameraIcon/>
   </div>
 </div>

 </fieldset>

<input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="handleFileInputChange"/>

<dialog ref="modal-ref" class="modal">
  <div class="modal-box transition-none max-w-2xl">
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