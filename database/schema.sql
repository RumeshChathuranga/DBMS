USE hrgsms_db;

CREATE TABLE IF NOT EXISTS Branch (
	branchID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  branchLocation VARCHAR(20) NOT NULL,
	rating NUMERIC(2,1),
  phone char(12) NOT NULL,
  email varchar(30) NOT NULL,
  CONSTRAINT chk_phone CHECK(
	phone like '+94%'),
	CONSTRAINT chk_rating CHECK(
	rating >=0 AND rating <= 5)
);

CREATE TABLE IF NOT EXISTS Room_Type (
	typeID	INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	typeName VARCHAR(20) NOT NULL,
	capacity INT NOT NULL,
	currRate NUMERIC(10,2) NOT NULL
);
    
CREATE TABLE IF NOT EXISTS Room (
	roomID BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	branchID BIGINT UNSIGNED NOT NULL,
	typeID	INT UNSIGNED NOT NULL,
	roomNo	INT UNSIGNED NOT NULL,
	roomStatus	ENUM('Occupied', 'Available') NOT NULL,
  CONSTRAINT fk_branchID 
    FOREIGN KEY (branchID) REFERENCES Branch(branchID) 
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_typeID 
    FOREIGN KEY (typeID) REFERENCES Room_Type(typeID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  UNIQUE KEY uq_branch_roomNo (branchID, roomNo), 
  CONSTRAINT chk_roomNo CHECK(roomNo>0)
);

CREATE TABLE IF NOT EXISTS Guest (
  guestID     BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  firstName   VARCHAR(50) NOT NULL,
  lastName    VARCHAR(50) NOT NULL,
  phone       VARCHAR(20) NOT NULL,
  email       VARCHAR(100),
  idNumber    VARCHAR(30) UNIQUE NOT NULL,
  CONSTRAINT chk_phone_guest CHECK(
	phone like '+94%')      
);

CREATE TABLE IF NOT EXISTS Booking (
  bookingID     BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  guestID       BIGINT UNSIGNED NOT NULL,
  branchID      BIGINT UNSIGNED NOT NULL,
  roomID        BIGINT UNSIGNED NOT NULL,
  rate          NUMERIC(10,2) UNSIGNED NOT NULL,
  checkInDate   DATETIME NOT NULL,
  checkOutDate  DATETIME NOT NULL,
  numGuests     INT UNSIGNED NOT NULL,
  bookingStatus ENUM('Booked','CheckedIn','CheckedOut','Cancelled') NOT NULL DEFAULT 'Booked',
  CONSTRAINT fk_guestID 
    FOREIGN KEY (guestID) REFERENCES Guest(guestID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_branchID_booking 
    FOREIGN KEY (branchID) REFERENCES Branch(branchID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_roomID_booking 
    FOREIGN KEY (roomID) REFERENCES Room(roomID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT chk_date CHECK(checkInDate<=checkOutDate)
);

CREATE TABLE IF NOT EXISTS Chargeble_Service (
  serviceID   INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  serviceType ENUM( 'Spa services', 'Pool access', 'room service', 'laundry', 'minibar usage') NOT NULL, 
  unit ENUM('per person','per kg', 'per item', 'per request'), 
  ratePerUnit  DECIMAL(10,2) UNSIGNED NOT NULL
);

CREATE TABLE IF NOT EXISTS Service_Usage ( 
  usageID	BIGINT UNSIGNED PRIMARY KEY NOT NULL,
  bookingID  BIGINT UNSIGNED NOT NULL,
  serviceID  INT UNSIGNED NOT NULL,
  rate  DECIMAL(10,2) UNSIGNED NOT NULL,
  quantity   INT UNSIGNED NOT NULL DEFAULT 1,
  usedAt	TIMESTAMP NOT NULL,
  CONSTRAINT fk_bookingID_service 
    FOREIGN KEY (bookingID) REFERENCES Booking(bookingID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_serviceID 
    FOREIGN KEY (serviceID) REFERENCES Chargeble_Service(serviceID)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Late_Checkout (
	bookingID BIGINT UNSIGNED PRIMARY KEY NOT NULL,
	checkOutTime TIMESTAMP,
	amount NUMERIC(10,2) UNSIGNED,
  CONSTRAINT fk_bookingID_late 
    FOREIGN KEY (bookingID) REFERENCES Booking(bookingID)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Tax_Policy (
  policyID   INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  rate       DECIMAL(5,4) UNSIGNED NOT NULL,       
  appliesTo  VARCHAR(20) NOT NULL,        
  policyName       VARCHAR(100) NOT NULL        
);

CREATE TABLE IF NOT EXISTS Discount (
  discountCode  INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  discountName  VARCHAR(100) NOT NULL,            
  discountCondition     VARCHAR(200),                     
  discountValue   DECIMAL(5,2) UNSIGNED NOT NULL,            
  validFrom     DATE NOT NULL,
  validTo       DATE NOT NULL,
  CONSTRAINT chk_dateValidity CHECK(validTo>validFrom)
);

CREATE TABLE IF NOT EXISTS Invoice (
  invoiceID       BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  bookingID       BIGINT UNSIGNED NOT NULL UNIQUE,
  policyID        INT UNSIGNED NULL,         
  discountCode    INT UNSIGNED NULL,         
  paymentPlan     ENUM('Full','Installment') NOT NULL DEFAULT 'Full',
  roomCharges     DECIMAL(15,2) UNSIGNED NOT NULL DEFAULT 0.00,
  serviceCharges  DECIMAL(15,2) UNSIGNED NOT Null DEFAULT 0.00,
  discountAmount  DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0.00,
  settledAmount   DECIMAL(15,2) UNSIGNED NOT NULL DEFAULT 0.00,   
  invoiceStatus   ENUM('Pending','Partially Paid','Paid','Cancelled') NOT NULL DEFAULT 'Pending',
  CONSTRAINT fk_bookingID_invoice
    FOREIGN KEY (bookingID) REFERENCES Booking(bookingID)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_policyID
    FOREIGN KEY (policyID) REFERENCES Tax_Policy(policyID)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_discountCode 
    FOREIGN KEY (discountCode) REFERENCES Discount(discountCode)
    ON DELETE SET NULL ON UPDATE CASCADE
);

ALTER TABLE Invoice
ADD COLUMN taxAmount DECIMAL(10,2) UNSIGNED NOT NULL DEFAULT 0.00,
ADD CONSTRAINT chk_paidAmount CHECK(settledAmount<=(roomCharges+serviceCharges+taxAmount-discountAmount));

CREATE TABLE IF NOT EXISTS Payment (
  transactionID   BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  invoiceID       BIGINT UNSIGNED NOT NULL,
  transactionDate DATE NOT NULL,
  paymentMethod   ENUM('Cash','Card','Online','Other') NOT NULL,
  amount          DECIMAL(15,2) UNSIGNED NOT NULL,
  CONSTRAINT fk_invoiceID 
    FOREIGN KEY (invoiceID) REFERENCES Invoice(invoiceID)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS User_Account (
  userID      INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  branchID    BIGINT UNSIGNED NULL,
  username    VARCHAR(100) NOT NULL UNIQUE,
  userPassword    VARCHAR(255) NOT NULL,             
  userRole        ENUM('Admin','Manager','Reception','Staff') NOT NULL,
  NIC         VARCHAR(20) UNIQUE,
  first_name  VARCHAR(20) NOT NULL,
  last_name   VARCHAR(20) NOT NULL,
  phone       VARCHAR(15),
  email       VARCHAR(30) UNIQUE,
  CONSTRAINT fk_branchID_user
    FOREIGN KEY (branchID) REFERENCES Branch(branchID)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Log (
  logID        BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_time   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  branchID     BIGINT UNSIGNED NULL,
  userID       INT UNSIGNED NULL,
  bookingID    BIGINT UNSIGNED NULL,
  logAction       ENUM('Create','Update','Delete','CheckIn','CheckOut','Payment','Other') NOT NULL,
  logDescription  VARCHAR(255),
  CONSTRAINT fk_branchID_log 
    FOREIGN KEY (branchID) REFERENCES Branch(branchID)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_userID_log 
    FOREIGN KEY (userID) REFERENCES User_Account(userID)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_bookingID_log 
    FOREIGN KEY (bookingID) REFERENCES Booking(bookingID)
    ON DELETE SET NULL ON UPDATE CASCADE
);