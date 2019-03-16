Use TheBigDatabase;

CREATE TABLE SensorData (
	UserId VARCHAR(100),
	SensorId VARCHAR(100),
	SensorType VARCHAR(100),
	SensorReadings VARCHAR(100),
    TimeStamp VARCHAR(100)
);

CREATE TABLE User (
	UserId VARCHAR(100),
    Parichki FLOAT
);

CREATE TABLE SensorCost (
    SensorType VARCHAR(100),
    UnitCost float
);

INSERT INTO SensorCost 
VALUES('co', 0.0011),
('distance', 0.00001),
('humidity', 0.0002),
('light', 0.0003),
('lpg', 0.0009),
('smoke', 0.0007),
('tempreture', 0.00002);
select * from SensorCost;


CREATE TABLE Transaction (
	UserId VARCHAR(100),
    SensorType VARCHAR(100),
    NumberOfData int
);
select * from Transaction;

INSERT INTO User 
VALUES('Daniela', 2000),
('Dyrvarqt', 2000),
('Georgiasdcvdsa', 2000),
('Pesho', 2000),
('Venci', 2000),
('Vincent', 2000);

select *
from User;

