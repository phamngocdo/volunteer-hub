create table event_registrations
(
    registration_id serial
        primary key,
    event_id        integer
        references events,
    user_id         integer
        references users,
    status          varchar(20),
    created_at      timestamp default now(),
    updated_at      timestamp default now()
);

comment on column event_registrations.status is 'pending | approved | rejected | cancelled | completed';

alter table event_registrations
    owner to phamngocdo;

create unique index event_registrations_event_id_user_id_idx
    on event_registrations (event_id, user_id);

