import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

export const useUserStore = defineStore('user', ()=>{
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)

    const isLogin = computed(() => {
        return !!accessToken.value
    })

    function setAccessToken(token) {
        accessToken.value = token
    }

    function setUserInfo(data) {
        id.value = data.user_id
        username.value = data.username
        photo.value = data.photo
        profile.value = data.profile
    }

    function logout(){
        username.value = ''
        id.value = 0
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }

    function setHasPulledUserInfo(value) {
        hasPulledUserInfo.value = value
    }

    return {
        username,
        id,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
        setHasPulledUserInfo,
        hasPulledUserInfo,
    }
})