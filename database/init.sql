-- データベース作成 --
create database bunbetu_db;
use bunbetu_db;
-- デーブル作成 --
create table Manager (
    m_id int primary key,
    hash_pw varchar(128),
    salt varchar(5)
);
create table User (
    u_id int primary key,
    hash_pw varchar(128),
    salt varchar(5)
);
create table Garbagellist (
    GarbageID int primary key,
    GarbageName varchar(100),
    Separation varchar(255),
    Category varchar(255)
);
create table Recycle (
    RecycleID int primary key,
    fk_GarbageName varchar(100),
    fk_Separation varchar(255),
    fk_Category varchar(255),
    RecycleName varchar(100),
    RecycleText varchar(255)
    foreign key (fk_GarbageName,fk_Separation,fk_Category) 
    references Garbagellist(GarbageName,Separation,Category)
);
create table Calendar (
    Calendar int primary key,
    Date varchar(100),
    Event varchar(100),
    fk_u_id int,
    foreign key (fk_u_id) 
    references User(u_id)
);
create table Favorite (
    FavoriteID int auto_increment,
    fk_GarbageID int,
    fk_GarbageName varchar(100),
    fk_Separation varchar(255),
    fk_Category varchar(255),
    fk_u_id int,
    foreign key (fk_GarbageName,fk_Separation,fk_Category) 
    references Garbagellist(GarbageName,Separation,Category),
    foreign key (fk_u_id) 
    references User(u_id)
);