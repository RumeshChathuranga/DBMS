"""
SQL Queries Repository
All raw SQL queries organized by feature/module
"""


class UserQueries:
    """Queries related to User_Account table"""
    
    # Authentication
    GET_USER_BY_USERNAME = """
        SELECT userID, username, userPassword, userRole, branchID, 
               first_name, last_name, email, phone
        FROM User_Account 
        WHERE username = %s
    """
    
    GET_USER_BY_ID = """
        SELECT userID, username, userRole, branchID, 
               first_name, last_name, email, phone
        FROM User_Account 
        WHERE userID = %s
    """
    
    CREATE_USER = """
        INSERT INTO User_Account 
        (username, userPassword, userRole, branchID, NIC, first_name, last_name, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    UPDATE_USER = """
        UPDATE User_Account 
        SET first_name = %s, last_name = %s, phone = %s, email = %s
        WHERE userID = %s
    """
    
    GET_ALL_USERS_BY_BRANCH = """
        SELECT userID, username, userRole, first_name, last_name, email, phone
        FROM User_Account 
        WHERE branchID = %s
        ORDER BY userRole, last_name
    """


class GuestQueries:
    """Queries related to Guest table"""
    
    CREATE_GUEST = """
        INSERT INTO Guest (firstName, lastName, phone, email, idNumber)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    GET_GUEST_BY_ID = """
        SELECT guestID, firstName, lastName, phone, email, idNumber
        FROM Guest 
        WHERE guestID = %s
    """
    
    GET_GUEST_BY_ID_NUMBER = """
        SELECT guestID, firstName, lastName, phone, email, idNumber
        FROM Guest 
        WHERE idNumber = %s
    """
    
    SEARCH_GUESTS = """
        SELECT guestID, firstName, lastName, phone, email, idNumber
        FROM Guest 
        WHERE firstName LIKE %s OR lastName LIKE %s OR phone LIKE %s
        ORDER BY lastName, firstName
        LIMIT %s OFFSET %s
    """
    
    UPDATE_GUEST = """
        UPDATE Guest 
        SET firstName = %s, lastName = %s, phone = %s, email = %s
        WHERE guestID = %s
    """


class BranchQueries:
    """Queries related to Branch table"""
    
    GET_ALL_BRANCHES = """
        SELECT branchID, branchLocation, rating, phone, email
        FROM Branch
        ORDER BY branchLocation
    """
    
    GET_BRANCH_BY_ID = """
        SELECT branchID, branchLocation, rating, phone, email
        FROM Branch 
        WHERE branchID = %s
    """


class RoomTypeQueries:
    """Queries related to Room_Type table"""
    
    GET_ALL_ROOM_TYPES = """
        SELECT typeID, typeName, capacity, currRate
        FROM Room_Type
        ORDER BY typeName
    """
    
    GET_ROOM_TYPE_BY_ID = """
        SELECT typeID, typeName, capacity, currRate
        FROM Room_Type 
        WHERE typeID = %s
    """


class RoomQueries:
    """Queries related to Room table"""
    
    GET_ALL_ROOMS_BY_BRANCH = """
        SELECT r.roomID, r.branchID, r.typeID, r.roomNo, r.roomStatus,
               rt.typeName, rt.capacity, rt.currRate,
               b.branchLocation
        FROM Room r
        JOIN Room_Type rt ON r.typeID = rt.typeID
        JOIN Branch b ON r.branchID = b.branchID
        WHERE r.branchID = %s
        ORDER BY r.roomNo
    """
    
    GET_ROOM_BY_ID = """
        SELECT r.roomID, r.branchID, r.typeID, r.roomNo, r.roomStatus,
               rt.typeName, rt.capacity, rt.currRate,
               b.branchLocation
        FROM Room r
        JOIN Room_Type rt ON r.typeID = rt.typeID
        JOIN Branch b ON r.branchID = b.branchID
        WHERE r.roomID = %s
    """
    
    # Critical query: Check room availability for date range
    CHECK_ROOM_AVAILABILITY = """
        SELECT r.roomID, r.branchID, r.typeID, r.roomNo, r.roomStatus,
               rt.typeName, rt.capacity, rt.currRate
        FROM Room r
        JOIN Room_Type rt ON r.typeID = rt.typeID
        WHERE r.branchID = %s 
        AND r.typeID = %s 
        AND r.roomStatus = 'Available'
        AND r.roomID NOT IN (
            SELECT roomID 
            FROM Booking 
            WHERE branchID = %s
            AND bookingStatus IN ('Booked', 'CheckedIn')
            AND (
                (checkInDate <= %s AND checkOutDate > %s)
                OR (checkInDate < %s AND checkOutDate >= %s)
                OR (checkInDate >= %s AND checkOutDate <= %s)
            )
        )
        ORDER BY r.roomNo
    """
    
    UPDATE_ROOM_STATUS = """
        UPDATE Room 
        SET roomStatus = %s 
        WHERE roomID = %s
    """


