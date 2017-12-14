import React from 'react';
import { Col, Layout, Row } from 'antd';
import LoginForm from '../../components/LoginForm';
import { Link, withRouter } from 'react-router-dom';

class LoginPage extends React.Component {
  onLogin = (token) => {
    this.props.onLogin && this.props.onLogin(token);

    this.props.history.push('/');
  };

  render() {
    return (
      <Layout style={{ height: '100%' }}>
        <Row>
          <Col span={8} offset={8}>
            <h1 style={{ textAlign: 'center', margin: '50px 0' }}>Sign In</h1>

            <LoginForm onLogin={this.onLogin} />

            <div style={{ margin: '25px 0', textAlign: 'center' }}>
              Don't have an account? <br />

              <Link to="/register/">Register</Link>
            </div>
          </Col>
        </Row>

      </Layout>
    );
  }
}

export default withRouter(LoginPage);