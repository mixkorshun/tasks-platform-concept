import React from 'react';
import TaskList from '../components/Tasks/TaskList';
import { Col, Row } from 'antd';

export default class IndexPage extends React.Component {
  render() {
    return (
      <Row>
        <Col span={8}>
          <h2>Assigned to me</h2>
          <TaskList
            feedUrl="/tasks/my/"
            forUser={this.props.user}
            authorization={this.props.authorization}
          />
        </Col>

        <Col offset={2} span={12}>
          <h2>Unassigned</h2>
          <TaskList
            feedUrl='/tasks/unassigned/'
            forUser={this.props.user}
            authorization={this.props.authorization}
          />
        </Col>

      </Row>

    );
  }
}