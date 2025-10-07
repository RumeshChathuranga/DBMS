# 🗃️ Database Documentation - HRGSMS

Comprehensive database documentation for the Hotel Reservation and Guest Services Management System.

## 📋 Overview

The HRGSMS database is designed using MySQL to efficiently handle hotel operations across multiple branches. The database follows normalization principles while optimizing for performance and data integrity.

## 🏗️ Database Architecture

### Design Principles

- **Third Normal Form (3NF)** compliance
- **ACID** transaction properties
- **Referential integrity** with foreign keys
- **Performance optimization** through indexing
- **Data consistency** with triggers and constraints

### Key Features

- Multi-branch support (Colombo, Kandy, Galle)
- Room inventory management
- Guest relationship management
- Reservation and billing system
- Service request handling
- Comprehensive reporting capabilities

## 📋 Database Schema

### Core Tables

#### Branch

Stores hotel branch information for multi-location management.

```sql
CREATE TABLE Branch (
    branchID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    branchLocation VARCHAR(20) NOT NULL,
    rating NUMERIC(2,1),
    phone CHAR(12) NOT NULL,
    email VARCHAR(30) NOT NULL,
    CONSTRAINT chk_phone CHECK(phone LIKE '+94%'),
    CONSTRAINT chk_rating CHECK(rating >= 0 AND rating <= 5)
);
```

**Columns:**

- `branchID`: Unique identifier for each branch
- `branchLocation`: Location name (Colombo, Kandy, Galle)
- `rating`: Branch rating (0-5 scale)
- `phone`: Contact phone number (Sri Lankan format)
- `email`: Branch email address

#### Room_Type

Defines different room categories and their specifications.

```sql
CREATE TABLE Room_Type (
    typeID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    typeName VARCHAR(20) NOT NULL,
    capacity INT NOT NULL,
    currRate NUMERIC(10,2) NOT NULL
);
```

**Columns:**

- `typeID`: Unique room type identifier
- `typeName`: Room type name (Single, Double, Suite, etc.)
- `capacity`: Maximum occupancy
- `currRate`: Current room rate per night

#### Room

Individual room records with branch and type associations.

```sql
CREATE TABLE Room (
    roomID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    branchID BIGINT UNSIGNED NOT NULL,
    typeID INT UNSIGNED NOT NULL,
    roomNo INT UNSIGNED NOT NULL,
    roomStatus ENUM('Occupied', 'Available') NOT NULL,
    FOREIGN KEY (branchID) REFERENCES Branch(branchID),
    FOREIGN KEY (typeID) REFERENCES Room_Type(typeID)
);
```

**Columns:**

- `roomID`: Unique room identifier
- `branchID`: Reference to branch
- `typeID`: Reference to room type
- `roomNo`: Room number within branch
- `roomStatus`: Current availability status

#### Guest

Guest profile and contact information.

```sql
CREATE TABLE Guest (
    guestID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone CHAR(12) NOT NULL,
    nic VARCHAR(15) UNIQUE NOT NULL,
    dateOfBirth DATE,
    nationality VARCHAR(30)
);
```

**Columns:**

- `guestID`: Unique guest identifier
- `firstName/lastName`: Guest name
- `email`: Contact email (unique)
- `phone`: Contact phone number
- `nic`: National ID/Passport (unique)
- `dateOfBirth`: Date of birth
- `nationality`: Guest nationality

#### Reservation

Booking records and reservation details.

```sql
CREATE TABLE Reservation (
    resID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    guestID BIGINT UNSIGNED NOT NULL,
    roomID BIGINT UNSIGNED NOT NULL,
    checkinDate DATE NOT NULL,
    checkoutDate DATE NOT NULL,
    totalAmount NUMERIC(10,2) NOT NULL,
    resStatus ENUM('Confirmed', 'Cancelled', 'Completed') NOT NULL,
    resDateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guestID) REFERENCES Guest(guestID),
    FOREIGN KEY (roomID) REFERENCES Room(roomID)
);
```

### Operational Tables

#### Check_In / Check_Out

Track guest check-in and check-out processes.

```sql
CREATE TABLE Check_In (
    checkinID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    resID BIGINT UNSIGNED NOT NULL,
    checkinTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    checkinBy VARCHAR(50) NOT NULL,
    FOREIGN KEY (resID) REFERENCES Reservation(resID)
);

CREATE TABLE Check_Out (
    checkoutID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    resID BIGINT UNSIGNED NOT NULL,
    checkoutTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    checkoutBy VARCHAR(50) NOT NULL,
    FOREIGN KEY (resID) REFERENCES Reservation(resID)
);
```

