/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: {
    unoptimized: true
  },
  trailingSlash: true,
  // 注释掉API重写，因为静态导出不支持
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/ai/:path*',
  //       destination: 'http://localhost:8000/:path*',
  //     },
  //   ]
  // }
}

module.exports = nextConfig