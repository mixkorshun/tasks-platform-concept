import React from 'react';
import MainLayout from './MainLayout';
import TaskList from '../components/Tasks/TaskList';

export default class IndexPage extends React.Component {
  render() {
    return (
      <MainLayout {...this.props}>
        <TaskList forUser={this.props.user} authorization={this.props.authorization} />
      </MainLayout>
    );
  }
}