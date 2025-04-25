const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  chainWebpack: config => {
    config.module
      .rule('leaflet')
      .test(/\.(png|jpg|jpeg|gif|svg|webp)$/)
      .include.add(/node_modules\/leaflet/)
      .end()
      .use('file-loader')
      .loader('file-loader')
      .options({
        name: 'img/[name].[hash:8].[ext]'
      });
  }
};