import React from 'react';
import { Col, Layout, Row } from 'antd';
import LoginForm from '../components/LoginForm';
import { Link } from 'react-router-dom';

export default class LoginPage extends React.Component {
  render() {
    return (
      <Layout style={{ height: '100%' }}>
        <Link to="/" style={{ margin: '10px 15px', color: '#aaa' }}>
          &lt; back to home
        </Link>

        <Row>
          <Col span={8} offset={8}>
            <h1 style={{ textAlign: 'center', margin: '50px 0' }}>Sign In</h1>

            <LoginForm />
          </Col>
        </Row>

      </Layout>
    );
  }
}
