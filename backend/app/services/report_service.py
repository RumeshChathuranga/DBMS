"""
Report Service
Handles report generation and analytics
"""
from typing import Dict, Any, List
from datetime import date
from decimal import Decimal
import logging

from app.database.connection import DatabaseOperations
from app.database.queries import ReportQueries

logger = logging.getLogger(__name__)


class ReportService:
    """Report generation service"""
    
    @staticmethod
    def get_occupancy_report(
        start_date: date,
        end_date: date,
        branch_id: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Generate room occupancy report
        
        Args:
            start_date: Start date
            end_date: End date
            branch_id: Branch ID (0 for all branches)
            
        Returns:
            Occupancy report data
        """
        try:
            report_data = DatabaseOperations.execute_query(
                ReportQueries.ROOM_OCCUPANCY_BY_DATE_RANGE,
                (end_date, start_date, branch_id, branch_id),
                fetch_all=True
            )
            
            logger.info(f"Occupancy report generated for {start_date} to {end_date}")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate occupancy report: {e}")
            raise
    
    @staticmethod
    def get_revenue_report(
        year: int,
        month: int,
        branch_id: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Generate monthly revenue report
        
        Args:
            year: Year
            month: Month (1-12)
            branch_id: Branch ID (0 for all branches)
            
        Returns:
            Revenue report data
        """
        try:
            report_data = DatabaseOperations.execute_query(
                ReportQueries.MONTHLY_REVENUE_BY_BRANCH,
                (year, month, branch_id, branch_id),
                fetch_all=True
            )
            
            logger.info(f"Revenue report generated for {year}-{month:02d}")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate revenue report: {e}")
            raise
    
    @staticmethod
    def get_service_usage_report(
        start_date: date,
        end_date: date,
        branch_id: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Generate service usage report
        
        Args:
            start_date: Start date
            end_date: End date
            branch_id: Branch ID (0 for all branches)
            
        Returns:
            Service usage report data
        """
        try:
            report_data = DatabaseOperations.execute_query(
                ReportQueries.SERVICE_USAGE_REPORT,
                (branch_id, branch_id, start_date, end_date),
                fetch_all=True
            )
            
            logger.info(f"Service usage report generated for {start_date} to {end_date}")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate service usage report: {e}")
            raise
    
    @staticmethod
    def get_unpaid_balances_report(branch_id: int = 0) -> List[Dict[str, Any]]:
        """
        Generate unpaid balances report
        
        Args:
            branch_id: Branch ID (0 for all branches)
            
        Returns:
            Unpaid balances report data
        """
        try:
            report_data = DatabaseOperations.execute_query(
                ReportQueries.UNPAID_BALANCES_REPORT,
                (branch_id, branch_id),
                fetch_all=True
            )
            
            logger.info("Unpaid balances report generated")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate unpaid balances report: {e}")
            raise