USE hrgsms_db;

-- ============================================
-- FUNCTIONS FOR CALCULATIONS
-- ============================================

-- Function 1: Calculate number of nights
DELIMITER //
CREATE FUNCTION fn_CalculateNights(
    p_checkIn DATETIME,
    p_checkOut DATETIME
)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE nights INT;
    SET nights = DATEDIFF(p_checkOut, p_checkIn);
    
    IF nights < 1 THEN
        SET nights = 1;
    END IF;
    
    RETURN nights;
END//
DELIMITER ;

-- Function 2: Calculate room charges
DELIMITER //
CREATE FUNCTION fn_CalculateRoomCharges(
    p_rate DECIMAL(10,2),
    p_checkIn DATETIME,
    p_checkOut DATETIME
)
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE nights INT;
    DECLARE charges DECIMAL(15,2);
    
    SET nights = fn_CalculateNights(p_checkIn, p_checkOut);
    SET charges = p_rate * nights;
    
    RETURN charges;
END//
DELIMITER ;

-- Function 3: Calculate service charges for a booking
DELIMITER //
CREATE FUNCTION fn_CalculateServiceCharges(
    p_bookingID BIGINT UNSIGNED
)
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE charges DECIMAL(15,2);
    
    SELECT COALESCE(SUM(rate * quantity), 0) INTO charges
    FROM Service_Usage
    WHERE bookingID = p_bookingID;
    
    RETURN charges;
END//
DELIMITER ;

-- Function 4: Calculate total bill
DELIMITER //
CREATE FUNCTION fn_CalculateTotalBill(
    p_bookingID BIGINT UNSIGNED
)
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE roomCharges DECIMAL(15,2);
    DECLARE serviceCharges DECIMAL(15,2);
    DECLARE taxAmount DECIMAL(10,2);
    DECLARE taxRate DECIMAL(5,4);
    DECLARE total DECIMAL(15,2);
    
    -- Get booking details and calculate room charges
    SELECT fn_CalculateRoomCharges(rate, checkInDate, checkOutDate)
    INTO roomCharges
    FROM Booking
    WHERE bookingID = p_bookingID;
    
    -- Calculate service charges
    SET serviceCharges = fn_CalculateServiceCharges(p_bookingID);
    
    -- Get tax rate
    SELECT rate INTO taxRate
    FROM Tax_Policy
    WHERE appliesTo = 'Room'
    LIMIT 1;
    
    IF taxRate IS NULL THEN
        SET taxRate = 0.15;
    END IF;
    
    -- Calculate tax
    SET taxAmount = (roomCharges + serviceCharges) * taxRate;
    
    -- Calculate total
    SET total = roomCharges + serviceCharges + taxAmount;
    
    RETURN total;
END//
DELIMITER ;

-- Function 5: Get occupancy rate for a branch
DELIMITER //
CREATE FUNCTION fn_GetOccupancyRate(
    p_branchID BIGINT UNSIGNED,
    p_date DATE
)
RETURNS DECIMAL(5,2)
READS SQL DATA
BEGIN
    DECLARE totalRooms INT;
    DECLARE occupiedRooms INT;
    DECLARE rate DECIMAL(5,2);
    
    -- Get total rooms
    SELECT COUNT(*) INTO totalRooms
    FROM Room
    WHERE branchID = p_branchID;
    
    -- Get occupied rooms
    SELECT COUNT(DISTINCT r.roomID) INTO occupiedRooms
    FROM Room r
    JOIN Booking b ON r.roomID = b.roomID
    WHERE r.branchID = p_branchID
    AND b.bookingStatus IN ('Booked', 'CheckedIn')
    AND p_date BETWEEN DATE(b.checkInDate) AND DATE(b.checkOutDate);
    
    IF totalRooms = 0 THEN
        RETURN 0;
    END IF;
    
    SET rate = (occupiedRooms / totalRooms) * 100;
    
    RETURN rate;
END//
DELIMITER ;

-- Function 6: Check room availability for dates
DELIMITER //
CREATE FUNCTION fn_IsRoomAvailable(
    p_roomID BIGINT UNSIGNED,
    p_checkIn DATETIME,
    p_checkOut DATETIME
)
RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE conflictCount INT;
    
    SELECT COUNT(*) INTO conflictCount
    FROM Booking
    WHERE roomID = p_roomID
    AND bookingStatus IN ('Booked', 'CheckedIn')
    AND (
        (checkInDate <= p_checkIn AND checkOutDate > p_checkIn)
        OR (checkInDate < p_checkOut AND checkOutDate >= p_checkOut)
        OR (checkInDate >= p_checkIn AND checkOutDate <= p_checkOut)
    );
    
    RETURN (conflictCount = 0);
END//
DELIMITER ;

-- Function 7: Get invoice balance
DELIMITER //
CREATE FUNCTION fn_GetInvoiceBalance(
    p_invoiceID BIGINT UNSIGNED
)
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE balance DECIMAL(15,2);
    
    SELECT (roomCharges + serviceCharges + taxAmount - discountAmount - settledAmount)
    INTO balance
    FROM Invoice
    WHERE invoiceID = p_invoiceID;
    
    RETURN COALESCE(balance, 0);
END//
DELIMITER ;

SELECT 'Functions created successfully!' as Status;
