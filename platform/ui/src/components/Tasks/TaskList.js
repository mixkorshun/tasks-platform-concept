import React from 'react';
import { request } from '../../utils';
import { message } from 'antd';
import Task from './Task';

export default class TaskList extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      loading: false,
      tasks: [],
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
      });
    } else {
      message.error(data.error_message);
    }

  };

  renderTasks() {
    let tasks = [];

    this.state.tasks.forEach((item) => {
      tasks.push(
        <Task
          name={item.name}
          price={item.price}
          description={item.description}
          status={item.status}

          forUser={this.props.forUser}
        />,
      );

    });

    return tasks;
  }

  render() {
    return (
      <div>
        {
          this.state.loading ?

            <Task loading /> :

            this.renderTasks()
        }
      </div>
    );
  }
}