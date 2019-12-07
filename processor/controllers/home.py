from flask import render_template, current_app as app, url_for
from processor.engine.utils.read_write_file import rw_xlsx
import os
from flask import request
import json


@app.route('/', methods=['get', 'post'])
def home():
    if request.method == 'POST':
        data = request.form
        print(data)
        chart_type = data.get("chartType")
        second_chart_type = data.get("secondChartType")
        pdf = data.get("PDF")
        year = data.get("Year")
        filter_images = get_image_filter_data(**dict(
            chart_type=chart_type,
            second_chart_type=second_chart_type,
            pdf=pdf,
            year=year
        ))
        print(len(filter_images))
        return json.dumps(filter_images)
        # return render_template('index.html', filter_images=filter_images)
    return render_template('index.html')


@app.route('/image/<string:file_name>', methods=['get', 'post'])
def image(file_name):
    return "Success {}".format(file_name)

def get_image_filter_data(**kwargs):
    print("Inside Function get_image_filter_data with kwargs :: {}".format(kwargs))
    data = get_excel_data()
    response = list()
    for row in data:
        if is_filtered_row(row, **kwargs):
            img_path = url_for('static', filename='data/ImageList/' + str(int(row[0])) + ".png")
            current_file_path = os.path.dirname(__file__)
            verify_img_path = os.path.join(current_file_path, ".." + img_path)
            if os.path.isfile(verify_img_path):
                response.append([row[0], img_path])
    return response


def get_excel_data():
    current_file_path = os.path.dirname(__file__)
    excel_abs_path = os.path.join(current_file_path, '..{}'.format(url_for(
        'static', filename="data/imageIndex.xlsx"
    )))
    print("excel path :: {}".format(excel_abs_path))
    excel = rw_xlsx(file_name=excel_abs_path)
    data = excel.read_from_xlsx()
    return data


def is_filtered_row(row, chart_type, second_chart_type, pdf, year):
    filtered = []
    ALL = "all"
    # Type of Chart
    if chart_type.upper() in [row[3].upper(), ALL.upper()]:
        filtered.append("chart_type")

    # Secondary Type Of Chart
    if second_chart_type.upper() in [row[4].upper(), ALL.upper()]:
        filtered.append("second_chart_type")

    # Source PDF
    if str(pdf) in [row[1], ALL]:
        filtered.append("pdf")

    # Year
    if year in [row[2], ALL]:
        filtered.append("year")

    for i in filtered:
        if not i:
            filtered = False
            break
    return True if len(filtered) == 4 else False


def map_return_values(row):
    mapping = {"chartType": 3, "secondChartType": 4, "PDF": 1, "Year": 2}
    return {k: row[v] for k, v in mapping.items()}


