USE hrgsms_db;

-- ============================================
-- TRIGGERS FOR ACID COMPLIANCE
-- ============================================

-- Trigger 1: Auto-update room status on check-in
DELIMITER //
CREATE TRIGGER trg_booking_checkin
AFTER UPDATE ON Booking
FOR EACH ROW
BEGIN
    IF NEW.bookingStatus = 'CheckedIn' AND OLD.bookingStatus = 'Booked' THEN
        UPDATE Room 
        SET roomStatus = 'Occupied' 
        WHERE roomID = NEW.roomID;
        
        -- Log the check-in
        INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
        VALUES (NEW.branchID, NULL, NEW.bookingID, 'CheckIn', 
                CONCAT('Guest checked in to room ', NEW.roomID));
    END IF;
END//
DELIMITER ;

-- Trigger 2: Auto-update room status on check-out
DELIMITER //
CREATE TRIGGER trg_booking_checkout
AFTER UPDATE ON Booking
FOR EACH ROW
BEGIN
    IF NEW.bookingStatus = 'CheckedOut' AND OLD.bookingStatus = 'CheckedIn' THEN
        UPDATE Room 
        SET roomStatus = 'Available' 
        WHERE roomID = NEW.roomID;
        
        -- Log the check-out
        INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
        VALUES (NEW.branchID, NULL, NEW.bookingID, 'CheckOut', 
                CONCAT('Guest checked out from room ', NEW.roomID));
    END IF;
END//
DELIMITER ;

-- Trigger 3: Auto-update room status on booking cancellation
DELIMITER //
CREATE TRIGGER trg_booking_cancel
AFTER UPDATE ON Booking
FOR EACH ROW
BEGIN
    IF NEW.bookingStatus = 'Cancelled' AND OLD.bookingStatus IN ('Booked', 'CheckedIn') THEN
        UPDATE Room 
        SET roomStatus = 'Available' 
        WHERE roomID = NEW.roomID;
        
        -- Log the cancellation
        INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
        VALUES (NEW.branchID, NULL, NEW.bookingID, 'Update', 
                CONCAT('Booking cancelled for room ', NEW.roomID));
    END IF;
END//
DELIMITER ;

-- Trigger 4: Prevent double booking
DELIMITER //
CREATE TRIGGER trg_prevent_double_booking
BEFORE INSERT ON Booking
FOR EACH ROW
BEGIN
    DECLARE booking_count INT;
    
    -- Check for overlapping bookings
    SELECT COUNT(*) INTO booking_count
    FROM Booking
    WHERE roomID = NEW.roomID
    AND bookingStatus IN ('Booked', 'CheckedIn')
    AND (
        (checkInDate <= NEW.checkInDate AND checkOutDate > NEW.checkInDate)
        OR (checkInDate < NEW.checkOutDate AND checkOutDate >= NEW.checkOutDate)
        OR (checkInDate >= NEW.checkInDate AND checkOutDate <= NEW.checkOutDate)
    );
    
    IF booking_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Room is already booked for overlapping dates';
    END IF;
END//
DELIMITER ;

-- Trigger 5: Log booking creation
DELIMITER //
CREATE TRIGGER trg_log_booking_creation
AFTER INSERT ON Booking
FOR EACH ROW
BEGIN
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    VALUES (NEW.branchID, NULL, NEW.bookingID, 'Create', 
            CONCAT('New booking created for room ', NEW.roomID));
END//
DELIMITER ;

-- Trigger 6: Update invoice status after payment
DELIMITER //
CREATE TRIGGER trg_update_invoice_after_payment
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
    DECLARE total_amount DECIMAL(15,2);
    DECLARE new_settled DECIMAL(15,2);
    DECLARE new_status VARCHAR(20);
    
    -- Get invoice total and current settled amount
    SELECT (roomCharges + serviceCharges + taxAmount - discountAmount), 
           settledAmount
    INTO total_amount, new_settled
    FROM Invoice
    WHERE invoiceID = NEW.invoiceID;
    
    -- Add new payment to settled amount
    SET new_settled = new_settled + NEW.amount;
    
    -- Determine new status
    IF new_settled >= total_amount THEN
        SET new_status = 'Paid';
    ELSEIF new_settled > 0 THEN
        SET new_status = 'Partially Paid';
    ELSE
        SET new_status = 'Pending';
    END IF;
    
    -- Update invoice
    UPDATE Invoice
    SET settledAmount = new_settled,
        invoiceStatus = new_status
    WHERE invoiceID = NEW.invoiceID;
    
    -- Log payment
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, i.bookingID, 'Payment',
           CONCAT('Payment of ', NEW.amount, ' received')
    FROM Invoice i
    JOIN Booking b ON i.bookingID = b.bookingID
    WHERE i.invoiceID = NEW.invoiceID;
END//
DELIMITER ;

-- Trigger 7: Validate check-out date
DELIMITER //
CREATE TRIGGER trg_validate_booking_dates
BEFORE INSERT ON Booking
FOR EACH ROW
BEGIN
    IF NEW.checkOutDate <= NEW.checkInDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-out date must be after check-in date';
    END IF;
    
    IF NEW.checkInDate < NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Check-in date cannot be in the past';
    END IF;
