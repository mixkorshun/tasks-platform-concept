import React from 'react';
import { Icon, Layout, Menu } from 'antd';

const { Header, Content } = Layout;

const iconStyles = {
  fontSize: 20,
  verticalAlign: 'middle',
  marginRight: 0,
};

export default class AuthorizedLayout extends React.Component {
  handleSelect = (item, k) => {
    if (item.key === 'logout') {
      const callback = this.props.onLogout;

      if (callback) {
        callback();
      }
    }
  };

  render() {
    return (
      <Layout style={{ minHeight: '100%' }}>
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
            theme="dark"
            mode="horizontal"
            style={{ lineHeight: '64px', float: 'right' }}
            onSelect={this.handleSelect}
          >
            <Menu.Item key="logout">
              <Icon type="logout" style={iconStyles} />
            </Menu.Item>
          </Menu>

          <div
            style={{
              float: 'right',
              color: '#fff',
              margin: 0,
              height: '63px',
            }}
          >
            {this.props.user ? this.props.user.email : ''}
          </div>
        </Header>
        <Layout>
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