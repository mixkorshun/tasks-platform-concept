import React from 'react';
import TaskList from '../../components/Tasks/TaskList';
import { Col, Row } from 'antd';

export default class IndexPage extends React.Component {
  render() {
    return (
      <Row>

        <Col offset={1} span={10}>
          <h2>Unassigned</h2>
          <div
            style={{
              background: '#fff',
              padding: 24,
              margin: 0,
            }}
          >
            <TaskList
              feedUrl="/tasks/unassigned/"
              autoreload={60000}
              forUser={this.props.user}
              authorization={this.props.authorization}
            />
          </div>
        </Col>

        <Col offset={2} span={10} >
          <h2>Assigned to me</h2>

          <div
            style={{
              background: '#fff',
              padding: 24,
              margin: 0,
            }}
          >
            <TaskList
              feedUrl="/tasks/assigned/"
              autoreload={60000}
              forUser={this.props.user}
              authorization={this.props.authorization}
            />
          </div>

        </Col>


      </Row>

    );
  }
}
