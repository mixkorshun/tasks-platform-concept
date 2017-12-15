import React from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';

import LoginPage from './Authorization/LoginPage';
import RegistrationPage from './Authorization/RegistrationPage';

import EmployeeIndexPage from './Employee/IndexPage';
import EmployerIndexPage from './Employer/IndexPage';
import EmployerAddTaskPage from './Employer/AddTaskPage';

import Cookies from 'universal-cookie';
import { request } from '../utils';
import { message } from 'antd';
import AuthorizedLayout from '../components/AuthorizedLayout';
import EnsureLoggedIn from '../components/EnsureLoggedIn';

const cookies = new Cookies();

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

  handleLogin = (token) => {
    cookies.set('sessionId', token, { path: '/' });

    this.setState({
      token: token,
    });

    this.loadUserProfile();
  };

  handleUserChanged = () => {
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
    } else if (response.status === 403) {
      this.handleLogout();
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

        <Route exact path="/register/">
          <RegistrationPage />
        </Route>

        <EnsureLoggedIn isAuthorized={this.state.token}>
          <AuthorizedLayout
            user={this.state.user}
            onLogout={this.handleLogout}
          >
            {this.state.user && this.state.user.type === 'employee' && (
              <Switch>
                <Route exact path="/">
                  <EmployeeIndexPage
                    authorization={this.state.token}
                    user={this.state.user}
                    onUserChanged={this.handleUserChanged}
                  />
                </Route>
              </Switch>
            )}

            {this.state.user && this.state.user.type === 'employer' && (
              <Switch>
                <Route exact path="/">
                  <EmployerIndexPage
                    authorization={this.state.token}
                    user={this.state.user}
                    onUserChanged={this.handleUserChanged}
                  />
                </Route>

                <Route exact path="/add_task/">
                  <EmployerAddTaskPage
                    authorization={this.state.token}
                    user={this.state.user}
                    onUserChanged={this.handleUserChanged}
                  />
                </Route>
              </Switch>
            )}
          </AuthorizedLayout>
        </EnsureLoggedIn>
      </Switch>
    );
  }
}

export default withRouter(Application);
