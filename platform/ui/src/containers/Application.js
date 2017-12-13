import React from 'react';
import { Route, Switch } from 'react-router-dom';
import LoginPage from './LoginPage';
import IndexPage from './IndexPage';
import Cookies from 'universal-cookie';
import { request } from '../utils';
import { message } from 'antd';

const cookies = new Cookies();

export default class Application extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      token: cookies.get('sessionId'),
      user: null,
    };

    if (this.state.token) {
      this.loadUserProfile();
    }
  }

  handleLogin = (token, user) => {
    cookies.set('sessionId', token, { path: '/' });

    this.setState({
      token: token,
      user: user,
    });

    this.loadUserProfile();
  };

  handleLogout = () => {
    cookies.remove('sessionId');

    this.setState({
      token: null,
      user: null,
    });
  };

  loadUserProfile = async () => {
    if (!this.state.token) {
      return;
    }

    let response = null;
    try {
      response = await request('/users/me/', {
        method: 'GET',
        headers: {
          'Authorization': 'Token ' + this.state.token,
        },
      });
    } catch (e) {
      message.error(
        'Sorry, server temporary unavailable. Please try again later.',
      );
      return;
    }

    if (Math.round(response.status / 100) * 100 === 500) {
      message.error('Internal server error occurred.');
      return;
    }

    let data = await response.json();

    if (response.ok) {
      this.setState({
        user: data,
      });
    } else {
      message.error(data.error_message);
    }


  };

  render() {
    return (
      <Switch>
        <Route exact path="/login/">
          <LoginPage onLogin={this.handleLogin} />
        </Route>
        <Route path="/">
          <IndexPage user={this.state.user} onLogout={this.handleLogout} />
        </Route>
      </Switch>
    );
  }
}