"""
Database Connection Management
Handles MySQL connections with PyMySQL
"""
import pymysql
from pymysql.cursors import DictCursor
from typing import Optional, Tuple, List, Dict, Any
from contextlib import contextmanager
import logging
from queue import Queue, Empty
import threading

from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionPool:
    """Simple connection pool for PyMySQL"""
    
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.pool = Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            for _ in range(self.max_connections):
                conn = self._create_connection()
                self.pool.put(conn)
            logger.info("✅ Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing connection pool: {e}")
            raise
    
    def _create_connection(self):
        """Create a new database connection"""
        return pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            cursorclass=DictCursor,
            autocommit=False
        )
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            # Try to get a connection with timeout
            conn = self.pool.get(timeout=5)
            
            # Test if connection is alive
            try:
                conn.ping(reconnect=True)
            except:
                # Connection is dead, create a new one
                conn = self._create_connection()
            
            return conn
        except Empty:
            logger.warning("Connection pool exhausted, creating new connection")
            return self._create_connection()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        try:
            if conn.open:
                self.pool.put_nowait(conn)
        except:
            # Pool is full, close the connection
            conn.close()


class Database:
    """Database connection manager"""
    
    _pool: Optional[ConnectionPool] = None
    
    @classmethod
    def initialize_pool(cls) -> None:
        """Initialize the connection pool"""
        if cls._pool is None:
            cls._pool = ConnectionPool(max_connections=10)
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._pool is None:
            cls.initialize_pool()
        return cls._pool.get_connection()
    
    @classmethod
    def return_connection(cls, conn):
        """Return a connection to the pool"""
        if cls._pool:
            cls._pool.return_connection(conn)
    
    @classmethod
    @contextmanager
    def get_db_connection(cls):
        """
        Context manager for database connections
        
        Usage:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
        """
        connection = None
        try:
            connection = cls.get_connection()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"❌ Database error: {e}")
            raise
        finally:
            if connection:
                cls.return_connection(connection)
    
    @classmethod
    @contextmanager
    def get_db_cursor(cls, dictionary: bool = True):
        """
        Context manager for database cursor
        
        Usage:
            with Database.get_db_cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
        """
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"❌ Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                cls.return_connection(connection)


class DatabaseOperations:
    """Common database operations"""
    
    @staticmethod
    def execute_query(
        query: str, 
        params: Optional[Tuple] = None, 
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Optional[Any]:
        """Execute a SELECT query"""
        try:
            with Database.get_db_cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Query execution error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    @staticmethod
    def execute_insert(
        query: str, 
        params: Optional[Tuple] = None
    ) -> int:
        """Execute an INSERT query"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
                
        except Exception as e:
            logger.error(f"❌ Insert execution error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    @staticmethod
    def execute_update(
        query: str, 
        params: Optional[Tuple] = None
    ) -> int:
        """Execute an UPDATE query"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
                
        except Exception as e:
            logger.error(f"❌ Update execution error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    @staticmethod
    def execute_delete(
        query: str, 
        params: Optional[Tuple] = None
    ) -> int:
        """Execute a DELETE query"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                deleted_rows = cursor.rowcount
                cursor.close()
                return deleted_rows
                
        except Exception as e:
            logger.error(f"❌ Delete execution error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    @staticmethod
    def execute_transaction(operations: List[Tuple[str, Tuple]]) -> bool:
        """Execute multiple queries in a transaction"""
        try:
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                
                for query, params in operations:
                    cursor.execute(query, params or ())
                
                conn.commit()
                cursor.close()
                return True
                
        except Exception as e:
            logger.error(f"❌ Transaction error: {e}")
            raise


# Initialize the pool when the module is imported
try:
    Database.initialize_pool()
except Exception as e:
    logger.warning(f"⚠️ Could not initialize database pool on import: {e}")
    logger.warning("Database will be initialized on first use")


# Test function
if __name__ == "__main__":
    print("Testing database connection...")
    try:
        with Database.get_db_cursor() as cursor:
            cursor.execute("SELECT DATABASE() as db_name")
            result = cursor.fetchone()
            print(f"✅ Connected to database: {result['db_name']}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"   - {table_name}")
                
    except Exception as e:
        print(f"❌ Connection test failed: {e}")