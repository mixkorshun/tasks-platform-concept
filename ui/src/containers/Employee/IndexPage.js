import React from 'react';
import TaskList from '../../components/Tasks/TaskList';
import { Tabs } from 'antd';

export default class IndexPage extends React.Component {
  setupAssignedRefreshCallback = (cb) => {
    this.assignedRefreshCallback = cb;
  };

  handleAssign = () => {
    this.assignedRefreshCallback && this.assignedRefreshCallback();
  };

  handleDone = () => {
    this.props.onUserChanged && this.props.onUserChanged();
  };

  render() {
    return (
      <Tabs
        defaultActiveKey="unassigned"
        style={{ textAlign: 'center' }}
      >
        <Tabs.TabPane tab="Unassigned" key="unassigned">
          <TaskList
            feedUrl="/tasks/unassigned/"
            forUser={this.props.user}
            authorization={this.props.authorization}
            taskAction="assign"
            taskActionLabel="Assign"
            onTaskAction={this.handleAssign}
          />
        </Tabs.TabPane>
        <Tabs.TabPane tab="In Progress" key="my">
          <TaskList
            feedUrl="/tasks/assigned/"
            forUser={this.props.user}
            authorization={this.props.authorization}
            taskAction="complete"
            taskActionLabel="Done"
            setupRefreshCallback={this.setupAssignedRefreshCallback}
            onTaskAction={this.handleDone}
          />
        </Tabs.TabPane>
      </Tabs>
    );
  }
}