class BookingQueries:
    """Queries related to Booking table"""
    
    CREATE_BOOKING = """
        INSERT INTO Booking 
        (guestID, branchID, roomID, rate, checkInDate, checkOutDate, 
         numGuests, bookingStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    GET_BOOKING_BY_ID = """
        SELECT b.bookingID, b.guestID, b.branchID, b.roomID, b.rate,
               b.checkInDate, b.checkOutDate, b.numGuests, b.bookingStatus,
               g.firstName, g.lastName, g.phone, g.email,
               r.roomNo, rt.typeName,
               br.branchLocation
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        JOIN Branch br ON b.branchID = br.branchID
        WHERE b.bookingID = %s
    """
    
    GET_ALL_BOOKINGS = """
        SELECT b.bookingID, b.checkInDate, b.checkOutDate, b.bookingStatus,
               g.firstName, g.lastName, g.phone,
               r.roomNo, rt.typeName,
               br.branchLocation
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        JOIN Branch br ON b.branchID = br.branchID
        ORDER BY b.checkInDate DESC
        LIMIT %s OFFSET %s
    """
    
    GET_BOOKINGS_BY_BRANCH = """
        SELECT b.bookingID, b.checkInDate, b.checkOutDate, b.bookingStatus,
               g.firstName, g.lastName, g.phone,
               r.roomNo, rt.typeName
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        WHERE b.branchID = %s
        ORDER BY b.checkInDate DESC
        LIMIT %s OFFSET %s
    """
    
    GET_BOOKINGS_BY_STATUS = """
        SELECT b.bookingID, b.checkInDate, b.checkOutDate, b.bookingStatus,
               g.firstName, g.lastName, g.phone,
               r.roomNo, rt.typeName,
               br.branchLocation
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        JOIN Branch br ON b.branchID = br.branchID
        WHERE b.bookingStatus = %s
        ORDER BY b.checkInDate DESC
    """
    
    UPDATE_BOOKING_STATUS = """
        UPDATE Booking 
        SET bookingStatus = %s 
        WHERE bookingID = %s
    """
    
    UPDATE_BOOKING = """
        UPDATE Booking 
        SET checkInDate = %s, checkOutDate = %s, numGuests = %s
        WHERE bookingID = %s
    """
    
    # Get bookings for check-in today
    GET_TODAYS_CHECKINS = """
        SELECT b.bookingID, b.checkInDate, b.checkOutDate,
               g.firstName, g.lastName, g.phone,
               r.roomNo, rt.typeName
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        WHERE b.branchID = %s
        AND DATE(b.checkInDate) = CURDATE()
        AND b.bookingStatus = 'Booked'
        ORDER BY b.checkInDate
    """
    
    # Get bookings for check-out today
    GET_TODAYS_CHECKOUTS = """
        SELECT b.bookingID, b.checkInDate, b.checkOutDate,
               g.firstName, g.lastName, g.phone,
               r.roomNo, rt.typeName
        FROM Booking b
        JOIN Guest g ON b.guestID = g.guestID
        JOIN Room r ON b.roomID = r.roomID
        JOIN Room_Type rt ON r.typeID = rt.typeID
        WHERE b.branchID = %s
        AND DATE(b.checkOutDate) = CURDATE()
        AND b.bookingStatus = 'CheckedIn'
        ORDER BY b.checkOutDate
    """


class ServiceQueries:
    """Queries related to Chargeble_Service table"""
    
    GET_ALL_SERVICES = """
        SELECT serviceID, serviceType, unit, ratePerUnit
        FROM Chargeble_Service
        ORDER BY serviceType
    """
    
    GET_SERVICE_BY_ID = """
        SELECT serviceID, serviceType, unit, ratePerUnit
        FROM Chargeble_Service 
        WHERE serviceID = %s
    """


class ServiceUsageQueries:
    """Queries related to Service_Usage table"""
    
    CREATE_SERVICE_USAGE = """
        INSERT INTO Service_Usage 
        (usageID, bookingID, serviceID, rate, quantity, usedAt)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    GET_SERVICES_BY_BOOKING = """
        SELECT su.usageID, su.bookingID, su.serviceID, su.rate, 
               su.quantity, su.usedAt,
               cs.serviceType, cs.unit,
               (su.rate * su.quantity) as totalCharge
        FROM Service_Usage su
        JOIN Chargeble_Service cs ON su.serviceID = cs.serviceID
        WHERE su.bookingID = %s
        ORDER BY su.usedAt DESC
    """
    
    GET_SERVICE_USAGE_BY_ID = """
        SELECT su.usageID, su.bookingID, su.serviceID, su.rate, 
               su.quantity, su.usedAt,
               cs.serviceType, cs.unit
        FROM Service_Usage su
        JOIN Chargeble_Service cs ON su.serviceID = cs.serviceID
        WHERE su.usageID = %s
    """


