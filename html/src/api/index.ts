import http from "./http";

const API = {

    // 编辑接口
    getSourceList() {
        return http.get('/source/list')
    },
    getSingleSource(id: string) {
        return http.get(`/source/${id}`)
    },
    saveSource(source: any) {
        return http.post('/source/save', source)
    },
    importSource(obj: any) {
        return http.post('/source/import', obj)
    },


    // test接口
    testSourceSearch(obj: any) {
        return http.post('/test/search', obj)
    },
    testSourceDetail(obj: any) {
        return http.post('/test/detail', obj)
    },
    testSourcePlay(obj: any) {
        return http.post('/test/play', obj)
    },

    // 对外接口
    search(keyword: string, refresh: string) {
        if (refresh) {
            return http.get(`/search?k=${keyword}&refresh=${refresh}`)
        } else {
            return http.get(`/search?k=${keyword}`)
        }
    },
    detail(id: string, url: string, refresh: string) {
        if (refresh) {
            return http.post('/detail', {id: id, url: url, refresh: refresh})
        } else {
            return http.post('/detail', {id: id, url: url})
        }
    },
    play(id: string, url: string, refresh: string) {
        if (refresh) {
            return http.post('/play', {id: id, url: url, refresh: refresh})
        } else {
            return http.post('/play', {id: id, url: url})
        }
    },

    searchHint(keyword: string) {
        return http.get(`/search/hint?k=${keyword}`)
    }
}

export default API
