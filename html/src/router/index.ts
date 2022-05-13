import {createRouter, createWebHashHistory} from 'vue-router'
import SourceIndex from '~/components/source/Index.vue'
import SourceEdit from '~/components/source/Edit.vue'
import Index from '~/components/page/Index.vue'
import Search from '~/components/page/Search.vue'
import Detail from '~/components/page/Detail.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Index,
            meta: {
                title: '首页'
            }
        },
        {
            path: '/index',
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
            path: '/source/index',
            name: 'sourceIndex',
            component: SourceIndex,
            meta: {
                title: '数据源'
            }
        },
        {
            path: '/source/edit',
            name: 'sourceEdit',
            component: SourceEdit,
            meta: {
                title: '数据源编辑'
            }
        }
    ]
});

router.beforeEach((to, from, next) => {
    // console.log(to)
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
    } else {
        title = ''
    }
    if (title.length > 0) {
        document.title = `${title} - mef - 电影电视搜索平台`
    } else {
        document.title = `mef - 电影电视搜索平台`
    }
    next()
})

export default router

