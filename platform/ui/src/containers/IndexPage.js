import React from 'react';
import TaskList from '../components/Tasks/TaskList';

export default class IndexPage extends React.Component {
  render() {
    return (
      <TaskList
        forUser={this.props.user}
        authorization={this.props.authorization}
      />
    );
  }
}