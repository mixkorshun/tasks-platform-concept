import React from 'react';
import { Button, Form, Input, message } from 'antd';
import { request } from '../../utils';

class AddTaskForm extends React.Component {

  handleSubmit(e) {
    e.preventDefault();

    this.props.form.validateFields(async (err, values) => {
      if (!err) {

        let resp;
        try {
          resp = await request('/tasks/', {
            method: 'POST',
            headers: {
              'Authorization': this.props.authorization ? 'Token ' + this.props.authorization : '',
            },
            body: JSON.stringify({
              name: values.name,
              price: parseFloat(values.price),
              description: values.description,
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

        this.props.onTaskAdd && this.props.onTaskAdd();
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;

    return (
      <Form onSubmit={(e) => this.handleSubmit(e)}>
        <Form.Item>
          {getFieldDecorator('name', {
            rules: [
              {
                required: true,
                message: 'Please input task name!',
              },
            ],
          })(
            <Input placeholder="Name" />,
          )}
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('price', {
            rules: [
              {
                required: true,
                message: 'Please input task price!',
              },
            ],
          })(
            <Input
              prefix="$ " type="number" placeholder="Price"
            />,
          )}
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('description')(
            <Input.TextArea rows={4} placeholder="Description" />,
          )}
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">Submit</Button>
        </Form.Item>
      </Form>
    );
  }
}

export default Form.create()(AddTaskForm);