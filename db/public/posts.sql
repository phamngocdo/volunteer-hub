create table posts
(
    post_id    serial
        primary key,
    event_id   integer
        references events,
    user_id    integer
        references users,
    images_url varchar(200),
    content    text not null,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

alter table posts
    owner to phamngocdo;

