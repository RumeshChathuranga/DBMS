"""
Booking Service
Handles booking and reservation business logic
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
import logging

from app.database.connection import DatabaseOperations, Database
from app.database.queries import (
    RoomQueries, GuestQueries, 
    RoomTypeQueries, LogQueries
)
from app.utils.helpers import DateTimeHelper, StringHelper
from app.utils.validators import Validators

logger = logging.getLogger(__name__)


class BookingService:
    """Booking service"""
    
    @staticmethod
    def check_room_availability(
        branch_id: int,
        type_id: int,
        check_in: datetime,
        check_out: datetime
    ) -> List[Dict[str, Any]]:
        """Check available rooms for given criteria"""
        try:
            is_valid, error_msg = Validators.validate_date_range(check_in, check_out)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Direct SQL query with all required fields
            query = """
                SELECT r.roomID, r.branchID, r.typeID, r.roomNo, r.roomStatus,
                       rt.typeName, rt.capacity, rt.currRate,
                       br.branchLocation
                FROM Room r
                JOIN Room_Type rt ON r.typeID = rt.typeID
                JOIN Branch br ON r.branchID = br.branchID
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
            
            available_rooms = DatabaseOperations.execute_query(
                query,
                (branch_id, type_id, branch_id, 
                 check_out, check_in,
                 check_out, check_in,
                 check_in, check_out),
                fetch_all=True
            )
            
            logger.info(f"Found {len(available_rooms)} available rooms")
            return available_rooms
            
        except Exception as e:
            logger.error(f"Failed to check room availability: {e}")
            raise
    
    @staticmethod
    def create_booking(booking_data: Dict[str, Any], user_id: int) -> Optional[int]:
        """Create a new booking"""
        try:
            is_valid, error_msg = Validators.validate_date_range(
                booking_data['checkInDate'],
                booking_data['checkOutDate']
            )
            if not is_valid:
                raise ValueError(error_msg)
            
            room = DatabaseOperations.execute_query(
                RoomQueries.GET_ROOM_BY_ID,
                (booking_data['roomID'],),
                fetch_one=True
            )
            
            if not room:
                raise ValueError("Room not found")
            
            if room['roomStatus'] != 'Available':
                raise ValueError(f"Room is not available")
            
            is_valid, error_msg = Validators.validate_guest_count(
                booking_data['numGuests'],
                room['capacity']
            )
            if not is_valid:
                raise ValueError(error_msg)
            
            available_rooms = BookingService.check_room_availability(
                booking_data['branchID'],
                room['typeID'],
                booking_data['checkInDate'],
                booking_data['checkOutDate']
            )
            
            if not any(r['roomID'] == booking_data['roomID'] for r in available_rooms):
                raise ValueError("Room is not available for selected dates")
            
            create_query = """
                INSERT INTO Booking (guestID, branchID, roomID, rate, checkInDate, checkOutDate, numGuests, bookingStatus)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            booking_id = DatabaseOperations.execute_insert(
                create_query,
                (
                    booking_data['guestID'],
                    booking_data['branchID'],
                    booking_data['roomID'],
                    room['currRate'],
                    booking_data['checkInDate'],
                    booking_data['checkOutDate'],
                    booking_data['numGuests'],
                    'Booked'
                )
            )
            
            DatabaseOperations.execute_insert(
                LogQueries.CREATE_LOG,
                (
                    booking_data['branchID'],
                    user_id,
                    booking_id,
                    'Create',
                    f"Booking created for room {room['roomNo']}"
                )
            )
            
            logger.info(f"Booking created: ID {booking_id}")
            return booking_id
            
        except Exception as e:
            logger.error(f"Failed to create booking: {e}")
            raise
    
    @staticmethod
    def get_booking_by_id(booking_id: int) -> Optional[Dict[str, Any]]:
        """Get booking by ID with full details"""
        try:
            query = """
                SELECT 
                    b.bookingID,
                    b.guestID,
                    b.branchID,
                    b.roomID,
                    b.rate,
                    b.checkInDate,
                    b.checkOutDate,
                    b.numGuests,
                    b.bookingStatus,
                    g.firstName,
                    g.lastName,
                    g.phone,
                    g.email,
                    r.roomNo,
                    rt.typeName,
                    br.branchLocation
                FROM Booking b
                JOIN Guest g ON b.guestID = g.guestID
                JOIN Room r ON b.roomID = r.roomID
                JOIN Room_Type rt ON r.typeID = rt.typeID
                JOIN Branch br ON b.branchID = br.branchID
                WHERE b.bookingID = %s
            """
            
            booking = DatabaseOperations.execute_query(
                query,
                (booking_id,),
                fetch_one=True
            )
            
            if booking:
                nights = DateTimeHelper.calculate_nights(
                    booking['checkInDate'],
                    booking['checkOutDate']
                )
                booking['nights'] = nights
                booking['bookingReference'] = StringHelper.generate_booking_reference(
                    booking['bookingID'],
                    booking['branchID']
                )
            
            return booking
            
        except Exception as e:
            logger.error(f"Failed to get booking: {e}")
            return None
    
    @staticmethod
    def get_bookings(
        branch_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """Get bookings with filters - FIXED VERSION"""
        try:
            logger.info(f"Getting bookings - branch_id: {branch_id}, status: {status}, page: {page}, page_size: {page_size}")
            
            # Complete query with ALL required fields
            query = """
                SELECT 
                    b.bookingID,
                    b.guestID,
                    b.branchID,
                    b.roomID,
                    b.rate,
                    b.checkInDate,
                    b.checkOutDate,
                    b.numGuests,
                    b.bookingStatus,
                    g.firstName,
                    g.lastName,
                    g.phone,
                    g.email,
                    r.roomNo,
                    rt.typeName,
                    br.branchLocation
                FROM Booking b
                JOIN Guest g ON b.guestID = g.guestID
                JOIN Room r ON b.roomID = r.roomID
                JOIN Room_Type rt ON r.typeID = rt.typeID
                JOIN Branch br ON b.branchID = br.branchID
            """
            
            conditions = []
            params = []
            
            if branch_id:
                conditions.append("b.branchID = %s")
                params.append(branch_id)
            
            if status:
                conditions.append("b.bookingStatus = %s")
                params.append(status)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY b.checkInDate DESC"
            
            logger.info(f"Executing query: {query}")
            logger.info(f"With params: {params}")
            
            bookings = DatabaseOperations.execute_query(
                query,
                tuple(params),
                fetch_all=True
            )
            
            logger.info(f"Retrieved {len(bookings) if bookings else 0} bookings")
            return bookings
            
        except Exception as e:
            logger.error(f"Failed to get bookings: {e}")
            logger.exception("Full exception details:")
            raise
    
    @staticmethod
    def check_in(booking_id: int, user_id: int) -> bool:
        """Check in a guest"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                
                booking = BookingService.get_booking_by_id(booking_id)
                
                if not booking:
                    raise ValueError("Booking not found")
                
                if booking['bookingStatus'] != 'Booked':
                    raise ValueError(f"Cannot check in: status is {booking['bookingStatus']}")
                
                cursor.execute(
                    "UPDATE Booking SET bookingStatus = %s WHERE bookingID = %s",
                    ('CheckedIn', booking_id)
                )
                
                cursor.execute(
                    "UPDATE Room SET roomStatus = %s WHERE roomID = %s",
                    ('Occupied', booking['roomID'])
                )
                
                cursor.execute(
                    LogQueries.CREATE_LOG,
                    (
                        booking['branchID'],
                        user_id,
                        booking_id,
                        'CheckIn',
                        f"Guest checked in to room {booking['roomNo']}"
                    )
                )
                
                conn.commit()
                cursor.close()
                
                logger.info(f"Check-in successful for booking {booking_id}")
                return True
                
        except Exception as e:
            logger.error(f"Check-in failed: {e}")
            raise
    
    @staticmethod
    def check_out(booking_id: int, user_id: int) -> bool:
        """Check out a guest"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                
                booking = BookingService.get_booking_by_id(booking_id)
                
                if not booking:
                    raise ValueError("Booking not found")
                
                if booking['bookingStatus'] != 'CheckedIn':
                    raise ValueError(f"Cannot check out: status is {booking['bookingStatus']}")
                
                cursor.execute(
                    "UPDATE Booking SET bookingStatus = %s WHERE bookingID = %s",
                    ('CheckedOut', booking_id)
                )
                
                cursor.execute(
                    "UPDATE Room SET roomStatus = %s WHERE roomID = %s",
                    ('Available', booking['roomID'])
                )
                
                cursor.execute(
                    LogQueries.CREATE_LOG,
                    (
                        booking['branchID'],
                        user_id,
                        booking_id,
                        'CheckOut',
                        f"Guest checked out from room {booking['roomNo']}"
                    )
                )
                
                conn.commit()
                cursor.close()
                
                logger.info(f"Check-out successful for booking {booking_id}")
                return True
                
        except Exception as e:
            logger.error(f"Check-out failed: {e}")
            raise
    
    @staticmethod
    def update_booking(
        booking_id: int,
        update_data: Dict[str, Any],
        user_id: int
    ) -> bool:
        """Update booking details"""
        try:
            booking = BookingService.get_booking_by_id(booking_id)
            if not booking:
                raise ValueError("Booking not found")
            
            if booking['bookingStatus'] not in ['Booked', 'CheckedIn']:
                raise ValueError("Cannot update cancelled or checked-out booking")
            
            check_in = update_data.get('checkInDate', booking['checkInDate'])
            check_out = update_data.get('checkOutDate', booking['checkOutDate'])
            
            is_valid, error_msg = Validators.validate_date_range(check_in, check_out)
            if not is_valid:
                raise ValueError(error_msg)
            
            update_query = """
                UPDATE Booking 
                SET checkInDate = %s, checkOutDate = %s, numGuests = %s
                WHERE bookingID = %s
            """
            
            affected_rows = DatabaseOperations.execute_update(
                update_query,
                (
                    check_in,
                    check_out,
                    update_data.get('numGuests', booking['numGuests']),
                    booking_id
                )
            )
            
            DatabaseOperations.execute_insert(
                LogQueries.CREATE_LOG,
                (
                    booking['branchID'],
                    user_id,
                    booking_id,
                    'Update',
                    "Booking updated"
                )
            )
            
            logger.info(f"Booking {booking_id} updated")
            return affected_rows > 0
            
        except Exception as e:
            logger.error(f"Failed to update booking: {e}")
            raise
    
    @staticmethod
    def cancel_booking(booking_id: int, user_id: int) -> bool:
        """Cancel a booking"""
        try:
            booking = BookingService.get_booking_by_id(booking_id)
            if not booking:
                raise ValueError("Booking not found")
            
            if booking['bookingStatus'] == 'Cancelled':
                raise ValueError("Booking is already cancelled")
            
            if booking['bookingStatus'] == 'CheckedOut':
                raise ValueError("Cannot cancel a checked-out booking")
            
            affected_rows = DatabaseOperations.execute_update(
                "UPDATE Booking SET bookingStatus = %s WHERE bookingID = %s",
                ('Cancelled', booking_id)
            )
            
            if booking['bookingStatus'] == 'CheckedIn':
                DatabaseOperations.execute_update(
                    "UPDATE Room SET roomStatus = %s WHERE roomID = %s",
                    ('Available', booking['roomID'])
                )
            
            DatabaseOperations.execute_insert(
                LogQueries.CREATE_LOG,
                (
                    booking['branchID'],
                    user_id,
                    booking_id,
                    'Update',
                    "Booking cancelled"
                )
            )
            
            logger.info(f"Booking {booking_id} cancelled")
            return affected_rows > 0
            
        except Exception as e:
            logger.error(f"Failed to cancel booking: {e}")
            raise
    
    @staticmethod
    def get_todays_checkins(branch_id: int) -> List[Dict[str, Any]]:
        """Get bookings scheduled for check-in today"""
        try:
            query = """
                SELECT b.*, g.firstName, g.lastName, r.roomNo
                FROM Booking b
                JOIN Guest g ON b.guestID = g.guestID
                JOIN Room r ON b.roomID = r.roomID
                WHERE b.branchID = %s
                AND DATE(b.checkInDate) = CURDATE()
                AND b.bookingStatus = 'Booked'
            """
            return DatabaseOperations.execute_query(query, (branch_id,), fetch_all=True)
        except Exception as e:
            logger.error(f"Failed to get today's check-ins: {e}")
            raise
    
    @staticmethod
    def get_todays_checkouts(branch_id: int) -> List[Dict[str, Any]]:
        """Get bookings scheduled for check-out today"""
        try:
            query = """
                SELECT b.*, g.firstName, g.lastName, r.roomNo
                FROM Booking b
                JOIN Guest g ON b.guestID = g.guestID
                JOIN Room r ON b.roomID = r.roomID
                WHERE b.branchID = %s
                AND DATE(b.checkOutDate) = CURDATE()
                AND b.bookingStatus = 'CheckedIn'
            """
            return DatabaseOperations.execute_query(query, (branch_id,), fetch_all=True)
        except Exception as e:
            logger.error(f"Failed to get today's check-outs: {e}")
            raise