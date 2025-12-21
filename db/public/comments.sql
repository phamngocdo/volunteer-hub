create table comments
(
    comment_id serial
        primary key,
    post_id    integer
        references posts,
    user_id    integer
        references users,
    content    text not null,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

alter table comments
    owner to phamngocdo;

