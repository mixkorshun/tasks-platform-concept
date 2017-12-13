import React from 'react';
import MainLayout from './MainLayout';

export default class IndexPage extends React.Component {
  render() {
    return (
      <MainLayout {...this.props}>
        Hello world
      </MainLayout>
    );
  }
}