import React from 'react';
import ReactDOM from 'react-dom';
import Application from './containers/Application';

import 'antd/dist/antd.css';
import { HashRouter } from 'react-router-dom';

ReactDOM.render(
  <HashRouter>
    <Application />
  </HashRouter>,
  document.getElementById('root'),
);
