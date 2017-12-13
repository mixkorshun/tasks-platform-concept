import React from 'react';
import { Layout, Menu } from 'antd';
import UserMenu from '../components/UserMenu';

const { Header, Sider, Content } = Layout;

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
          <Sider style={{ background: '#fff' }}>
            <Menu
              mode="inline"
              style={{ height: '100%', borderRight: 0 }}
            >
              <Menu.Item key="all">All tasks</Menu.Item>
              {this.props.user && (
                <Menu.Item key="my">My tasks</Menu.Item>
              )}
            </Menu>
          </Sider>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 480,
            }}
          >
            {this.props.children}
          </Content>
        </Layout>
      </Layout>
    );
  }
}