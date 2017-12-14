import React from 'react';
import { request } from '../../utils';
import { Button, List, message } from 'antd';

export default class TaskList extends React.Component {

  constructor(props) {
    super(props);

    this.limit = 15;

    this.state = {
      loading: false,
      tasks: [],
      hasMore: false,
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
    this.handleRefresh();
  };

  loadTasks = async (lastId, limit) => {
    let resp = null;

    try {
      resp = await request(this.props.feedUrl, {
        method: 'GET',
        qs: {
          'last_id': lastId || 0,
          'limit': limit,
        },
        headers: {
          'Authorization': this.props.authorization ? 'Token ' + this.props.authorization : '',
        },
      });
    } catch (e) {
      throw new Error('Server temporary unavailable. Please try again later.');
    }


    if (Math.round(resp.status / 100) * 100 === 500) {
      throw new Error('Internal server error occurred.');
    }

    let data = await resp.json();

    if (resp.ok) {
      return data;
    } else {
      throw new Error(data.error_message);
    }
  };

  handleRefresh = () => {
    this.setState({
      loading: true,
    });

    this.loadTasks(null, this.limit).then((data) => {
      this.setState({
        loading: false,
        hasMore: data.length === this.limit,
        tasks: data,
      });
    }).catch((e) => {
      message.error(e);
    });
  };

  handleLoadMore = () => {
    this.setState({
      loading: true,
    });

    const lastId = this.state.tasks[this.state.tasks.length - 1].id;

    this.loadTasks(lastId, this.limit).then((data) => {
      let tasks = this.state.tasks.concat(data);

      this.setState({
        loading: false,
        hasMore: data.length === this.limit,
        tasks: tasks,
      });
    }).catch((e) => {
      message.error(e);
    });
  };

  render() {
    return (
      <List
        itemLayout="horizontal"
        dataSource={this.state.tasks}
        loading={this.state.loading}
        loadMore={this.state.hasMore && (
          <div
            style={{
              textAlign: 'center',
              marginTop: 12,
              height: 32,
              lineHeight: '32px',
            }}
          >
            <Button onClick={this.handleLoadMore}>Load more</Button>
          </div>)
        }

        style={{
          textAlign: 'left',
        }}

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

            <div style={{ marginLeft: '50px', fontWeight: 600 }}>${item.price}</div>
          </List.Item>
        )}
      />
    );
  }
}