import React from 'react';
import { Col, Row } from 'antd';
import AddTaskForm from '../../components/Tasks/AddTaskForm';
import { withRouter } from 'react-router-dom';

class AddTaskPage extends React.Component {

  onAddTask = () => {
    this.props.history.push('/');
  };

  render() {
    return (
      <Row>
        <Col  offset={7} span={10}>
          <div style={{ background: '#fff', padding: 24 }}>
            <h1>Add task</h1>

            <AddTaskForm
              onTaskAdd={this.onAddTask}
              authorization={this.props.authorization}
            />
          </div>
        </Col>
      </Row>
    );
  }
}

export default withRouter(AddTaskPage);