#### Additional_Service

Hotel services available to guests.

```sql
CREATE TABLE Additional_Service (
    serviceID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    serviceName VARCHAR(50) NOT NULL,
    serviceDesc TEXT,
    serviceRate NUMERIC(8,2) NOT NULL,
    serviceCategory VARCHAR(30)
);
```

#### Service_Request

Guest requests for additional services.

```sql
CREATE TABLE Service_Request (
    requestID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    guestID BIGINT UNSIGNED NOT NULL,
    serviceID INT UNSIGNED NOT NULL,
    quantity INT DEFAULT 1,
    requestTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    totalCost NUMERIC(10,2),
    FOREIGN KEY (guestID) REFERENCES Guest(guestID),
    FOREIGN KEY (serviceID) REFERENCES Additional_Service(serviceID)
);
```

### Financial Tables

#### Bill

Billing information for reservations.

```sql
CREATE TABLE Bill (
    billID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    resID BIGINT UNSIGNED NOT NULL,
    roomCharges NUMERIC(10,2) NOT NULL,
    serviceCharges NUMERIC(10,2) DEFAULT 0,
    taxes NUMERIC(10,2) DEFAULT 0,
    totalAmount NUMERIC(10,2) NOT NULL,
    billDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resID) REFERENCES Reservation(resID)
);
```

#### Payment

Payment records and transaction details.

```sql
CREATE TABLE Payment (
    paymentID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    billID BIGINT UNSIGNED NOT NULL,
    paymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'Bank Transfer') NOT NULL,
    amountPaid NUMERIC(10,2) NOT NULL,
    paymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    transactionRef VARCHAR(50),
    FOREIGN KEY (billID) REFERENCES Bill(billID)
);
```

### System Tables

#### User / User_Role

System access control and user management.

```sql
CREATE TABLE User_Role (
    roleID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    roleName VARCHAR(30) NOT NULL,
    roleDesc TEXT
);

CREATE TABLE User (
    userID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    roleID INT UNSIGNED NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (roleID) REFERENCES User_Role(roleID)
);
```

## 🔧 Database Triggers

### Room Status Updates

Automatically update room status based on reservations.

```sql
DELIMITER $$
CREATE TRIGGER update_room_status_checkin
AFTER INSERT ON Check_In
FOR EACH ROW
BEGIN
    UPDATE Room r
    JOIN Reservation res ON r.roomID = res.roomID
    SET r.roomStatus = 'Occupied'
    WHERE res.resID = NEW.resID;
END$$
DELIMITER ;
```

### Billing Calculations

Automatically calculate bill amounts when services are added.

```sql
DELIMITER $$
CREATE TRIGGER calculate_service_charges
AFTER INSERT ON Service_Request
FOR EACH ROW
BEGIN
    DECLARE service_rate NUMERIC(8,2);

    SELECT serviceRate INTO service_rate
    FROM Additional_Service
    WHERE serviceID = NEW.serviceID;

    UPDATE Service_Request
    SET totalCost = service_rate * NEW.quantity
    WHERE requestID = NEW.requestID;
END$$
DELIMITER ;
```

## 🚀 Stored Procedures

### Check Room Availability

```sql
DELIMITER $$
CREATE PROCEDURE CheckRoomAvailability(
    IN p_checkin_date DATE,
    IN p_checkout_date DATE,
    IN p_branch_id BIGINT UNSIGNED
)
BEGIN
    SELECT r.roomID, r.roomNo, rt.typeName, rt.currRate
    FROM Room r
    JOIN Room_Type rt ON r.typeID = rt.typeID
    WHERE r.branchID = p_branch_id
    AND r.roomID NOT IN (
        SELECT res.roomID
        FROM Reservation res
        WHERE res.resStatus = 'Confirmed'
        AND (
            (p_checkin_date BETWEEN res.checkinDate AND res.checkoutDate)
            OR (p_checkout_date BETWEEN res.checkinDate AND res.checkoutDate)
            OR (res.checkinDate BETWEEN p_checkin_date AND p_checkout_date)
        )
    );
END$$
DELIMITER ;
```

### Generate Revenue Report

