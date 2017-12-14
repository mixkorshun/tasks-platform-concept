import React from 'react';
import { Col, Layout, message, Row } from 'antd';
import RegistrationForm from '../../components/RegistrationForm';
import { Link, withRouter } from 'react-router-dom';

class RegistrationPage extends React.Component {

  onRegister = () => {
    this.props.onRegister && this.props.onRegister();

    this.props.history.push('/login/');

    message.success(
      'Your account has created successfully. ' +
      'Now you can sign in.',
    );
  };

  render() {
    return (
      <Layout style={{ height: '100%' }}>
        <Row>
          <Col span={8} offset={8}>
            <h1 style={{ textAlign: 'center', margin: '50px 0' }}>Sign Up</h1>

            <RegistrationForm onRegister={this.onRegister} />

            <div style={{ margin: '25px 0', textAlign: 'center' }}>
              Already have an account? <br />

              <Link to="/login/">Sign In</Link>
            </div>
          </Col>
        </Row>

      </Layout>
    );
  }
}

export default withRouter(RegistrationPage);