class InvoiceQueries:
    """Queries related to Invoice table"""
    
    CREATE_INVOICE = """
        INSERT INTO Invoice 
        (bookingID, policyID, discountCode, paymentPlan, 
         roomCharges, serviceCharges, taxAmount, discountAmount, 
         settledAmount, invoiceStatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    GET_INVOICE_BY_BOOKING = """
        SELECT i.invoiceID, i.bookingID, i.policyID, i.discountCode,
               i.paymentPlan, i.roomCharges, i.serviceCharges, 
               i.taxAmount, i.discountAmount, i.settledAmount, i.invoiceStatus,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount) as totalAmount,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount - i.settledAmount) as balanceDue
        FROM Invoice i
        WHERE i.bookingID = %s
    """
    
    GET_INVOICE_BY_ID = """
        SELECT i.invoiceID, i.bookingID, i.policyID, i.discountCode,
               i.paymentPlan, i.roomCharges, i.serviceCharges, 
               i.taxAmount, i.discountAmount, i.settledAmount, i.invoiceStatus,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount) as totalAmount,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount - i.settledAmount) as balanceDue,
               b.checkInDate, b.checkOutDate,
               g.firstName, g.lastName, g.phone, g.email
        FROM Invoice i
        JOIN Booking b ON i.bookingID = b.bookingID
        JOIN Guest g ON b.guestID = g.guestID
        WHERE i.invoiceID = %s
    """
    
    UPDATE_INVOICE_SETTLED_AMOUNT = """
        UPDATE Invoice 
        SET settledAmount = %s, invoiceStatus = %s
        WHERE invoiceID = %s
    """
    
    GET_PENDING_INVOICES = """
        SELECT i.invoiceID, i.bookingID, i.invoiceStatus,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount) as totalAmount,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount - i.settledAmount) as balanceDue,
               g.firstName, g.lastName, g.phone,
               b.checkOutDate
        FROM Invoice i
        JOIN Booking b ON i.bookingID = b.bookingID
        JOIN Guest g ON b.guestID = g.guestID
        WHERE i.invoiceStatus IN ('Pending', 'Partially Paid')
        AND b.branchID = %s
        ORDER BY b.checkOutDate
    """


class PaymentQueries:
    """Queries related to Payment table"""
    
    CREATE_PAYMENT = """
        INSERT INTO Payment 
        (invoiceID, transactionDate, paymentMethod, amount)
        VALUES (%s, %s, %s, %s)
    """
    
    GET_PAYMENTS_BY_INVOICE = """
        SELECT transactionID, invoiceID, transactionDate, 
               paymentMethod, amount
        FROM Payment 
        WHERE invoiceID = %s
        ORDER BY transactionDate DESC
    """
    
    GET_PAYMENT_BY_ID = """
        SELECT transactionID, invoiceID, transactionDate, 
               paymentMethod, amount
        FROM Payment 
        WHERE transactionID = %s
    """


class TaxPolicyQueries:
    """Queries related to Tax_Policy table"""
    
    GET_ALL_TAX_POLICIES = """
        SELECT policyID, rate, appliesTo, policyName
        FROM Tax_Policy
        ORDER BY appliesTo
    """
    
    GET_TAX_POLICY_BY_TYPE = """
        SELECT policyID, rate, appliesTo, policyName
        FROM Tax_Policy 
        WHERE appliesTo = %s
        LIMIT 1
    """


class DiscountQueries:
    """Queries related to Discount table"""
    
    GET_VALID_DISCOUNTS = """
        SELECT discountCode, discountName, discountCondition, 
               discountValue, validFrom, validTo
        FROM Discount
        WHERE CURDATE() BETWEEN validFrom AND validTo
        ORDER BY discountValue DESC
    """
    
    GET_DISCOUNT_BY_CODE = """
        SELECT discountCode, discountName, discountCondition, 
               discountValue, validFrom, validTo
        FROM Discount 
        WHERE discountCode = %s
        AND CURDATE() BETWEEN validFrom AND validTo
    """


class LogQueries:
    """Queries related to Log table"""
    
    CREATE_LOG = """
        INSERT INTO Log 
        (branchID, userID, bookingID, logAction, logDescription)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    GET_RECENT_LOGS = """
        SELECT l.logID, l.event_time, l.logAction, l.logDescription,
               u.username, u.first_name, u.last_name,
               br.branchLocation
        FROM Log l
        LEFT JOIN User_Account u ON l.userID = u.userID
        LEFT JOIN Branch br ON l.branchID = br.branchID
        WHERE l.branchID = %s
        ORDER BY l.event_time DESC
        LIMIT %s
    """


