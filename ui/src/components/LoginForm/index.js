import React from 'react';
import { Button, Form, Icon, Input, message } from 'antd';
import { request } from '../../utils';

class LoginForm extends React.Component {

  handleSubmit(e) {
    e.preventDefault();

    this.props.form.validateFields(async (err, values) => {
      if (!err) {

        let resp;
        try {
          resp = await request('/users/login/', {
            method: 'POST',
            body: JSON.stringify({
              email: values.email,
              password: values.password,
            }),
          });
        } catch (e) {
          message.error(
            'Server Temporary Unavailable. ' +
            'Please try again in several minutes.',
          );
        }

        let result = await resp.json();

        if (!resp.ok) {
          if (Math.round(resp.status / 100) * 100 === 500) {
            message.error(
              'Server Temporary Unavailable. ' +
              'Please try again in several minutes.',
            );
          } else {
            message.error(result.error_message);
          }
          return;
        }

        this.props.onLogin && this.props.onLogin(result.token);
      }
    });
  };

  render() {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched } = this.props.form;

    return (
      <Form
        className="login-form"
        onSubmit={(e) => this.handleSubmit(e)}
      >
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
        <Form.Item style={{ textAlign: 'center' }}>
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