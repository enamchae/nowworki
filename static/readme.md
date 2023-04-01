Create User Table

    Create TABLE user(
    name TEXT,
    UID TEXT,
    password TEXT not null,
    PRIMARY KEY(UID)
    )

Create Posts

    Create TABLE Post(
    UID TEXT,
    Category TEXT not null,
    text TEXT not null,
    PID int not null,
    FullTime int,
    time int not null,
    PRIMARY KEY (PID),
    FOREIGN KEY (UID) REFERENCES User
    )
Create Post Replies

    Create TABLE PostRep(
        UID TEXT,
        text TEXT not null,
        PID int,
        RID int,
        time int,
        PRIMARY KEY (PID, RID),
        FOREIGN KEY (PID) REFERENCES Post,
        FOREIGN KEY (UID) REFERENCES User
    )