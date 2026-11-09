"""Service layer for business logic"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.data import DataImport, DataQualityIssue
from app.repositories.audit import AuditLogRepository


class DataImportService:
    """Handle data import operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upload_and_process(self, file, file_type: str, user_id: int) -> DataImport:
        """Upload and process a data file"""
        # Read file content
        contents = await file.read()

        # Create import record
        data_import = DataImport(
            filename=file.filename,
            file_type=file_type,
            file_size=len(contents),
            uploaded_by=user_id,
            status="processing",
        )
        self.session.add(data_import)
        await self.session.flush()
        await self.session.refresh(data_import)

        try:
            # Parse file
            if file_type == "csv":
                df = pd.read_csv(BytesIO(contents))
            elif file_type in ["excel", "xlsx"]:
                df = pd.read_excel(BytesIO(contents))
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            data_import.total_rows = len(df)

            # Validate data
            issues = self._validate_data(df, data_import.id)

            # Save issues
            for issue in issues:
                self.session.add(issue)

            data_import.accepted_rows = data_import.total_rows - sum(
                1 for i in issues if i.severity == "error"
            )
            data_import.rejected_rows = sum(
                1 for i in issues if i.severity == "error"
            )
            data_import.warning_rows = sum(
                1 for i in issues if i.severity == "warning"
            )
            data_import.status = "completed"

            # Log audit
            audit_repo = AuditLogRepository(self.session)
            await audit_repo.create({
                "user_id": user_id,
                "action": "upload_data",
                "resource_type": "data_import",
                "resource_id": data_import.id,
                "details": {"filename": file.filename, "rows": data_import.total_rows},
            })

            await self.session.commit()
            await self.session.refresh(data_import)

        except Exception as e:
            data_import.status = "failed"
            data_import.error_message = str(e)
            await self.session.commit()
            raise

        return data_import

    def _validate_data(self, df: pd.DataFrame, import_id: int) -> List[DataQualityIssue]:
        """Validate uploaded data and return issues"""
        issues = []

        # Check required columns (example for student data)
        required_columns = ["student_id", "course_id", "period_id"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            issues.append(DataQualityIssue(
                data_import_id=import_id,
                row_number=0,
                column_name="",
                issue_type="missing_columns",
                severity="error",
                description=f"Missing required columns: {', '.join(missing_columns)}",
                suggested_fix=f"Add missing columns: {', '.join(missing_columns)}",
            ))

        # Check for missing values in critical columns
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                issues.append(DataQualityIssue(
                    data_import_id=import_id,
                    row_number=0,
                    column_name=col,
                    issue_type="missing_values",
                    severity="warning",
                    description=f"Column '{col}' has {missing_count} missing values",
                    suggested_fix="Review and fill missing values or remove affected rows",
                ))

        # Check for duplicates
        if all(col in df.columns for col in required_columns):
            duplicates = df.duplicated(subset=required_columns, keep=False)
            if duplicates.any():
                dup_count = duplicates.sum()
                issues.append(DataQualityIssue(
                    data_import_id=import_id,
                    row_number=0,
                    column_name=",".join(required_columns),
                    issue_type="duplicates",
                    severity="warning",
                    description=f"Found {dup_count} duplicate rows",
                    suggested_fix="Remove duplicate entries or keep only the latest record",
                ))

        # Check numeric ranges (example for marks)
        if "mark" in df.columns:
            invalid_marks = df[(df["mark"] < 0) | (df["mark"] > 100)]
            if len(invalid_marks) > 0:
                issues.append(DataQualityIssue(
                    data_import_id=import_id,
                    row_number=0,
                    column_name="mark",
                    issue_type="out_of_range",
                    severity="error",
                    description=f"Found {len(invalid_marks)} marks outside valid range (0-100)",
                    suggested_fix="Correct marks to be within 0-100 range",
                ))

        return issues

    async def list_imports(self, skip: int = 0, limit: int = 50) -> List[DataImport]:
        """List recent data imports"""
        from sqlalchemy import select
        result = await self.session.execute(
            select(DataImport).order_by(DataImport.created_at.desc()).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_import(self, import_id: int) -> Optional[DataImport]:
        """Get a specific import"""
        return await self.session.get(DataImport, import_id)

    async def get_issues(
        self,
        import_id: int,
        severity: Optional[str] = None,
        resolved: Optional[bool] = None
    ) -> List[DataQualityIssue]:
        """Get data quality issues for an import"""
        from sqlalchemy import select
        query = select(DataQualityIssue).where(DataQualityIssue.data_import_id == import_id)

        if severity:
            query = query.where(DataQualityIssue.severity == severity)
        if resolved is not None:
            query = query.where(DataQualityIssue.is_resolved == resolved)

        result = await self.session.execute(query)
        return result.scalars().all()