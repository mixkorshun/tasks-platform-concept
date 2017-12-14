import React from 'react';
import TaskList from '../../components/Tasks/TaskList';
import { Tabs } from 'antd';

export default class IndexPage extends React.Component {

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
          />
        </Tabs.TabPane>
        <Tabs.TabPane tab="My tasks" key="my">
          <TaskList
            feedUrl="/tasks/assigned/"
            autoreload={60000}
            forUser={this.props.user}
            authorization={this.props.authorization}
            taskAction="complete"
            taskActionLabel="Done"
          />
        </Tabs.TabPane>
      </Tabs>
    );
  }
}
