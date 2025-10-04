"""
Report Routes
Handles report generation and analytics
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Dict, Any, List
from datetime import date
import logging

from app.models.schemas import (
    OccupancyReportQuery, RevenueReportQuery, ServiceUsageReportQuery
)
from app.services.report_service import ReportService
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/recent-activities", response_model=List[Dict[str, Any]])
async def get_recent_activities(
    limit: int = Query(10, ge=1, le=50),
    branch_id: int = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get recent system activities/logs
    
    Available to: All authenticated users
    """
    try:
        from app.database.connection import DatabaseOperations
        from app.database.queries import LogQueries
        
        # Use user's branch if not specified
        if branch_id is None:
            branch_id = current_user.get('branchID')
        
        # Fetch recent logs
        if branch_id is None:
            # Admin user - get logs from all branches
            query = """
                SELECT l.logID, l.event_time, l.logAction, l.logDescription,
                       u.username, u.first_name, u.last_name,
                       br.branchLocation
                FROM Log l
                LEFT JOIN User_Account u ON l.userID = u.userID
                LEFT JOIN Branch br ON l.branchID = br.branchID
                ORDER BY l.event_time DESC
                LIMIT %s
            """
            recent_logs = DatabaseOperations.execute_query(
                query, (limit,), fetch_all=True
            )
        else:
            # Regular user - get logs from specific branch
            recent_logs = DatabaseOperations.execute_query(
                LogQueries.GET_RECENT_LOGS,
                (branch_id, limit),
                fetch_all=True
            )
        
        activities = []
        for log in recent_logs:
            activity = {
                "id": f"log-{log['logID']}",
                "type": log['logAction'].lower() if log['logAction'] else 'system',
                "title": log['logAction'] or 'System Activity',
                "description": log['logDescription'] or 'System activity logged',
                "timestamp": log['event_time'].isoformat() if log['event_time'] else None,
                "user": f"{log['first_name'] or ''} {log['last_name'] or ''}".strip() or log['username'] or 'System',
                "branch": log['branchLocation'] or 'Unknown'
            }
            activities.append(activity)
        
        logger.info(f"Retrieved {len(activities)} recent activities for branch {branch_id}")
        return activities
        
    except Exception as e:
        logger.error(f"Failed to get recent activities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recent activities"
        )


@router.post("/occupancy", dependencies=[Depends(require_role("Admin", "Manager"))])
async def get_occupancy_report(
    query: OccupancyReportQuery,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate room occupancy report
    
    Available to: Admin, Manager
    """
    try:
        # If user is Manager (not Admin), restrict to their branch
        branch_id = query.branchID
        if current_user['userRole'] == 'Manager':
            branch_id = current_user.get('branchID', 0)
        
        report_data = ReportService.get_occupancy_report(
            query.startDate,
            query.endDate,
            branch_id
        )
        
        return {
            "success": True,
            "message": "Occupancy report generated successfully",
            "data": {
                "report": report_data,
                "period": {
                    "startDate": str(query.startDate),
                    "endDate": str(query.endDate)
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate occupancy report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate occupancy report"
        )


@router.post("/revenue", dependencies=[Depends(require_role("Admin", "Manager"))])
async def get_revenue_report(
    query: RevenueReportQuery,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate monthly revenue report
    
    Available to: Admin, Manager
    """
    try:
        # If user is Manager (not Admin), restrict to their branch
        branch_id = query.branchID
        if current_user['userRole'] == 'Manager':
            branch_id = current_user.get('branchID', 0)
        
        report_data = ReportService.get_revenue_report(
            query.year,
            query.month,
            branch_id
        )
        
        return {
            "success": True,
            "message": "Revenue report generated successfully",
            "data": {
                "report": report_data,
                "period": {
                    "year": query.year,
                    "month": query.month
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate revenue report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate revenue report"
        )


@router.post("/service-usage", dependencies=[Depends(require_role("Admin", "Manager"))])
async def get_service_usage_report(
    query: ServiceUsageReportQuery,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate service usage report
    
    Available to: Admin, Manager
    """
    try:
        # If user is Manager (not Admin), restrict to their branch
        branch_id = query.branchID
        if current_user['userRole'] == 'Manager':
            branch_id = current_user.get('branchID', 0)
        
        report_data = ReportService.get_service_usage_report(
            query.startDate,
            query.endDate,
            branch_id
        )
        
        return {
            "success": True,
            "message": "Service usage report generated successfully",
            "data": {
                "report": report_data,
                "period": {
                    "startDate": str(query.startDate),
                    "endDate": str(query.endDate)
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate service usage report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate service usage report"
        )


@router.get("/unpaid-balances", dependencies=[Depends(require_role("Admin", "Manager"))])
async def get_unpaid_balances_report(
    branch_id: int = Query(0),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate unpaid balances report
    
    Available to: Admin, Manager
    """
    try:
        # If user is Manager (not Admin), restrict to their branch
        if current_user['userRole'] == 'Manager':
            branch_id = current_user.get('branchID', 0)
        
        report_data = ReportService.get_unpaid_balances_report(branch_id)
        
        return {
            "success": True,
            "message": "Unpaid balances report generated successfully",
            "data": {
                "report": report_data
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate unpaid balances report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate unpaid balances report"
        )