const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    client: {
      webSocketURL: 'wss://10.0.3.69:8080/ws', // Ajusta con la URL de tu servidor
    },
  },
});
