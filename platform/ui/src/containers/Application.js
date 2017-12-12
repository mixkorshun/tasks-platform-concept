import React from 'react';
import { Route, Switch } from 'react-router-dom';
import LoginPage from './LoginPage';
import IndexPage from './IndexPage';

export default class Application extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: {
        id: 1,
        email: 'admin@localhost',
        token: null,
      },
    };
  }

  render() {
    return (
      <Switch>
        <Route exact path="/login/">
          <LoginPage />
        </Route>
        <Route path="/">
          <IndexPage user={this.state.user} />
        </Route>
      </Switch>
    );
  }
}