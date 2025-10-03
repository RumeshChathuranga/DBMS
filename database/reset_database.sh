#!/bin/bash

# Reset and populate HRGSMS database
# Usage: bash reset_database.sh

echo "🔄 Resetting HRGSMS Database..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Database connection info
DB_USER="root"
DB_PASSWORD="Ruma@1220"
DB_NAME="hrgsms_db"

echo -e "${YELLOW}⚠️  This will delete all existing data!${NC}"
echo -e "${BLUE}📊 Current database status:${NC}"

# Show current record counts
mysql -u $DB_USER -p$DB_PASSWORD -e "
USE $DB_NAME;
SELECT 'Branches' as Item, COUNT(*) as Count FROM Branch
UNION ALL SELECT 'Rooms', COUNT(*) FROM Room
UNION ALL SELECT 'Users', COUNT(*) FROM User_Account
UNION ALL SELECT 'Guests', COUNT(*) FROM Guest
UNION ALL SELECT 'Bookings', COUNT(*) FROM Booking;
" 2>/dev/null

echo ""
read -p "Continue with database reset? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🗑️  Clearing existing data...${NC}"
    
    # Drop and recreate database
    mysql -u $DB_USER -p$DB_PASSWORD -e "
    DROP DATABASE IF EXISTS $DB_NAME;
    CREATE DATABASE $DB_NAME;
    " 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Database cleared successfully${NC}"
        
        echo -e "${BLUE}🏗️  Creating schema...${NC}"
        mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME < schema.sql 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Schema created successfully${NC}"
            
            echo -e "${BLUE}📊 Inserting seed data...${NC}"
            mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME < seed_data.sql 2>/dev/null
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Seed data inserted successfully${NC}"
                echo ""
                echo -e "${GREEN}🎉 Database reset complete!${NC}"
                echo ""
                echo -e "${BLUE}📝 Login Credentials:${NC}"
                echo "  Username: admin"
                echo "  Password: Admin@123"
            else
                echo -e "${RED}❌ Error inserting seed data${NC}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Error creating schema${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Error clearing database${NC}"
        exit 1
    fi
else
    echo "Operation cancelled."
    exit 0
fi