END//
DELIMITER ;

-- Trigger 8: Auto-calculate nights in booking
DELIMITER //
CREATE TRIGGER trg_calculate_booking_rate
BEFORE INSERT ON Booking
FOR EACH ROW
BEGIN
    DECLARE room_rate DECIMAL(10,2);
    
    -- Get current room rate
    SELECT rt.currRate INTO room_rate
    FROM Room r
    JOIN Room_Type rt ON r.typeID = rt.typeID
    WHERE r.roomID = NEW.roomID;
    
    -- Set the rate (snapshot at booking time)
    SET NEW.rate = room_rate;
END//
DELIMITER ;

-- Trigger 9: Update invoice service charges when service is added
DELIMITER //
CREATE TRIGGER trg_update_service_charges_insert
AFTER INSERT ON Service_Usage
FOR EACH ROW
BEGIN
    DECLARE service_cost DECIMAL(15,2);
    
    -- Calculate the cost for this service
    SET service_cost = NEW.rate * NEW.quantity;
    
    -- Update the invoice service charges
    UPDATE Invoice
    SET serviceCharges = serviceCharges + service_cost
    WHERE bookingID = NEW.bookingID;
    
    -- Log the service addition
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, NEW.bookingID, 'Update',
           CONCAT('Service charge added: ', service_cost)
    FROM Booking b
    WHERE b.bookingID = NEW.bookingID;
END//
DELIMITER ;

-- Trigger 10: Update invoice service charges when service is updated
DELIMITER //
CREATE TRIGGER trg_update_service_charges_update
AFTER UPDATE ON Service_Usage
FOR EACH ROW
BEGIN
    DECLARE old_cost DECIMAL(15,2);
    DECLARE new_cost DECIMAL(15,2);
    DECLARE cost_difference DECIMAL(15,2);
    
    -- Calculate old and new costs
    SET old_cost = OLD.rate * OLD.quantity;
    SET new_cost = NEW.rate * NEW.quantity;
    SET cost_difference = new_cost - old_cost;
    
    -- Update the invoice service charges
    UPDATE Invoice
    SET serviceCharges = serviceCharges + cost_difference
    WHERE bookingID = NEW.bookingID;
    
    -- Log the service update
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, NEW.bookingID, 'Update',
           CONCAT('Service charge updated. Difference: ', cost_difference)
    FROM Booking b
    WHERE b.bookingID = NEW.bookingID;
END//
DELIMITER ;

-- Trigger 11: Update invoice service charges when service is removed
DELIMITER //
CREATE TRIGGER trg_update_service_charges_delete
AFTER DELETE ON Service_Usage
FOR EACH ROW
BEGIN
    DECLARE removed_cost DECIMAL(15,2);
    
    -- Calculate the cost that was removed
    SET removed_cost = OLD.rate * OLD.quantity;
    
    -- Update the invoice service charges
    UPDATE Invoice
    SET serviceCharges = serviceCharges - removed_cost
    WHERE bookingID = OLD.bookingID;
    
    -- Log the service removal
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, OLD.bookingID, 'Delete',
           CONCAT('Service charge removed: ', removed_cost)
    FROM Booking b
    WHERE b.bookingID = OLD.bookingID;
END//
DELIMITER ;

-- Trigger 12: Update invoice when late checkout charge is added
DELIMITER //
CREATE TRIGGER trg_update_late_checkout_charges
AFTER INSERT ON Late_Checkout
FOR EACH ROW
BEGIN
    -- Update the invoice service charges with late checkout fee
    UPDATE Invoice
    SET serviceCharges = serviceCharges + IFNULL(NEW.amount, 0)
    WHERE bookingID = NEW.bookingID;
    
    -- Log the late checkout charge
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, NEW.bookingID, 'Update',
           CONCAT('Late checkout charge added: ', IFNULL(NEW.amount, 0))
    FROM Booking b
    WHERE b.bookingID = NEW.bookingID;
END//
DELIMITER ;

-- Trigger 13: Update invoice when late checkout charge is updated
DELIMITER //
CREATE TRIGGER trg_update_late_checkout_charges_update
AFTER UPDATE ON Late_Checkout
FOR EACH ROW
BEGIN
    DECLARE charge_difference DECIMAL(10,2);
    
    -- Calculate the difference in late checkout charges
    SET charge_difference = IFNULL(NEW.amount, 0) - IFNULL(OLD.amount, 0);
    
    -- Update the invoice service charges
    UPDATE Invoice
    SET serviceCharges = serviceCharges + charge_difference
    WHERE bookingID = NEW.bookingID;
    
    -- Log the late checkout charge update
    INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription)
    SELECT b.branchID, NULL, NEW.bookingID, 'Update',
           CONCAT('Late checkout charge updated. Difference: ', charge_difference)
    FROM Booking b
    WHERE b.bookingID = NEW.bookingID;
END//
DELIMITER ;

SELECT 'Triggers created successfully!' as Status;
