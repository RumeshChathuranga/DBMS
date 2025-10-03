USE hrgsms_db;

-- ============================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================

-- Indexes for Booking table (most queried)
CREATE INDEX idx_booking_dates ON Booking(checkInDate, checkOutDate);
CREATE INDEX idx_booking_status ON Booking(bookingStatus);
CREATE INDEX idx_booking_guest ON Booking(guestID);
CREATE INDEX idx_booking_room ON Booking(roomID);
CREATE INDEX idx_booking_branch ON Booking(branchID);

-- Indexes for Room table
CREATE INDEX idx_room_status ON Room(roomStatus);
CREATE INDEX idx_room_type ON Room(typeID);
CREATE INDEX idx_room_branch ON Room(branchID);

-- Indexes for Guest table
CREATE INDEX idx_guest_phone ON Guest(phone);
CREATE INDEX idx_guest_name ON Guest(lastName, firstName);

-- Indexes for Service_Usage table
CREATE INDEX idx_service_usage_booking ON Service_Usage(bookingID);
CREATE INDEX idx_service_usage_date ON Service_Usage(usedAt);

-- Indexes for Invoice table
CREATE INDEX idx_invoice_status ON Invoice(invoiceStatus);
CREATE INDEX idx_invoice_booking ON Invoice(bookingID);

-- Indexes for Payment table
CREATE INDEX idx_payment_invoice ON Payment(invoiceID);
CREATE INDEX idx_payment_date ON Payment(transactionDate);

-- Indexes for Log table
CREATE INDEX idx_log_time ON Log(event_time);
CREATE INDEX idx_log_action ON Log(logAction);
CREATE INDEX idx_log_booking ON Log(bookingID);

-- Composite index for availability checking (critical for performance)
CREATE INDEX idx_booking_room_dates_status ON Booking(roomID, checkInDate, checkOutDate, bookingStatus);

-- Composite index for revenue reports
CREATE INDEX idx_invoice_branch_date ON Invoice(invoiceID, invoiceStatus);

SELECT 'Indexes created successfully!' as Status;
