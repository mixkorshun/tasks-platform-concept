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

  componentDidMount() {
    this.loadTasks();
  };

  loadTasks = async () => {
    this.setState({
      loading: true,
    });

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

        renderItem={item => (
          <List.Item
            key={item.name}
            actions={[
              item.employee_id ? (
                <Button type="primary">Done</Button>
              ) : (
                <Button type="primary">Take</Button>
              ),
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