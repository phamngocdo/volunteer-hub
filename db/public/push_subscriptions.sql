create table push_subscriptions
(
    id         serial
        primary key,
    user_id    integer
        constraint fk_user_id
            references users
            on delete cascade,
    endpoint   text not null,
    p256dh     text not null,
    auth       text not null,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

comment on column push_subscriptions.endpoint is 'Web Push subscription endpoint for user';

comment on column push_subscriptions.p256dh is 'Web Push p256dh key';

comment on column push_subscriptions.auth is 'Web Push auth key';

alter table push_subscriptions
    owner to phamngocdo;

create unique index push_subscriptions_user_id_endpoint_idx
    on push_subscriptions (user_id, endpoint);

