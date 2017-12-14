import React from 'react';
import AddTaskForm from '../../components/Tasks/AddTaskForm';
import { withRouter } from 'react-router-dom';

class AddTaskPage extends React.Component {

  onAddTask = () => {
    this.props.history.push('/');
  };

  render() {
    return (
      <div>
        <h1>Add task</h1>

        <AddTaskForm
          onTaskAdd={this.onAddTask}
          authorization={this.props.authorization}
        />
      </div>
    );
  }
}

export default withRouter(AddTaskPage);