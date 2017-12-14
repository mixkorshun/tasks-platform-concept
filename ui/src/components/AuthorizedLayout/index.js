import React from 'react';
import { Col, Icon, Layout, Menu, Row } from 'antd';

const { Header, Content, Footer } = Layout;

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
            <Row type="flex" justify="center">
              <Col
                span={12} style={{
                minWidth: 600,
                background: '#fff',
                padding: ' 10px 24px 24px',
                margin: 0,
                minHeight: '480px',
              }}
              >
                {this.props.children}
              </Col>
            </Row>
          </Content>
        </Layout>
        <Footer style={{ textAlign: 'center', color: '#aaa', fontSize: 12 }}>
          Tasks Platform. 2017 &copy;
        </Footer>
      </Layout>
    );
  }
}