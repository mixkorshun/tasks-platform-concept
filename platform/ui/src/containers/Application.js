import React from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';
import LoginPage from './LoginPage';
import IndexPage from './IndexPage';
import Cookies from 'universal-cookie';
import { request } from '../utils';
import { message } from 'antd';

const cookies = new Cookies();

class EnsureLoggedIn extends React.Component {

  componentDidMount() {
    const { dispatch, currentURL } = this.props;

    if (!this.props.isAuthorized) {
      this.props.history.push('/login/');
    }
  }

  render() {
    if (this.props.isAuthorized) {
      return this.props.children;
    } else {
      return null;
    }
  }
}

EnsureLoggedIn = withRouter(EnsureLoggedIn);

class Application extends React.Component {
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

    this.props.history.push('/login/');
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
        <EnsureLoggedIn isAuthorized={this.state.token}>
          <Route path="/">
            <IndexPage user={this.state.user} onLogout={this.handleLogout} />
          </Route>
        </EnsureLoggedIn>
      </Switch>
    );
  }
}

Application = withRouter(Application);

export default Application;