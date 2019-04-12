import csv

from xlrd import open_workbook

def main():
    workbook = open_workbook("data/ccs/CCS_data.xlsx")
    sheet = workbook.sheet_by_index(0)

    data = [["course_id", "ccs_score"],]
    for row in range(1, sheet.nrows):
        data.append([int(sheet.cell_value(row, 1)), int(sheet.cell_value(row, 7))])

    with open("data/ccs/ccs.csv", "w") as output_f:
        writer = csv.writer(output_f)
        writer.writerows(data)

if __name__ == "__main__":
    main()
