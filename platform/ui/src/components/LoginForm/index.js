import React from 'react';
import { Button, Form, Icon, Input } from 'antd';

class LoginForm extends React.Component {
  render() {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched } = this.props.form;

    return (
      <Form className="login-form">
        <Form.Item>
          {getFieldDecorator('email', {
            rules: [
              {
                required: true,
                message: 'Please input your email!',
              },
            ],
          })(
            <Input
              prefix={<Icon
                type="mail"
                style={{ color: 'rgba(0,0,0,.25)' }}
              />} placeholder="Email"
            />,
          )}
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('password', {
            rules: [
              {
                required: true,
                message: 'Please input your password!',
              },
            ],
          })(
            <Input
              prefix={<Icon
                type="lock"
                style={{ color: 'rgba(0,0,0,.25)' }}
              />} type="password" placeholder="Password"
            />,
          )}
        </Form.Item>
        <Form.Item style={{textAlign: 'center'}}>
          <Button
            type="primary"
            htmlType="submit"
            className="login-form-button"
          >Sign in</Button>
        </Form.Item>
      </Form>
    );
  }
}

export default Form.create()(LoginForm);