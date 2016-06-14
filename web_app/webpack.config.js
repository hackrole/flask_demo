module.exports = {
  entry: {
    "vendor": "./app/vendor",
    "app": "./app/boot",
  },
  output: {
    path: __dirname,
    filename: 'app.bundle.js',
  },
  resolve: {
    extensions: ['', '.js', '.ts']
  },
  devtool: 'source-map',
  module: {
    loaders: [
      {
        test: /\.ts/,
        loaders: ['ts-loader'],
        exclude: /node_moduels/
      }
    ]
  },
  plugins: [
    new webpack.optimisze.CommonsChunkPlugin("vendor", "./dist/vendor.bundle.js"),
  ]
}
