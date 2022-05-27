// @ts-ignore
import axios, {AxiosRequestConfig, AxiosResponse} from 'axios'

const BASE_URL = import.meta.env.VITE_APP_BASE_URL

//创建axios的一个实例
const instance = axios.create({
    baseURL: BASE_URL + '/api', //接口统一域名
    timeout: 6000, //设置超时
    headers: {
        'Content-Type': 'application/json;charset=UTF-8;',
    }
});

//请求拦截器
instance.interceptors.request.use((config: AxiosRequestConfig) => {

    //@ts-ignore
    if (config.newUrl) {
        //@ts-ignore
        config.baseURL = config.newUrl
    } else {
        config.baseURL = BASE_URL + '/api'
    }

    //若请求方式为post，则将data参数转为JSON字符串
    if (config.method === 'POST') {
        config.data = JSON.stringify(config.data);
    }
    return config;
}, (error: any) =>
    // 对请求错误做些什么
    Promise.reject(error));

//响应拦截器
instance.interceptors.response.use((response: AxiosResponse) => {

    // let resUrl = response.request.responseURL;
    // let reqUrl: any = response.config.url;
    //
    // resUrl = decodeURIComponent(resUrl);
    //
    // if (resUrl.indexOf(reqUrl) === -1) {
    //     console.log('需要重定向', resUrl, reqUrl);
    //     window.location.href = resUrl
    // }

    return response.data;
}, (error: any) => {
    console.log(error)
    //响应错误
    if (error.response && error.response.status) {
        return Promise.reject(error);
    }
    return Promise.reject(error);
});


const http = {
    get(url: string, data: any = null, config: any = null) {
        return instance.get(url, {
            params: data,
            ...config
        })
    },
    post(url: string, data: any = null, config: any = null) {
        return instance.post(url, data, {...config})
    }
}

export default http




