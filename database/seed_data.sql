USE hrgsms_db;

-- ============================================
-- 1. INSERT BRANCHES (required first!)
-- ============================================

INSERT INTO Branch (branchLocation, rating, phone, email) VALUES
('Colombo', 4.5, '+94112345678', 'colombo@skynest.lk'),
('Kandy', 4.3, '+94812345678', 'kandy@skynest.lk'),
('Galle', 4.7, '+94912345678', 'galle@skynest.lk');

-- ============================================
-- 2. INSERT ROOM TYPES
-- ============================================

INSERT INTO Room_Type (typeName, capacity, currRate) VALUES
('Single', 1, 5000.00),
('Double', 2, 8000.00),
('Deluxe', 2, 12000.00),
('Suite', 4, 20000.00);

-- ============================================
-- 3. INSERT ROOMS (10+ rooms per branch)
-- ============================================

-- Colombo Branch (ID: 1)
INSERT INTO Room (branchID, typeID, roomNo, roomStatus) VALUES
(1, 1, 101, 'Available'),
(1, 1, 102, 'Available'),
(1, 2, 201, 'Available'),
(1, 2, 202, 'Available'),
(1, 3, 301, 'Available'),
(1, 3, 302, 'Available'),
(1, 4, 401, 'Available');

-- Kandy Branch (ID: 2)
INSERT INTO Room (branchID, typeID, roomNo, roomStatus) VALUES
(2, 1, 101, 'Available'),
(2, 1, 102, 'Available'),
(2, 2, 201, 'Available'),
(2, 2, 202, 'Available'),
(2, 3, 301, 'Available'),
(2, 3, 302, 'Available'),
(2, 4, 401, 'Available');

-- Galle Branch (ID: 3)
INSERT INTO Room (branchID, typeID, roomNo, roomStatus) VALUES
(3, 1, 101, 'Available'),
(3, 1, 102, 'Available'),
(3, 2, 201, 'Available'),
(3, 2, 202, 'Available'),
(3, 3, 301, 'Available'),
(3, 3, 302, 'Available'),
(3, 4, 401, 'Available');

-- ============================================
-- 4. INSERT SERVICES (6 required)
-- ============================================

INSERT INTO Chargeble_Service (serviceType, unit, ratePerUnit) VALUES
('Spa services', 'per person', 3000.00),
('Pool access', 'per person', 500.00),
('room service', 'per item', 1000.00),
('laundry', 'per kg', 300.00),
('minibar usage', 'per item', 500.00);

-- ============================================
-- 5. INSERT TAX POLICIES
-- ============================================

INSERT INTO Tax_Policy (rate, appliesTo, policyName) VALUES
(0.1500, 'Room', 'VAT 15%'),
(0.1000, 'Service', 'Service Tax 10%');

-- ============================================
-- 6. INSERT USERS (Password: Admin@123)
-- ============================================

INSERT INTO User_Account (branchID, username, userPassword, userRole, NIC, first_name, last_name, phone, email) VALUES
(NULL, 'admin', '$2b$12$ysf6zMFGct1JrGgzSOwuZeLNTuZgnGmQl9gmVFhE1tcol3tCs36SK', 'Admin', '199512345678', 'System', 'Admin', '+94771234567', 'admin@skynest.lk'),
(1, 'manager_cmb', '$2b$12$ysf6zMFGct1JrGgzSOwuZeLNTuZgnGmQl9gmVFhE1tcol3tCs36SK', 'Manager', '199612345678', 'Colombo', 'Manager', '+94771234568', 'manager.cmb@skynest.lk'),
(2, 'manager_kdy', '$2b$12$ysf6zMFGct1JrGgzSOwuZeLNTuZgnGmQl9gmVFhE1tcol3tCs36SK', 'Manager', '199712345678', 'Kandy', 'Manager', '+94771234569', 'manager.kdy@skynest.lk'),
(1, 'reception_cmb', '$2b$12$ysf6zMFGct1JrGgzSOwuZeLNTuZgnGmQl9gmVFhE1tcol3tCs36SK', 'Reception', '199812345678', 'John', 'Receptionist', '+94771234570', 'reception.cmb@skynest.lk');

-- ============================================
-- 7. INSERT GUESTS (5 required)
-- ============================================

INSERT INTO Guest (firstName, lastName, phone, email, idNumber) VALUES
('Kamal', 'Silva', '+94771234567', 'kamal.silva@email.com', '199512345678V'),
('Nimal', 'Perera', '+94772345678', 'nimal.perera@email.com', '198812345678V'),
('Sunil', 'Fernando', '+94773456789', 'sunil.fernando@email.com', '199212345678V'),
('Amara', 'Dissanayake', '+94774567890', 'amara.d@email.com', '199012345678V'),
('Chamara', 'Wickramasinghe', '+94775678901', 'chamara.w@email.com', '199312345678V');

-- ============================================
-- 8. INSERT BOOKINGS (8 required)
-- ============================================

-- Booking 1: Checked Out (paid)
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (1, 1, 1, 5000.00, DATE_SUB(NOW(), INTERVAL 25 DAY), DATE_SUB(NOW(), INTERVAL 22 DAY), 1, 'CheckedOut');

-- Booking 2: Checked Out (partially paid)
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (2, 1, 3, 8000.00, DATE_SUB(NOW(), INTERVAL 20 DAY), DATE_SUB(NOW(), INTERVAL 17 DAY), 2, 'CheckedOut');

-- Booking 3: Currently Checked In
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (3, 2, 8, 8000.00, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_ADD(NOW(), INTERVAL 3 DAY), 2, 'CheckedIn');

-- Booking 4: Currently Checked In
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (4, 2, 12, 12000.00, NOW(), DATE_ADD(NOW(), INTERVAL 2 DAY), 2, 'CheckedIn');

