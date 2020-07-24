## Company：

| 列名           | 数据类型     | 约束     | 备注 |
| -------------- | ------------ | -------- | ---- |
| Company_name   | varchar(100) | **主键** |      |
| Address        | Varchar(100) | 非空     |      |
| Phone          | Varchar(30)  | 非空     |      |
| Contact_person | Varchar(20)  | 无       |      |
| Date           | Datetime     | 无       |      |
| State          | int          | 无       |      |
|                |              |          |      |

### 建表:

```mysql
create table company(
company_name varchar(100) primary key,
address varchar(100) not null,
phone varchar(30) not null,
contact_person varchar(20),
date datetime,
state int
);

```

### 插入数据:

```mysql
insert into company values('company of XXX','shanghai,china','010-124542','张先生','2020-07-11 16:05:30',true);
```

## User:

| 列名         | 数据类型     | 约束         | 备注           |
| ------------ | ------------ | ------------ | -------------- |
| name         | Varchar(20)  | 唯一、非空   |                |
| email        | Varchar(30)  | 非空、不重复 | 修改密码用     |
| phone        | Varchar(30)  | 非空         |                |
| is_admin_    | int          | 非空         | 判断是否是管理 |
| state        | int          | 非空         | 账号是否可用   |
| company_name | varchar(100) | 外键         | 来自公司表     |
|              |              |              |                |

`ALTER TABLE our_db.user ADD UNIQUE (email);`

### 创建表:

```mysql
create table user(
    name varchar(20) primary key,
    email varchar(30) not null,
    phone varchar(30) not null,
    is_admin int DEFAULT 0,
    state int DEFAULT 1,
    company_name varchar(100) not null,
    FOREIGN KEY(company_name) REFERENCES company(company_name),
    unique(email)
    );
    
    
```

### 插入数据:

```mysql
insert into user values(
    '张三','XXX@163.com','152******70',true,true,'company of XXX'
);
```

### 尝试删表发现失败:

```mysql
drop table company;
```


> 因为 company表对user表有外键约束



>FOREIGN KEY(company_name) REFERENCES company(company_name)
这一句的意思是外键约束，当前company_name的值来自于company表中的company_name属性。

1. 如果当前表插入 的company_name值，它在user的name属性中没有,则不允许插入。
2. 在当前表没有删除的时候，如果有对company表的删除操作，那么它将会被拒绝。





## user_pwd:

| 列名  | 数据类型    | 约束        | 备注             |
| ----- | ----------- | ----------- | ---------------- |
| email | Varchar(30) | 主键、外键  |                  |
| name  | Varchar(20) | Varchar(20) |                  |
| pwd   | Varchar(32) | 非空        |                  |
| code  | varchar(8)  |             |                  |
| code_ | datetime    |             | 发送验证码的时间 |

### 创建表:



```mysql
create table user_pwd(
    email varchar(30) primary key,
    name varchar(20),
    pwd varchar(32) not null,
    code varchar(8) DEFAULT NULL,
    code_time datetime DEFAULT NULL,
    FOREIGN KEY(name) REFERENCES user(name)
);
```

### 添加数据:

```mysql
insert into user_pwd values(
    '1256031976@qq.com',
    'yejiahao',
    '123456',
    NULL,
    NULL
);

```

### 查询:

当用户输入账号和密码的时候，进行表的查询

```mysql
select pwd_md5 from user_pwd where name = '张三';
```





## obs_log（操作日志）

| 列名      | 数据类型    | 约束 | 备注 |
| --------- | ----------- | ---- | ---- |
| id        | int         | 主键 | 自增 |
| name      | Varchar(20) | 非空 |      |
| oper_time | datetime    | 非空 |      |
| action    | Varchar(20) | 非空 |      |

 

### 创建日志表



```mysql
create table user_log(
id int not null auto_increment,
name varchar(20),
action varchar(100) not null,
oper_time datetime not null,
primary key(id)
);

```

`insert into user_log(name,action,oper_time) values('t','登录成功',now());`



## 文件表

| 列名        | 数据类型     | 约束     | 备注               |
| ----------- | ------------ | -------- | ------------------ |
| File_path   | Varchar(100) | 联合主键 | 文件路径           |
| File_name   | Varchar(50)  |          | 文件名             |
| File_md5    | Varchar(32)  |          | 暂时允许不填       |
| Create_time | datetime     |          | 创建时间           |
| Owner       | Varchar(32)  | 外键     | 所属人，来自用户表 |

```mysql
create table file(
    file_path varchar(100),
    file_name varchar(50),
    file_md5 varchar(32),
    PRIMARY KEY(file_path, file_name)
);
```

