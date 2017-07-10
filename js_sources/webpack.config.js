'use strict';

const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');
const merge = require('webpack-merge');

const APP_DIR = path.resolve(__dirname, 'src');
const BUILD_DIR = path.resolve(__dirname, "..", "autonomie/static/js/build/");
var PROD = (process.env.NODE_ENV === 'production');

const config = {
  entry: {
    task: path.join(APP_DIR, 'task', 'task.js')
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          presets: ['es2015']
        }
      },
      {
        test: /\.mustache$/,
        loader: "handlebars-loader"
      }
    ]
  },
  output: {
    path: BUILD_DIR,
    filename: PROD ? '[name].min.js': '[name].js'
  },
  plugins: PROD? [
      // Pre-Provide datas used by other libraries
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      jquery: 'jquery',
      _: 'underscore'
    }),
    new webpack.optimize.UglifyJsPlugin({
        compress: {
            warnings: false
        }
    })
  ]: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      jquery: 'jquery',
      _: 'underscore'
    })
  ],
  resolve: {
    root: path.join(__dirname, './src')
  },
  resolveLoader: {
    root: path.join(__dirname, './node_modules')
  }
};

module.exports = config;
