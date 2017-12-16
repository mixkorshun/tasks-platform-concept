# Tasks platform

[![Build Status](https://travis-ci.org/mixkorshun/tasks-platform-concept.svg?branch=master)](https://travis-ci.org/mixkorshun/tasks-platform-concept)

Simple task tracker platform.

## Features
 - RESTful backend API
 - Environment-based application configuration
 - Support SQLite and MySQL database engines
 - No ORM
 - Authentication using JWT tokens
 - React SPA with ant.design UI kit

## Run application locally

Clone git repository:
```bash
$ git clone git@github.com:mixkorshun/tasks-platform-concept.git .
```

Start application using docker:
```bash
$ docker-compose up
```

Application works at `http://127.0.0.1:9001/`.
You can login to system using 2 sample users:

 - `employee@platform.loc:qwerty` – employee account
 - `employer@platform.loc:qwerty` – employer account
 
## Deployment

**Note:** To run deployment commands you required an `ansible` program.
Read more about ansible: https://www.ansible.com/

### Setup new application server/cluster

Then setup remote server provision:
```bash
$ cd provision
$ ansible-playbook -i inventory/[inventory] setup.yml
```

**Tip:** To apply database migrations use `migrate.yml` ansible-playbook 
after initial release deployment.

### Deploy application

To build application release run following command:
```bash
$ ./build_release.sh provision/release.tar.gz
```

Then deploy newly created release:
```bash
$ cd provision
$ RELEASE=[version] RELEASE_FILE=release.tar.gz ansible-playbook -i inventory/[inventory] deploy.yml
```
