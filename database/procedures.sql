USE hrgsms_db;

-- ============================================
-- STORED PROCEDURES
-- ============================================

-- Procedure 1: Complete Check-In Process
DELIMITER //
CREATE PROCEDURE sp_CheckInGuest(
    IN p_bookingID BIGINT UNSIGNED
)
BEGIN
    DECLARE v_roomID BIGINT UNSIGNED;
    DECLARE v_current_status VARCHAR(20);
    
    -- Start transaction
    START TRANSACTION;
    
    -- Get booking details
    SELECT roomID, bookingStatus INTO v_roomID, v_current_status
    FROM Booking
    WHERE bookingID = p_bookingID;
    
    -- Validate booking status
    IF v_current_status != 'Booked' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Booking must be in Booked status to check in';
    END IF;
    
    -- Update booking status
    UPDATE Booking
    SET bookingStatus = 'CheckedIn'
    WHERE bookingID = p_bookingID;
    
    -- Update room status (trigger will handle this, but explicit for clarity)
    UPDATE Room
    SET roomStatus = 'Occupied'
    WHERE roomID = v_roomID;
    
    COMMIT;
    
    SELECT 'Check-in successful' as Message;
END//
DELIMITER ;

-- Procedure 2: Complete Check-Out Process with Invoice Generation
DELIMITER //
CREATE PROCEDURE sp_CheckOutGuest(
    IN p_bookingID BIGINT UNSIGNED,
    OUT p_invoiceID BIGINT UNSIGNED,
    OUT p_totalAmount DECIMAL(15,2)
)
BEGIN
    DECLARE v_roomID BIGINT UNSIGNED;
    DECLARE v_branchID BIGINT UNSIGNED;
    DECLARE v_rate DECIMAL(10,2);
    DECLARE v_checkIn DATETIME;
    DECLARE v_checkOut DATETIME;
    DECLARE v_nights INT;
    DECLARE v_roomCharges DECIMAL(15,2);
    DECLARE v_serviceCharges DECIMAL(15,2);
    DECLARE v_taxAmount DECIMAL(10,2);
    DECLARE v_taxRate DECIMAL(5,4);
    DECLARE v_current_status VARCHAR(20);
    DECLARE v_invoice_exists INT;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Get booking details
    SELECT roomID, branchID, rate, checkInDate, checkOutDate, bookingStatus
    INTO v_roomID, v_branchID, v_rate, v_checkIn, v_checkOut, v_current_status
    FROM Booking
    WHERE bookingID = p_bookingID;
    
    -- Validate booking status
    IF v_current_status NOT IN ('CheckedIn', 'Booked') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid booking status for checkout';
    END IF;
    
    -- Calculate nights
    SET v_nights = DATEDIFF(v_checkOut, v_checkIn);
    IF v_nights < 1 THEN
        SET v_nights = 1;
    END IF;
    
    -- Calculate room charges
    SET v_roomCharges = v_rate * v_nights;
    
    -- Calculate service charges
    SELECT COALESCE(SUM(rate * quantity), 0) INTO v_serviceCharges
    FROM Service_Usage
    WHERE bookingID = p_bookingID;
    
    -- Get tax rate
    SELECT rate INTO v_taxRate
    FROM Tax_Policy
    WHERE appliesTo = 'Room'
    LIMIT 1;
    
    IF v_taxRate IS NULL THEN
        SET v_taxRate = 0.15; -- Default 15%
    END IF;
    
    -- Calculate tax
    SET v_taxAmount = (v_roomCharges + v_serviceCharges) * v_taxRate;
    
    -- Check if invoice exists
    SELECT COUNT(*) INTO v_invoice_exists
    FROM Invoice
    WHERE bookingID = p_bookingID;
    
    -- Create or update invoice
    IF v_invoice_exists = 0 THEN
        INSERT INTO Invoice (
            bookingID, policyID, paymentPlan,
            roomCharges, serviceCharges, taxAmount,
            discountAmount, settledAmount, invoiceStatus
        )
        SELECT 
            p_bookingID,
            (SELECT policyID FROM Tax_Policy WHERE appliesTo = 'Room' LIMIT 1),
            'Full',
            v_roomCharges,
            v_serviceCharges,
            v_taxAmount,
            0.00,
            0.00,
            'Pending';
        
        SET p_invoiceID = LAST_INSERT_ID();
    ELSE
        SELECT invoiceID INTO p_invoiceID
        FROM Invoice
        WHERE bookingID = p_bookingID;
    END IF;
    
    -- Update booking status
    UPDATE Booking
    SET bookingStatus = 'CheckedOut'
    WHERE bookingID = p_bookingID;
    
    -- Update room status (trigger will handle this)
    UPDATE Room
    SET roomStatus = 'Available'
    WHERE roomID = v_roomID;
    
    -- Calculate total amount
    SET p_totalAmount = v_roomCharges + v_serviceCharges + v_taxAmount;
    
    COMMIT;
END//
DELIMITER ;

