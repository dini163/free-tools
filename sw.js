/**
 * FreeDevTools Service Worker
 * 实现缓存策略，提升网站加载速度
 */

const CACHE_NAME = 'free-tools-v1.2.1';
const ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/css/style.min.css',
    '/js/theme.min.js',
    '/js/i18n.min.js',
    '/manifest.json'
];

// 安装事件 - 缓存关键资源
self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching app shell...');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .then(() => {
                console.log('[SW] Install completed');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[SW] Install failed:', error);
            })
    );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME) {
                            console.log('[SW] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('[SW] Activation completed');
                return self.clients.claim();
            })
    );
});

// 请求拦截 - 缓存优先策略
self.addEventListener('fetch', (event) => {
    // 只处理 GET 请求
    if (event.request.method !== 'GET') {
        return;
    }
    
    // 跳过外部请求
    if (!event.request.url.includes(self.location.origin)) {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then((cachedResponse) => {
                // 如果缓存中有，直接返回
                if (cachedResponse) {
                    console.log('[SW] Serving from cache:', event.request.url);
                    
                    // 后台更新缓存（stale-while-revalidate）
                    fetchAndCache(event.request);
                    
                    return cachedResponse;
                }
                
                // 否则从网络获取
                return fetchAndCache(event.request);
            })
            .catch((error) => {
                console.error('[SW] Fetch failed:', error);
                return fetch(event.request);
            })
    );
});

// 从网络获取并缓存
function fetchAndCache(request) {
    return fetch(request)
        .then((response) => {
            // 检查响应是否有效
            if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
            }
            
            // 克隆响应（因为响应流只能读取一次）
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
                .then((cache) => {
                    console.log('[SW] Caching new resource:', request.url);
                    cache.put(request, responseToCache);
                });
            
            return response;
        })
        .catch((error) => {
            console.error('[SW] Network request failed:', error);
            throw error;
        });
}

// 监听消息
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

console.log('[SW] Service Worker loaded');
