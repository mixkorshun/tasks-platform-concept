import React from 'react';
import { Button, Col, Row } from 'antd';
import TaskList from '../../components/Tasks/TaskList';
import { withRouter } from 'react-router-dom';

class IndexPage extends React.Component {

  clickAddTask = () => {
    this.props.history.push('/add_task/');
  };

  render() {
    return (
      <Row>

        <Col offset={1} span={15}>
          <div style={{ background: '#fff', padding: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <h1>My tasks</h1>
              <Button
                style={{ marginTop: '7px' }}
                icon="plus"
                shape="circle"
                onClick={this.clickAddTask}
              />
            </div>

            <TaskList
              feedUrl="/tasks/authored/"
              authorization={this.props.authorization}
            />
          </div>
        </Col>
      </Row>
    );
  }
}

export default withRouter(IndexPage);