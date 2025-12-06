from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class InvoiceArchiver:
    def __init__(
        self,
        drive_folder_id: str,
        service_account_file: str,
        sheet_id: Optional[str] = None,
    ) -> None:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=[
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )

        self.drive_service = build("drive", "v3", credentials=credentials)
        self.sheets_service = build("sheets", "v4", credentials=credentials)
        self.drive_folder_id = drive_folder_id
        self.sheet_id = sheet_id

    def upload_to_drive_by_month(self, local_path: Path, filename: str, fecha: datetime) -> str:
        month_folder_id = self._get_or_create_folder(self.drive_folder_id, fecha.strftime("%Y-%m"))

        file_metadata = {"name": filename, "parents": [month_folder_id]}
        media = MediaFileUpload(str(local_path), resumable=True)

        file = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")

    def append_invoice_to_sheet(self, fecha: datetime, empresa: str, drive_file_id: str) -> None:
        if not self.sheet_id:
            return

        fecha_str = fecha.isoformat(timespec="seconds")
        link = f"https://drive.google.com/file/d/{drive_file_id}/view"

        values = [[fecha_str, empresa, "", "", "", link]]

        body = {"values": values}

        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range="Hoja1!A:F",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()

    def _get_or_create_folder(self, parent_id: str, folder_name: str) -> str:
        query = (
            "mimeType='application/vnd.google-apps.folder' "
            f"and name='{folder_name}' "
            f"and '{parent_id}' in parents "
            "and trashed=false"
        )

        results = (
            self.drive_service.files()
            .list(q=query, fields="files(id, name)", pageSize=1)
            .execute()
        )

        files = results.get("files", [])
        if files:
            return files[0]["id"]

        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = (
            self.drive_service.files()
            .create(body=file_metadata, fields="id")
            .execute()
        )

        return folder["id"]
