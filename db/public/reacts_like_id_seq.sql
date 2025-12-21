create sequence reacts_like_id_seq
    as integer;

alter sequence reacts_like_id_seq owner to phamngocdo;

alter sequence reacts_like_id_seq owned by reacts.react_id;