-- Booking 5: Booked (upcoming)
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (5, 3, 15, 5000.00, DATE_ADD(NOW(), INTERVAL 5 DAY), DATE_ADD(NOW(), INTERVAL 9 DAY), 1, 'Booked');

-- Booking 6: Booked (upcoming)
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (1, 3, 18, 12000.00, DATE_ADD(NOW(), INTERVAL 10 DAY), DATE_ADD(NOW(), INTERVAL 15 DAY), 2, 'Booked');

-- Booking 7: Checked Out (fully paid)
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (2, 1, 5, 12000.00, DATE_SUB(NOW(), INTERVAL 30 DAY), DATE_SUB(NOW(), INTERVAL 27 DAY), 2, 'CheckedOut');

-- Booking 8: Cancelled
INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
VALUES (3, 2, 10, 8000.00, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_ADD(NOW(), INTERVAL 2 DAY), 2, 'Cancelled');


-- Update room statuses
UPDATE Room SET roomStatus = 'Occupied' WHERE roomID IN (8, 12);

-- ============================================
-- 9. INSERT SERVICE USAGE (13 records)
-- ============================================

INSERT INTO Service_Usage (usageID, bookingID, serviceID, rate, quantity, usedAt) VALUES
(1001, 1, 1, 3000.00, 1, DATE_SUB(NOW(), INTERVAL 24 DAY)),
(1002, 1, 3, 1000.00, 2, DATE_SUB(NOW(), INTERVAL 24 DAY)),
(1003, 1, 5, 500.00, 3, DATE_SUB(NOW(), INTERVAL 23 DAY)),
(1004, 2, 2, 500.00, 2, DATE_SUB(NOW(), INTERVAL 19 DAY)),
(1005, 2, 3, 1000.00, 3, DATE_SUB(NOW(), INTERVAL 19 DAY)),
(1006, 2, 4, 300.00, 2, DATE_SUB(NOW(), INTERVAL 18 DAY)),
(1007, 3, 1, 3000.00, 2, NOW()),
(1008, 3, 2, 500.00, 2, NOW()),
(1009, 4, 3, 1000.00, 4, NOW()),
(1010, 4, 5, 500.00, 2, NOW()),
(1011, 7, 1, 3000.00, 2, DATE_SUB(NOW(), INTERVAL 29 DAY)),
(1012, 7, 2, 500.00, 2, DATE_SUB(NOW(), INTERVAL 29 DAY)),
(1013, 7, 3, 1000.00, 2, DATE_SUB(NOW(), INTERVAL 28 DAY));

-- ============================================
-- 10. INSERT INVOICES
-- ============================================

INSERT INTO Invoice (bookingID, policyID, paymentPlan, roomCharges, serviceCharges, taxAmount, discountAmount, settledAmount, invoiceStatus)
VALUES 
(1, 1, 'Full', 15000.00, 6500.00, 3225.00, 0.00, 0.00, 'Pending'),
(2, 1, 'Full', 24000.00, 4600.00, 4290.00, 0.00, 0.00, 'Pending'),
(7, 1, 'Full', 36000.00, 9000.00, 6750.00, 0.00, 0.00, 'Pending');

-- ============================================
-- 11. INSERT PAYMENTS (6 total, 3 partial)
-- ============================================

INSERT INTO Payment (invoiceID, transactionDate, paymentMethod, amount) VALUES
(1, DATE_SUB(CURDATE(), INTERVAL 22 DAY), 'Card', 24725.00),
(2, DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Cash', 10000.00),
(2, DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Card', 5000.00),
(2, DATE_SUB(CURDATE(), INTERVAL 16 DAY), 'Online', 5000.00),
(3, DATE_SUB(CURDATE(), INTERVAL 27 DAY), 'Card', 30000.00),
(3, DATE_SUB(CURDATE(), INTERVAL 27 DAY), 'Card', 21750.00);

-- ============================================
-- 12. INSERT LOGS
-- ============================================

INSERT INTO Log (branchID, userID, bookingID, logAction, logDescription) VALUES
(1, 1, 1, 'Create', 'Booking created'),
(1, 1, 1, 'CheckIn', 'Guest checked in'),
(1, 1, 1, 'CheckOut', 'Guest checked out'),
(1, 1, 2, 'Create', 'Booking created'),
(2, 2, 3, 'Create', 'Booking created'),
(2, 2, 3, 'CheckIn', 'Guest checked in');

-- ============================================
-- SUMMARY
-- ============================================

SELECT '=====================================' as '';
SELECT '   DATABASE SETUP COMPLETE' as '';
SELECT '=====================================' as '';
SELECT 'Branches' as Item, COUNT(*) as Count FROM Branch
UNION ALL SELECT 'Room Types', COUNT(*) FROM Room_Type
UNION ALL SELECT 'Rooms', COUNT(*) FROM Room
UNION ALL SELECT 'Services', COUNT(*) FROM Chargeble_Service
UNION ALL SELECT 'Tax Policies', COUNT(*) FROM Tax_Policy
UNION ALL SELECT 'Users', COUNT(*) FROM User_Account
UNION ALL SELECT 'Guests', COUNT(*) FROM Guest
UNION ALL SELECT 'Bookings', COUNT(*) FROM Booking
UNION ALL SELECT 'Service Usage', COUNT(*) FROM Service_Usage
UNION ALL SELECT 'Invoices', COUNT(*) FROM Invoice
UNION ALL SELECT 'Payments', COUNT(*) FROM Payment
UNION ALL SELECT 'Logs', COUNT(*) FROM Log;

SELECT '' as '';
SELECT 'Login Credentials:' as '';
SELECT '  Username: admin' as '';
SELECT '  Password: Admin@123' as '';
SELECT '=====================================' as '';