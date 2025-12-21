create table reacts
(
    react_id   integer   default nextval('reacts_like_id_seq'::regclass) not null
        primary key,
    post_id    integer
        references posts,
    user_id    integer
        references users,
    category   varchar(100),
    created_at timestamp default now(),
    updated_at timestamp default now()
);

comment on column reacts.category is 'like | ...';

alter table reacts
    owner to phamngocdo;

create unique index reacts_post_id_user_id_idx
    on reacts (post_id, user_id);