class ReportQueries:
    """Queries for various reports"""
    
    # Room occupancy report
    ROOM_OCCUPANCY_BY_DATE_RANGE = """
        SELECT b.branchID, br.branchLocation,
               COUNT(DISTINCT bk.roomID) as occupiedRooms,
               COUNT(DISTINCT r.roomID) as totalRooms,
               ROUND((COUNT(DISTINCT bk.roomID) / COUNT(DISTINCT r.roomID)) * 100, 2) as occupancyRate
        FROM Branch b
        CROSS JOIN Room r ON b.branchID = r.branchID
        LEFT JOIN Booking bk ON r.roomID = bk.roomID 
            AND bk.bookingStatus IN ('Booked', 'CheckedIn')
            AND bk.checkInDate <= %s 
            AND bk.checkOutDate >= %s
        WHERE b.branchID = %s OR %s = 0
        GROUP BY b.branchID, br.branchLocation
    """
    
    # Revenue report by branch
    MONTHLY_REVENUE_BY_BRANCH = """
        SELECT b.branchID, br.branchLocation,
               SUM(i.roomCharges) as roomRevenue,
               SUM(i.serviceCharges) as serviceRevenue,
               SUM(i.roomCharges + i.serviceCharges) as totalRevenue,
               COUNT(DISTINCT bk.bookingID) as totalBookings
        FROM Branch b
        JOIN Booking bk ON b.branchID = bk.branchID
        LEFT JOIN Invoice i ON bk.bookingID = i.bookingID
        WHERE YEAR(bk.checkInDate) = %s 
        AND MONTH(bk.checkInDate) = %s
        AND (b.branchID = %s OR %s = 0)
        GROUP BY b.branchID, br.branchLocation
        ORDER BY totalRevenue DESC
    """
    
    # Service usage breakdown
    SERVICE_USAGE_REPORT = """
        SELECT cs.serviceType, cs.unit,
               COUNT(su.usageID) as usageCount,
               SUM(su.quantity) as totalQuantity,
               SUM(su.rate * su.quantity) as totalRevenue,
               AVG(su.rate * su.quantity) as avgRevenuePerUse
        FROM Chargeble_Service cs
        LEFT JOIN Service_Usage su ON cs.serviceID = su.serviceID
        LEFT JOIN Booking bk ON su.bookingID = bk.bookingID
        WHERE (bk.branchID = %s OR %s = 0)
        AND su.usedAt BETWEEN %s AND %s
        GROUP BY cs.serviceID, cs.serviceType, cs.unit
        ORDER BY totalRevenue DESC
    """
    
    # Guest billing summary with unpaid balances
    UNPAID_BALANCES_REPORT = """
        SELECT i.invoiceID, i.bookingID,
               g.firstName, g.lastName, g.phone, g.email,
               br.branchLocation,
               i.roomCharges, i.serviceCharges, i.taxAmount, i.discountAmount,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount) as totalAmount,
               i.settledAmount,
               (i.roomCharges + i.serviceCharges + i.taxAmount - i.discountAmount - i.settledAmount) as balanceDue,
               bk.checkOutDate
        FROM Invoice i
        JOIN Booking bk ON i.bookingID = bk.bookingID
        JOIN Guest g ON bk.guestID = g.guestID
        JOIN Branch br ON bk.branchID = br.branchID
        WHERE i.invoiceStatus IN ('Pending', 'Partially Paid')
        AND (bk.branchID = %s OR %s = 0)
        ORDER BY bk.checkOutDate DESC
    """