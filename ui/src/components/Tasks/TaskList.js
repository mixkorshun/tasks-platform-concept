import React from 'react';
import { request } from '../../utils';
import { Button, List, message } from 'antd';

export default class TaskList extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      loading: false,
      tasks: [],
      lastLoaded: 0,
    };
  }

  handleTaskAction = async (item, index) => {
    let resp;
    try {
      resp = await request(
        '/tasks/' + item.id + '/' + this.props.taskAction + '/', {
          method: 'POST',
          headers: {
            'Authorization': this.props.authorization ? 'Token ' + this.props.authorization : '',
          },
        });
    } catch (e) {
      message.error(
        'Server Temporary Unavailable. ' +
        'Please try again in several minutes.',
      );
    }

    let result = await resp.json();

    if (!resp.ok) {
      if (Math.round(resp.status / 100) * 100 === 500) {
        message.error(
          'Server Temporary Unavailable. ' +
          'Please try again in several minutes.',
        );
      } else {
        message.error(result.error_message);
      }
    }

    let tasks = this.state.tasks;
    tasks.splice(index, 1);

    this.setState({
      tasks: tasks,
    });
  };

  componentDidMount() {
    this.reloadTasks();
  };

  reloadTasks = async (useLoading = true) => {
    if (useLoading) {
      this.setState({
        loading: true,
      });
    }

    let resp = null;

    try {
      resp = await request(this.props.feedUrl, {
        method: 'GET',

        headers: {
          'Authorization': this.props.authorization ? 'Token ' + this.props.authorization : '',
        },
      });
    } catch (e) {
      message.error(
        'Server temporary unavailable. Please try again later.',
      );
      return;
    }


    if (Math.round(resp.status / 100) * 100 === 500) {
      message.error('Internal server error occurred.');
      return;
    }

    let data = await resp.json();

    if (resp.ok) {
      this.setState({
        loading: false,
        tasks: data,
        lastLoaded: data.length,
      });
    } else {
      message.error(data.error_message);
    }

  };

  render() {
    return (
      <List
        itemLayout="horizontal"
        dataSource={this.state.tasks}
        loading={this.state.loading}
        loadMore={this.state.lastLoaded === 20 && (
          <div
            style={{
              textAlign: 'center',
              marginTop: 12,
              height: 32,
              lineHeight: '32px',
            }}
          >
            <Button>Load more</Button>
          </div>)
        }

        renderItem={(item, index) => (
          <List.Item
            key={item.name}
            actions={this.props.taskAction && [
              <Button
                type="primary"
                onClick={(e) => this.handleTaskAction(item, index)}
              >{this.props.taskActionLabel}</Button>,
            ]}
          >
            <List.Item.Meta
              title={item.name}
              description={item.description}
            />

            <span>$ {item.price}</span>
          </List.Item>
        )}
      />
    );
  }
}