create table events
(
    event_id    serial
        primary key,
    manager_id  integer
        references users,
    title       varchar(200),
    image_url   varchar(200),
    description text,
    category    varchar(100),
    location    varchar(200),
    start_date  date,
    end_date    date,
    status      varchar(20),
    created_at  timestamp default now(),
    updated_at  timestamp default now()
);

comment on column events.status is 'pending | approved | rejected | completed';

alter table events
    owner to phamngocdo;

