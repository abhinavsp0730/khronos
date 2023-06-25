import csv
import logging
import os
import threading

import gspread
from django.conf import settings
from rich.console import Console
from rich.table import Table

from .constants import MAX_ROW

logger = logging.getLogger(__name__)


class KhronosService:
    def __init__(self, sorted_test_timings: list[dict]):
        self.sorted_test_timings = sorted_test_timings

    @staticmethod
    def save_duration(test, temp_file, test_time_str, time):
        lock = threading.Lock()
        lock.acquire()
        try:
            temp_file.write(f"{str(test)},{test_time_str},{time}{os.linesep}")
        finally:
            lock.release()

    def create_khronos_terminal_report(self):
        try:
            max_row = settings.KHRONOS_REPORT_MAX_ROW
        except AttributeError:
            max_row = MAX_ROW

        top_slowest_test = self.sorted_test_timings[:max_row]
        table = Table(title=f"Khronos Report  (Top {max_row} Slowest Test(s)), Duration (in sec)")
        table.add_column("S. No.", style="cyan", no_wrap=True)
        table.add_column("Test", style="magenta")
        table.add_column("Duration", style="red")

        for index, test_timing in enumerate(top_slowest_test):
            table.add_row(str(index + 1), test_timing[0], str(test_timing[-1]["duration"]))

        console = Console()
        console.print(table)

    @staticmethod
    def check_directory(directory_path: str) -> bool:
        if os.path.isdir(directory_path):
            if os.access(directory_path, os.W_OK):
                return True

        return False

    def create_khronos_csv_report(self):
        try:
            directory_path = settings.KHRONOS_CSV_REPORT_PATH
            if directory_path:
                if os.path.isdir(directory_path) and os.access(directory_path, os.W_OK):
                    csv_data = [["S. No", "Test", ", Duration (in sec)"]]
                    for index, test_timing in enumerate(self.sorted_test_timings):
                        csv_data.append([str(index + 1), test_timing[0], str(test_timing[-1]["duration"])])
                    khronos_report_file_path = directory_path + "/khronos_report.csv"
                    with open(khronos_report_file_path, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(csv_data)
                    logger.info(f"khronos report is generated at {khronos_report_file_path}")

                else:
                    logger.info("The khronos_csv_report_path is invalid or isn't writable")

        except AttributeError:
            pass

    def create_khronos_gsheet_report(self):
        try:
            spreadsheet_id = settings.KHRONOS_SPREEDSHEET_REPORT_GSHEET_ID
            credentials_file_path = settings.KHRONOS_GSHEET_CREDS_FILE_PATH
            if os.path.isfile(credentials_file_path):
                gsheet_service = gspread.service_account(filename=credentials_file_path)
                gsheet = gsheet_service.open_by_key(key=spreadsheet_id)
                worksheet = gsheet.sheet1
                worksheet.clear()
                gsheet_data = [["S. No", "Test", "Duration (in sec)"]]
                for index, test_timing in enumerate(self.sorted_test_timings):
                    gsheet_data.append([str(index + 1), test_timing[0], str(test_timing[-1]["duration"])])

                worksheet.update("A:C", gsheet_data)
                logger.info("khronos gsheet report is generated.")

            else:
                logger.info(f"{credentials_file_path} is not a valid file path.")

        except AttributeError:
            pass

    def generate_khronos_reports(self):
        self.create_khronos_terminal_report()
        self.create_khronos_csv_report()
        self.create_khronos_gsheet_report()
