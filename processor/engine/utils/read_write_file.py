import csv
import itertools
import os
import zipfile

import xlrd
import xlwt
from xlutils.copy import copy


class rw_csv:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_from_csv(self):
        if self.file_name is None:
            self.file_name = "output.csv"
        results = []
        with open(self.file_name, "rU") as File:
            reader = csv.DictReader(File)
            for row in reader:
                results.append(row)
        return results

    def write_in_csv(self, fieldnames, data, header=False):
        with open(self.file_name, 'a') as File:
            writer = csv.DictWriter(File, fieldnames=fieldnames)
            file_is_empty = os.stat(self.file_name).st_size == 0
            if header is True and file_is_empty:
                writer.writeheader()

            """
                for i in data:
                    temp_data = dict(itertools.izip(fieldnames, i))
                    print temp_data
                    writer.writerow(temp_data)
            """
            writer.writerow(dict(itertools.izip(fieldnames, data)))
        return dict(response='OK')


class rw_xlsx:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_from_xlsx(self, start=None, end=None, headers=False):
        rows = []
        workbook = xlrd.open_workbook(self.file_name, "rb")
        sheet = workbook.sheet_by_index(0)

        for rowx in range(sheet.nrows):
            rows.append(sheet.row_values(rowx, start_colx=start, end_colx=end))

        return rows if headers else rows[1: ]

    def write_in_xlsx(self, data, header=False):
        r = 0
        if os.path.isfile(self.file_name):
            rb = xlrd.open_workbook(self.file_name)
            sheet = rb.sheet_by_index(0)
            r = sheet.nrows
            workbook = copy(rb)
            sheet = workbook.get_sheet("Test")
            if header is True:
                return dict(header=True)
        else:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('Test')

        # for num in range(len(data)):
        for column, heading in enumerate(data):
            sheet.write(r, column, heading)
        workbook.save(self.file_name)

        return dict(respone=True)


class rw_zip:
    def write_in_zip(self, path, zipFileName):
        """ziph is zipfile handle"""
        if os.path.isfile(zipFileName):
            zipf = zipfile.ZipFile(zipFileName, 'a', zipfile.ZIP_DEFLATED)
        else:
            zipf = zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)

            if os.path.isfile(path):
                # return "PROVIDE-VLAID-PATH"
                zipf.write(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        zipf.write(os.path.join(root, file))
            zipf.close()
            return dict(response=True)


"""
data = []
data.append(["Date", "InvoieType", "TaxInvoicePrefix", "CustomerName", "DBInvoice"",DBcutomer"])

rw_xlsx("output.xlsx").write_in_xlsx(data)
rw_csv("output.csv").write_in_csv(fieldnames=["a", "b", "c", "d", "e", "f"], data=data[0], header=True)
rw_zip().write_in_zip("output.xlsx", "python.zip")
rw_zip().write_in_zip("output.csv", "python.zip")

"""
