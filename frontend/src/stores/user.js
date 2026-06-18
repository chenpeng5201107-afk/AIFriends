import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useUserStore = defineStore('user', ()=>{
    const username = ref('')
    const id = ref(1)
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')

    function isLogin() {
        return !!accessToken.value
    }

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

    return {
        username,
        id,
        photo,
        profile,
        accessToken,
        isLogin,
        setAccessToken,
        setUserInfo,
        logout
    }
})