-- Procedure 3: Process Payment
DELIMITER //
CREATE PROCEDURE sp_ProcessPayment(
    IN p_invoiceID BIGINT UNSIGNED,
    IN p_paymentMethod VARCHAR(20),
    IN p_amount DECIMAL(15,2)
)
BEGIN
    DECLARE v_balance DECIMAL(15,2);
    DECLARE v_totalAmount DECIMAL(15,2);
    DECLARE v_settledAmount DECIMAL(15,2);
    
    START TRANSACTION;
    
    -- Get invoice details
    SELECT 
        (roomCharges + serviceCharges + taxAmount - discountAmount) as total,
        settledAmount
    INTO v_totalAmount, v_settledAmount
    FROM Invoice
    WHERE invoiceID = p_invoiceID;
    
    -- Calculate balance
    SET v_balance = v_totalAmount - v_settledAmount;
    
    -- Validate payment amount
    IF p_amount > v_balance THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment amount exceeds balance due';
    END IF;
    
    IF p_amount <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Payment amount must be positive';
    END IF;
    
    -- Insert payment record
    INSERT INTO Payment (invoiceID, transactionDate, paymentMethod, amount)
    VALUES (p_invoiceID, CURDATE(), p_paymentMethod, p_amount);
    
    COMMIT;
    
    SELECT 'Payment processed successfully' as Message,
           (v_totalAmount - v_settledAmount - p_amount) as RemainingBalance;
END//
DELIMITER ;

-- Procedure 4: Add Service to Booking
DELIMITER //
CREATE PROCEDURE sp_AddServiceToBooking(
    IN p_bookingID BIGINT UNSIGNED,
    IN p_serviceID INT UNSIGNED,
    IN p_quantity INT UNSIGNED
)
BEGIN
    DECLARE v_serviceRate DECIMAL(10,2);
    DECLARE v_usageID BIGINT UNSIGNED;
    DECLARE v_bookingStatus VARCHAR(20);
    
    START TRANSACTION;
    
    -- Check booking status
    SELECT bookingStatus INTO v_bookingStatus
    FROM Booking
    WHERE bookingID = p_bookingID;
    
    IF v_bookingStatus NOT IN ('Booked', 'CheckedIn') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Can only add services to active bookings';
    END IF;
    
    -- Get service rate
    SELECT ratePerUnit INTO v_serviceRate
    FROM Chargeble_Service
    WHERE serviceID = p_serviceID;
    
    -- Generate unique usage ID
    SET v_usageID = UNIX_TIMESTAMP() * 1000;
    
    -- Insert service usage
    INSERT INTO Service_Usage (usageID, bookingID, serviceID, rate, quantity, usedAt)
    VALUES (v_usageID, p_bookingID, p_serviceID, v_serviceRate, p_quantity, NOW());
    
    COMMIT;
    
    SELECT 'Service added successfully' as Message,
           v_usageID as UsageID,
           (v_serviceRate * p_quantity) as TotalCharge;
END//
DELIMITER ;

-- Procedure 5: Get Room Availability
DELIMITER //
CREATE PROCEDURE sp_GetAvailableRooms(
    IN p_branchID BIGINT UNSIGNED,
    IN p_typeID INT UNSIGNED,
    IN p_checkIn DATETIME,
    IN p_checkOut DATETIME
)
BEGIN
    SELECT r.roomID, r.roomNo, r.roomStatus,
           rt.typeName, rt.capacity, rt.currRate
    FROM Room r
    JOIN Room_Type rt ON r.typeID = rt.typeID
    WHERE r.branchID = p_branchID 
    AND r.typeID = p_typeID 
    AND r.roomStatus = 'Available'
    AND r.roomID NOT IN (
        SELECT roomID 
        FROM Booking 
        WHERE branchID = p_branchID
        AND bookingStatus IN ('Booked', 'CheckedIn')
        AND (
            (checkInDate <= p_checkOut AND checkOutDate > p_checkIn)
            OR (checkInDate < p_checkOut AND checkOutDate >= p_checkIn)
            OR (checkInDate >= p_checkIn AND checkOutDate <= p_checkOut)
        )
    )
    ORDER BY r.roomNo;
END//
DELIMITER ;

-- Procedure 6: Cancel Booking
DELIMITER //
CREATE PROCEDURE sp_CancelBooking(
    IN p_bookingID BIGINT UNSIGNED
)
BEGIN
    DECLARE v_status VARCHAR(20);
    
    START TRANSACTION;
    
    SELECT bookingStatus INTO v_status
    FROM Booking
    WHERE bookingID = p_bookingID;
    
    IF v_status = 'CheckedOut' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot cancel a checked-out booking';
    END IF;
    
    IF v_status = 'Cancelled' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Booking is already cancelled';
    END IF;
    
    UPDATE Booking
    SET bookingStatus = 'Cancelled'
    WHERE bookingID = p_bookingID;
    
    COMMIT;
    
    SELECT 'Booking cancelled successfully' as Message;
END//
DELIMITER ;

SELECT 'Stored Procedures created successfully!' as Status;
