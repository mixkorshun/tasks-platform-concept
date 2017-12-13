import React from 'react';
import { Col, Layout, Row } from 'antd';
import LoginForm from '../components/LoginForm';
import { Link } from 'react-router-dom';

export default class LoginPage extends React.Component {
  render() {
    return (
      <Layout style={{ height: '100%' }}>
        <Row>
          <Col span={8} offset={8}>
            <h1 style={{ textAlign: 'center', margin: '50px 0' }}>Sign In</h1>

            <LoginForm onLogin={this.props.onLogin} />
          </Col>
        </Row>

      </Layout>
    );
  }
}
