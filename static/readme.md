Create User Table

    Create TABLE user(
    name varchar(20),
    UID varchar(10),
    password char(32) not null,
    PRIMARY KEY(UID)
    )

Create Posts

    Create TABLE Post(
    UID varchar(10),
    Category varchar(10),
    text TEXT not null,
    PID int not null,
    FullTime bool,
    time time not null,
    title TEXT not null,
    PRIMARY KEY (PID),
    FOREIGN KEY(UID) REFERENCES user(UID))
Create Post Replies

    Create TABLE PostRep(
        UID varchar(10),
        text TEXT not null,
        PID int,
        RID tinyint,
        time time,
        Title text,
        PRIMARY KEY (PID, RID),
        FOREIGN KEY (PID) REFERENCES Post(PID),
        FOREIGN KEY (UID) REFERENCES User(UID)
    )