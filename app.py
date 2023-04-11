from flask import Flask, request, render_template, redirect, url_for, Markup, session
import pandas as pd
from src.eln import update_data

from src.scifinder import get_data


app = Flask(__name__, template_folder='src/templates',
            static_folder='src/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploaded_data/', methods=['POST'])
def handle_upload():
    file = request.files['fileInput']

    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return render_template('index.html', alert_message='File type not supported')

    
    return render_template('display.html',df = df.to_html(), search_enabled=True)


@app.route('/search/search_api/results', methods=['POST'])
def search_function():
    df_html = pd.read_html(request.form['df'])
    df = df_html[0]
    df.drop('Unnamed: 0', axis=1, inplace=True)
    source = request.form['source']

    # getdata from scifinder api
    data = get_data(df, source=source)


    return render_template('display.html', df=data.to_html(), search_enabled=False)


@app.route('/update', methods=['POST'])
def update_function():
    updated_df = pd.read_html(request.form['df'])[0]
    updated_df.drop('Unnamed: 0', axis=1, inplace=True)

    # call function to update data into eln
    var = update_data(dataframe=updated_df)
    if var == 'true':
        return render_template('modal.html', message='Data uploaded successfully', redirect_url=url_for('index'))
    else:
        return render_template('display.html', df=updated_df.to_html(), search_enabled=False)


if __name__ == '__main__':
    app.run(debug=True)
