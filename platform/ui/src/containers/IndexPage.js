import React from 'react';
import MainLayout from './MainLayout';

export default class IndexPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: this.props.user,
    };
  }

  render() {
    return (
      <MainLayout user={this.state.user}>
        Hello world
      </MainLayout>
    );
  }
}