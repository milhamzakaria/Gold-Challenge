#flask API, Swagger UI

from os import sep
import re
import pandas as pd
from flask import request, Flask, jsonify
app = Flask(__name__)
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from bantuan import *
from cleaning import process_csv, process_text

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )

swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }

swagger = Swagger(app, template=swagger_template, config=swagger_config)
@swag_from("D:/BINAR ZOOM/CHALLENGE/input/docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = { 
        'status_code':200, 
        'description':'challange binar', 
        'data': "cleansing data dan membuat API"
        }

    response_data = jsonify(json_response)
    return response_data

@swag_from("D:/BINAR ZOOM/CHALLENGE/input/docs/text_processing.yml", methods=['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')

    json_response = { 
        'status_code':200, 
        'description':'teks yang sudah diproses', 
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text, )
        }

    response_data = jsonify(json_response)
    return response_data

@swag_from("D:/BINAR ZOOM/CHALLENGE/input/docs/text_processing_file.yml", methods=['POST'])
@app.route('/text_processing_file', methods=['POST'])
def text_processing_file():
    """
    file: D:/BINAR ZOOM/CHALLENGE/input/docs/text_processing_file.yml
    """
    text = request.files.getlist('file')[0]

    # TODO : manfaatkan abusive_dict
    df_abusive = pd.read_csv("D:/BINAR ZOOM/CHALLENGE/input/data/abusive.csv")

    alay_dict = pd.read_csv("D:/BINAR ZOOM/CHALLENGE/input/data/new_kamusalay.csv", encoding ='iso-8859-1', header=None)
    alay_dict = alay_dict.rename(columns={0: 'original', 1: 'replacement'})

    # merubah bentuk dataframe menjadi bentuk dictionary
    alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))

    #merubah kata kata alay menjadi kata baku
    def normalize_alay(text):
        return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

    def preprocess(text):
        text = lowercase(text) # 1
        text = remove_unnecessary_char(text) # 2
        text = remove_nonaplhanumeric(text) # 3
        text = normalize_alay(text) # 4
        return text

    # original data
    df_new = pd.DataFrame()
    df = pd.read_csv(text, encoding ='latin-1')
    df_new['old_tweet'] = df['Tweet']

    # mengapplikasikan fugsi pre process
    df['Tweet'] = df['Tweet'].apply(preprocess)
    df_new['new_tweet'] = df['Tweet']

    df_new.to_csv('output_filename.csv', sep=';')

    json_response = { 
        'status_code':200, 
        'description':'teks yang sudah diproses', 
        'data': 'sukses'
        }

    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__':
    app.run()

