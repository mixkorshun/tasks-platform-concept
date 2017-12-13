import React from 'react';
import { Layout } from 'antd';
import UserMenu from '../components/UserMenu';

const { Header, Content } = Layout;

export default class MainLayout extends React.Component {
  render() {
    return (
      <Layout style={{ height: '100%' }}>
        <Header className="header">
          <h1
            style={{
              float: 'left',
              color: '#fff',
              margin: 0,
              height: '63px',
            }}
          >Tasks Platform</h1>
          <UserMenu user={this.props.user} onLogout={this.props.onLogout} />
        </Header>
        <Layout>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 480,
            }}
          >
            <div style={{ maxWidth: 800, margin: 'auto' }}>
              {this.props.children}
            </div>
          </Content>
        </Layout>
      </Layout>
    );
  }
}