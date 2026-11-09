"""Report generation service"""

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, Dict, Any, List

from app.models.report import ReportJob


class ReportService:
    """Handle report generation"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_report(
        self,
        report_request: dict,
        user_id: int
    ) -> ReportJob:
        """Generate a new report"""
        report_job = ReportJob(
            user_id=user_id,
            report_type=report_request["report_type"],
            report_format=report_request["report_format"],
            title=f"{report_request['report_type']} Report - {datetime.utcnow().strftime('%Y-%m-%d')}",
            parameters=report_request.model_dump() if hasattr(report_request, 'model_dump') else report_request,
            status="processing",
        )
        self.session.add(report_job)
        await self.session.flush()
        await self.session.refresh(report_job)

        try:
            # Generate report based on type
            if report_request["report_format"] == "pdf":
                file_path = await self._generate_pdf_report(report_job)
            elif report_request["report_format"] == "excel":
                file_path = await self._generate_excel_report(report_job)
            else:
                file_path = None

            report_job.status = "completed"
            report_job.file_path = file_path
            report_job.generated_at = datetime.utcnow()

            await self.session.commit()
            await self.session.refresh(report_job)

        except Exception as e:
            report_job.status = "failed"
            report_job.error_message = str(e)
            await self.session.commit()
            raise

        return report_job

    async def _generate_pdf_report(self, report_job: ReportJob) -> str:
        """Generate PDF report"""
        # Implementation would use ReportLab
        file_path = f"/tmp/reports/{report_job.id}.pdf"
        # Placeholder - actual implementation would generate PDF
        return file_path

    async def _generate_excel_report(self, report_job: ReportJob) -> str:
        """Generate Excel report"""
        # Implementation would use openpyxl
        file_path = f"/tmp/reports/{report_job.id}.xlsx"
        # Placeholder - actual implementation would generate Excel
        return file_path

    async def list_reports(self, skip: int = 0, limit: int = 50) -> List[ReportJob]:
        """List generated reports"""
        from sqlalchemy import select
        result = await self.session.execute(
            select(ReportJob).order_by(ReportJob.created_at.desc()).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_report_file(self, report_id: int) -> Optional[str]:
        """Get report file path"""
        report = await self.session.get(ReportJob, report_id)
        return report.file_path if report else None