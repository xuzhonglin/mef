import {createRouter, createWebHistory} from 'vue-router'
import AdminSourceIndex from '~/components/admin/source/Index.vue'
import AdminSourceEdit from '~/components/admin/source/Edit.vue'
import AdminLogin from '~/components/admin/Login.vue'
import Index from '~/components/page/Index.vue'
import Search from '~/components/page/Search.vue'
import Detail from '~/components/page/Detail.vue'
import Cookie from "../utils/cookie";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index,
            meta: {
                title: '首页'
            }
        },
        {
            path: '/search',
            name: 'search',
            component: Search,
            meta: {
                title: '搜索'
            }
        },
        {
            path: '/detail',
            name: 'detail',
            component: Detail,
            meta: {
                title: '详情'
            }
        },
        {
            path: '/admin/login',
            name: 'adminLogin',
            component: AdminLogin,
            meta: {
                title: '登录',
                requireAuth: false
            }
        },
        {
            path: '/admin/source/list',
            name: 'adminSourceList',
            component: AdminSourceIndex,
            meta: {
                title: '数据源列表',
                requireAuth: true
            }
        },
        {
            path: '/admin/source/edit',
            name: 'adminSourceEdit',
            component: AdminSourceEdit,
            meta: {
                title: '数据源编辑',
                requireAuth: true
            }
        }
    ]
});

const setupTitle = (to: any) => {
    let title: any = ''
    //详情
    if (to.name == 'detail') {
        let playUrl = to.query.url
        let playTitle = sessionStorage.getItem(`DETAIL_${playUrl}`)
        title = playTitle ? JSON.parse(playTitle).title : to.meta.title
    }
    //搜索
    else if (to.name == 'search') {
        title = to.query.keyword ? `搜索：${to.query.keyword}` : to.meta.title
    }
    //其他有标题的页面
    else if (to.meta.title) {
        title = to.meta.title
    }
    if (title.length > 0) {
        document.title = `${title} - mef - 电影电视搜索平台`
    } else {
        document.title = `mef - 电影电视搜索平台`
    }
};


router.beforeEach((to, from, next) => {

    setupTitle(to);

    if (to.meta.requireAuth) {
        let token = Cookie.get('mef_token')
        if (!token) {
            console.log('未登录')
            next({
                path: '/admin/login',
                query: {redirect: to.fullPath}
            })
        } else {
            next()
        }
    } else {
        next()
    }

})

export default router