```sql
DELIMITER $$
CREATE PROCEDURE GenerateRevenueReport(
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_branch_id BIGINT UNSIGNED
)
BEGIN
    SELECT
        b.branchLocation,
        COUNT(r.resID) as total_reservations,
        SUM(bill.totalAmount) as total_revenue,
        AVG(bill.totalAmount) as avg_bill_amount
    FROM Branch b
    LEFT JOIN Room room ON b.branchID = room.branchID
    LEFT JOIN Reservation r ON room.roomID = r.roomID
    LEFT JOIN Bill bill ON r.resID = bill.resID
    WHERE (p_branch_id IS NULL OR b.branchID = p_branch_id)
    AND bill.billDate BETWEEN p_start_date AND p_end_date
    GROUP BY b.branchID, b.branchLocation;
END$$
DELIMITER ;
```

## 📈 Database Indexes

### Performance Optimization Indexes

```sql
-- Reservation queries
CREATE INDEX idx_reservation_dates ON Reservation(checkinDate, checkoutDate);
CREATE INDEX idx_reservation_status ON Reservation(resStatus);
CREATE INDEX idx_reservation_guest ON Reservation(guestID);

-- Room searches
CREATE INDEX idx_room_branch_type ON Room(branchID, typeID);
CREATE INDEX idx_room_status ON Room(roomStatus);

-- Guest lookups
CREATE INDEX idx_guest_email ON Guest(email);
CREATE INDEX idx_guest_phone ON Guest(phone);

-- Billing queries
CREATE INDEX idx_bill_date ON Bill(billDate);
CREATE INDEX idx_payment_method ON Payment(paymentMethod);

-- Service requests
CREATE INDEX idx_service_request_guest ON Service_Request(guestID);
CREATE INDEX idx_service_request_status ON Service_Request(status);
```

## 🔒 Data Constraints

### Business Rules Enforcement

```sql
-- Room rates must be positive
ALTER TABLE Room_Type ADD CONSTRAINT chk_positive_rate
CHECK (currRate > 0);

-- Check-out date must be after check-in date
ALTER TABLE Reservation ADD CONSTRAINT chk_valid_dates
CHECK (checkoutDate > checkinDate);

-- Service quantity must be positive
ALTER TABLE Service_Request ADD CONSTRAINT chk_positive_quantity
CHECK (quantity > 0);

-- Payment amount must be positive
ALTER TABLE Payment ADD CONSTRAINT chk_positive_payment
CHECK (amountPaid > 0);
```

## 🧪 Sample Data

### Branches

```sql
INSERT INTO Branch (branchLocation, rating, phone, email) VALUES
('Colombo', 4.5, '+94112345678', 'colombo@skynest.lk'),
('Kandy', 4.3, '+94812345678', 'kandy@skynest.lk'),
('Galle', 4.7, '+94912345678', 'galle@skynest.lk');
```

### Room Types

```sql
INSERT INTO Room_Type (typeName, capacity, currRate) VALUES
('Single', 1, 100.00),
('Double', 2, 150.00),
('Triple', 3, 200.00),
('Suite', 4, 300.00),
('Deluxe Suite', 6, 500.00);
```

### Services

```sql
INSERT INTO Additional_Service (serviceName, serviceDesc, serviceRate, serviceCategory) VALUES
('Room Service', 'In-room dining service', 25.00, 'Dining'),
('Laundry', 'Laundry and dry cleaning', 15.00, 'Housekeeping'),
('Spa Treatment', 'Relaxing spa services', 75.00, 'Wellness'),
('Airport Transfer', 'Transportation to/from airport', 50.00, 'Transportation');
```

## 🔧 Database Maintenance

### Backup Procedures

```bash
# Daily backup
mysqldump -u root -p hrgsms_db > backup_$(date +%Y%m%d).sql

# Compressed backup
mysqldump -u root -p hrgsms_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore from backup
mysql -u root -p hrgsms_db < backup_20241001.sql
```

### Optimization Queries

```sql
-- Analyze table statistics
ANALYZE TABLE Reservation, Room, Guest, Bill;

-- Optimize tables
OPTIMIZE TABLE Reservation, Room, Guest, Bill;

-- Check table integrity
CHECK TABLE Reservation, Room, Guest, Bill;
```

## 📊 Performance Monitoring

### Key Metrics

- Query execution time
- Index usage statistics
- Table size growth
- Connection pool utilization
- Slow query log analysis

### Monitoring Queries

```sql
-- Check table sizes
SELECT
    TABLE_NAME,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'hrgsms_db'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- Index usage statistics
SELECT
    OBJECT_NAME,
    INDEX_NAME,
    CARDINALITY
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'hrgsms_db'
ORDER BY CARDINALITY DESC;
```

---

**Robust database design for efficient hotel operations** 📊
