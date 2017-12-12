import React from 'react';
import { Icon, Layout, Menu } from 'antd';

const { Header, Sider, Content } = Layout;

const iconStyles = {
  fontSize: 20,
  verticalAlign: 'middle',
  marginRight: 0,
};

export default class MainLayout extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
    };
  }

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

          <Menu
            theme="dark" mode="horizontal"
            style={{ lineHeight: '64px' }}
          >
            {this.state.user ? (
              <Menu.SubMenu
                theme="light"
                style={{ float: 'right' }}
                title={<span><Icon
                  type="user"
                  style={iconStyles}
                /> {this.state.user.email}</span>}
              >
                <Menu.Item><Icon type="user" />Profile</Menu.Item>
                <Menu.Divider />
                <Menu.Item><Icon type="logout" />Sign out</Menu.Item>

              </Menu.SubMenu>
            ) : (
              <Menu.Item style={{ float: 'right' }}>
                <Icon type="login" style={iconStyles} />
              </Menu.Item>
            )}
          </Menu>
        </Header>
        <Layout>
          <Sider style={{ background: '#fff' }}>
            <Menu
              mode="inline"
              style={{ height: '100%', borderRight: 0 }}
            >
              <Menu.Item key="all">All tasks</Menu.Item>
              {this.state.user && (
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