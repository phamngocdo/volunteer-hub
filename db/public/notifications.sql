create table notifications
(
    notification_id serial
        primary key,
    user_id         integer
        references users,
    event_id        integer
        references events,
    message         text,
    is_read         boolean   default false,
    created_at      timestamp default now(),
    updated_at      timestamp default now()
);

alter table notifications
    owner to phamngocdo;

