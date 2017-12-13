import React from 'react';

import { Button, Card, Tag, Tooltip } from 'antd';

class Status extends React.Component {
  render() {
    if (this.props.value === 'open') {
      return (
        <Tag color="#87d068">{this.props.value}</Tag>
      );
    } else if (this.props.value === 'in progress') {
      return (
        <Tag color="#108ee9">{this.props.value}</Tag>
      );
    } else {
      return (
        <Tag>{this.props.value}</Tag>
      );
    }
  }
}

export default class Task extends React.Component {

  render() {
    return (
      <Card
        title={this.props.name}
        loading={this.props.loading}
        actions={!this.loading && ([
          <Tooltip title="Status">
            <Status value={this.props.status} />
          </Tooltip>,
          <Tooltip title="Author">
            {this.props.author}
          </Tooltip>,
          <div />,
          <Tooltip title="Price">
            <span style={{ fontSize: 18}}>$ {this.props.price}</span>
          </Tooltip>,
        ])}
        extra={!this.loading && this.props.forUser && (<Button type="primary">Pick Up</Button>)}
        style={{ maxWidth: 750 }}
      >
        <p>{this.props.description}</p>
      </Card>
    );
  }
}