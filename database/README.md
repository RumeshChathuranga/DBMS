# 🗃️ Database Documentation - HRGSMS

This directory contains all database-related files for the Hotel Reservation and Guest Services Management System.

## 📋 Overview

The HRGSMS database is designed to handle all aspects of hotel operations including room management, reservations, guest services, and billing across multiple hotel branches (Colombo, Kandy, and Galle).

## 🗂️ Database Files

| File                | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| `schema.sql`        | Complete database schema with all tables, relationships, and constraints |
| `seed_data.sql`     | Sample data for testing and development                                  |
| `triggers.sql`      | Database triggers for automated operations                               |
| `procedures.sql`    | Stored procedures for complex operations                                 |
| `functions.sql`     | Custom database functions                                                |
| `indexes.sql`       | Performance optimization indexes                                         |
| `reset_database.sh` | Script to reset and rebuild the database                                 |

## 🏗️ Database Schema

### Core Tables

#### Branch Management

- **Branch**: Hotel branch information (Colombo, Kandy, Galle)
- **Room_Type**: Room categories (Single, Double, Suite, etc.)
- **Room**: Individual room records with type and branch associations

#### Guest Management

- **Guest**: Guest profile information
- **Guest_Account**: Account details and preferences

#### Reservation System

- **Reservation**: Booking records and details
- **Check_In**: Check-in process tracking
- **Check_Out**: Check-out process tracking

#### Services & Billing

- **Additional_Service**: Hotel services (spa, dining, etc.)
- **Service_Request**: Guest service requests
- **Bill**: Billing information and calculations
- **Payment**: Payment records and methods

#### System Management

- **User**: System user accounts
- **User_Role**: Role definitions for access control

### 🔗 Key Relationships

```
Branch (1) -----> (M) Room
Room_Type (1) --> (M) Room
Guest (1) -------> (M) Reservation
Room (1) --------> (M) Reservation
Reservation (1) -> (1) Check_In
Reservation (1) -> (1) Check_Out
Guest (1) -------> (M) Service_Request
Additional_Service (1) -> (M) Service_Request
Reservation (1) -> (1) Bill
Bill (1) --------> (M) Payment
```

## 📊 Database Features

### 🔧 Stored Procedures

- Guest check-in/check-out automation
- Room availability checking
- Billing calculations
- Revenue reporting
- Occupancy analytics

### ⚡ Triggers

- Automatic room status updates
- Billing calculations on service requests
- Audit trail for critical operations
- Data validation and integrity checks

### 🚀 Functions

- Room rate calculations
- Date utility functions
- Guest loyalty point calculations
- Revenue analysis functions

### 📈 Indexes

- Performance optimization for frequent queries
- Composite indexes for complex searches
- Unique constraints for data integrity

## 🛠️ Setup Instructions

### Prerequisites

- MySQL 8.0 or higher
- Sufficient privileges to create databases
- Command line access

### Quick Setup

```bash
# Navigate to database directory
cd database

# Make reset script executable
chmod +x reset_database.sh

# Run the setup script
./reset_database.sh
```

### Manual Setup

```sql
-- 1. Create database
CREATE DATABASE hrgsms_db;
USE hrgsms_db;

-- 2. Create schema
SOURCE schema.sql;

-- 3. Add indexes
SOURCE indexes.sql;

-- 4. Add stored procedures
SOURCE procedures.sql;

-- 5. Add functions
SOURCE functions.sql;

-- 6. Add triggers
SOURCE triggers.sql;

-- 7. Load sample data
SOURCE seed_data.sql;
```

## 🔐 Security Considerations

### Access Control

- Limited database user privileges
- Role-based access implementation
- Encrypted sensitive data storage

### Data Protection

- Input validation at database level
- Constraint enforcement
- Audit triggers for sensitive operations

## 📈 Performance Optimization

### Indexing Strategy

- Primary key indexes on all tables
- Foreign key indexes for join optimization
- Composite indexes for complex queries
- Covering indexes for frequently accessed columns

### Query Optimization

- Stored procedures for complex operations
- Efficient JOIN strategies
- Proper WHERE clause usage
- LIMIT clauses for large datasets

## 🧪 Testing Data

The `seed_data.sql` file includes:

- 3 hotel branches (Colombo, Kandy, Galle)
- Various room types and configurations
- Sample guest records
- Test reservations
- Service offerings
- User accounts for different roles

## 📋 Maintenance

### Regular Tasks

- Database backup procedures
- Index maintenance and optimization
- Query performance monitoring
- Data archival strategies

### Monitoring

- Connection pool monitoring
- Query execution time tracking
- Storage usage analysis
- Error log review

## 🔄 Migration Support

### Version Control

- Schema versioning strategy
- Migration scripts for updates
- Rollback procedures
- Data migration tools

### Backup Strategy

- Regular automated backups
- Point-in-time recovery
- Cross-branch data synchronization
- Disaster recovery procedures

## 📚 Additional Resources

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Database Design Best Practices](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)
- [Performance Tuning Guide](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

## 🆘 Troubleshooting

### Common Issues

1. **Connection Problems**: Check MySQL service status and credentials
2. **Permission Errors**: Verify user privileges and database access
3. **Performance Issues**: Review query execution plans and indexes
4. **Data Integrity**: Check foreign key constraints and triggers

### Error Codes

- `1045`: Access denied - check credentials
- `1049`: Unknown database - ensure database exists
- `1146`: Table doesn't exist - run schema.sql
- `1452`: Foreign key constraint - check data relationships

---

**Database designed for optimal performance and scalability** 🚀
