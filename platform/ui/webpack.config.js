const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');

const isProduction = (process.env.NODE_ENV === 'production');

let config = {
  context: path.resolve(__dirname, 'src'),
  entry: {
    index: ['babel-polyfill', './index.js'],
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.js',
    publicPath: '/',
  },
  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader?sourceMap',
      },
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['react', 'es2015', 'es2017'],
          plugins: ['transform-class-properties'],
        },
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          name: 'fonts/[name].[ext]',
        },
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html',
      filename: 'index.html',
      inject: 'body',
    }),
  ],
};

if (isProduction) {
  config['plugins'].push(
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: { warnings: false },
      output: { comments: false },
    }),
  );
}

module.exports = config;
