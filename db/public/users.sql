create table users
(
    user_id      serial
        primary key,
    first_name   varchar(100),
    last_name    varchar(100),
    email        varchar(100) not null
        unique,
    password     text         not null,
    phone_number varchar(100),
    role         varchar(20),
    status       varchar(20),
    created_at   timestamp default now(),
    updated_at   timestamp default now(),
    avatar_url   varchar(200)
);

comment on column users.role is 'volunteer | manager | admin';

comment on column users.status is 'active | banned | pending';

alter table users
    owner to phamngocdo;

