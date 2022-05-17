<template>
  <div class="header">
    <a class="logo" href="/admin/source/list">
      <img src="/index_logo.png"/>
      <div class="title">{{ title }}</div>
    </a>
    <div>
      <a class="back-link" @click="btnAction" v-if="btnText.length!==0">{{ btnText }}</a>
      <a class="back-link" @click="secBtnAction" v-if="secBtnText.length!==0">{{ secBtnText }}</a>
    </div>
  </div>
</template>

<script lang="ts">


export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    btnText: {
      type: String,
      default: '',
    },
    btnAction: {
      type: Function,
      default: () => {
      },
    },
    secBtnText: {
      type: String,
      default: '',
    },
    secBtnAction: {
      type: Function,
      default: () => {
      },
    },
  },
}


</script>

<style scoped lang="scss">
.header {
  height: 3rem;
  background: #409EFF;
  color: #fff;
  line-height: 3rem;
  /*font-size: 20px;*/
  padding: 0 2rem;
  display: flex;

  .logo {
    display: flex;
    align-items: center;
    height: 100%;

    img {
      //width: 40px;
      height: 27px;
      margin-right: 10px;
      object-fit: scale-down;
    }

    .title {
      font-size: 18px;
      color: #fff;
    }
  }
}

.back-link {
  margin-left: 25px;
  font-size: 12px;
  color: #fff;
  border: 1px solid #fff;
  padding: 2px 5px;
  border-radius: 3px;
  cursor: pointer;
}

.back-link:hover {
  color: #409EFF;
  background: #fff;
}

/*包含以下五种的链接*/
a {
  text-decoration: none;
}

/*正常的未被访问过的链接*/
a:link {
  text-decoration: none;
}

/*已经访问过的链接*/
a:visited {
  text-decoration: none;
}

/*鼠标划过(停留)的链接*/
a:hover {
  text-decoration: none;
}

/* 正在点击的链接，鼠标在元素上按下还没有松开*/
a:active {
  text-decoration: none;
}

/* 获得焦点的时候 鼠标松开时显示的颜色*/
a:focus {
  text-decoration: none;
}
</style>