const Cookie = {
    get: (name: string) => {
        const reg = new RegExp(`(^| )${name}=([^;]*)(;|$)`);
        const arr = document.cookie.match(reg);
        if (arr) {
            return unescape(arr[2]);
        } else {
            return null;
        }
    },
    set: (name: string, value: string, expires: any, path: string, domain: string, secure: boolean) => {
        let cookieText = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;
        if (expires instanceof Date) {
            cookieText += `; expires=${expires.toUTCString()}`;
        }
        if (path) {
            cookieText += `; path=${path}`;
        }
        if (domain) {
            cookieText += `; domain=${domain}`;
        }
        if (secure) {
            cookieText += `; secure`;
        }
        document.cookie = cookieText;
    },
    del: (name: string, path: string, domain: string, secure: boolean) => {
        Cookie.set(name, '', new Date(0), path, domain, secure);
    }
}

export default Cookie