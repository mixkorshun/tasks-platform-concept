import React from 'react';
import { Button } from 'antd';
import TaskList from '../../components/Tasks/TaskList';
import { withRouter } from 'react-router-dom';

class IndexPage extends React.Component {

  clickAddTask = () => {
    this.props.history.push('/add_task/');
  };

  render() {
    return (
      <div>
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
    );
  }
}

export default withRouter(IndexPage);