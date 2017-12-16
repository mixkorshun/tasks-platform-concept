const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const webpack = require('webpack');

const isProduction = (process.env.NODE_ENV === 'production');

let config = {
  context: path.resolve(__dirname, 'src'),
  entry: {
    index: ['babel-polyfill', './index.js'],
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.[hash].js',
    publicPath: '/',
  },
  module: {
    loaders: [
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract(
          { loader: 'css-loader', options: { minimize: isProduction } },
          'style-loader',
        ),
      }, {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['react', 'es2015', 'es2017'],
          plugins: ['transform-class-properties'],
        },
      }, {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          name: 'fonts/[name].[ext]',
          limit: 4096,
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
    new webpack.DefinePlugin({
      'process.env': { NODE_ENV: JSON.stringify(process.env.NODE_ENV) },
      'api_endpoint': JSON.stringify(process.env.API_ENDPOINT || '/api'),
    }),
    new ExtractTextPlugin("[name].bundle.[hash].css")
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
