import React from 'react';
import { Icon, Menu } from 'antd';
import { Link } from 'react-router-dom';

const iconStyles = {
  fontSize: 20,
  verticalAlign: 'middle',
  marginRight: 0,
};

export default class UserMenu extends React.Component {
  handleClick = (item, k) => {
    if (item.key === 'logout') {
      const callback = this.props.onLogout;

      if (callback) {
        callback();
      }
    }
  };

  render() {
    return (
      <Menu
        theme="dark"
        mode="horizontal"
        style={{ lineHeight: '64px' }}
        onSelect={this.handleClick}
      >
        {this.props.user ? (
          <Menu.SubMenu
            theme="light"
            style={{ float: 'right' }}
            title={<span><Icon
              type="user" style={iconStyles}
            /> {this.props.user.email}</span>}
          >
            <Menu.Item><Icon type="user" />Profile</Menu.Item>
            <Menu.Divider />
            <Menu.Item key="logout"><Icon type="logout" />Sign
              out</Menu.Item>
          </Menu.SubMenu>
        ) : (
          <Menu.Item style={{ float: 'right' }}>
            <Link to="/login/">
              <Icon type="login" style={iconStyles} />
            </Link>
          </Menu.Item>
        )}
      </Menu>);
  }
}