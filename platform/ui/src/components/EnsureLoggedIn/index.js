import React from 'react';
import { withRouter } from 'react-router-dom';

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

export default withRouter(EnsureLoggedIn);
