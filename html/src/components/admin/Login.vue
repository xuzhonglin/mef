<template>
  <div class="login-box">
    <!--    <div class="login-title">登录</div>-->
    <img class="login-image" src="/search_logo.png"/>
    <input class="login-input" placeholder="用户名" name="username" v-model="username"/>
    <input class="login-input" placeholder="登录密码" type="password" name="password" v-model="password"/>
    <input class="login-input" placeholder="动态码" maxlength="6" name="totpCode" v-model="totpCode"/>
    <button class="login-button" @click="login">登录</button>
  </div>
</template>

<script lang="ts" setup>

import {ref} from "vue";
import Api from "../../api";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus/es";


const username = ref('')
const password = ref('')
const totpCode = ref('')
const router = useRouter()

const login = async () => {
  if (!username.value || !password.value || !totpCode.value) {
    ElMessage.error('请检查输入')
    return
  }
  const res = await Api.login(username.value, password.value, totpCode.value)
  if (res && res.code === 200) {
    ElMessage.success('登录成功')
    console.log(router.currentRoute.value)
    setTimeout(() => {
      let redirect_url: any = router.currentRoute.value.query.redirect
      if (redirect_url) {
        window.location.href = redirect_url
        // router.push(redirect_url)
      } else {
        window.location.href = '/admin/source/list'
        // router.push('/admin/source/list')
      }
    }, 1000)

  } else {
    ElMessage.error(res.msg)
  }
}

document.onkeyup = (e: any) => {
  // console.log(e)
  if (e.keyCode !== 13) {
    return
  }
  login()
}

</script>

<style scoped lang="scss">
.login-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 400px;
  //height: 200px;
  background-color: #ffffff;
  border-radius: 5px;
  padding: 40px;
  margin: 20vh auto;

  .login-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 30px;
  }

  .login-image {
    //width: 100px;
    height: 40px;
    margin-bottom: 30px;
  }

  .login-input {
    width: calc(100% - 20px);
    height: 33px;
    border-radius: 5px;
    border: 1px solid #e1e1e1;
    padding: 0 10px;
    margin-bottom: 20px;

    //&:last-of-type {
    //  margin-bottom: 0;
    //}

    &:focus {
      outline: none;
      border: 1px solid #409EFF;
    }
  }

  .login-button {
    width: 100%;
    height: 38px;
    border-radius: 5px;
    background-color: #409EFF;
    color: #ffffff;
    font-size: 16px;
    cursor: pointer;
    border: 1px solid #409EFF;
    //margin: 20px 0;
    margin: 10px auto;

    &:hover {
      border: 1px solid #3786d9;
      background-color: #3786d9;
    }
  }

}
</style>