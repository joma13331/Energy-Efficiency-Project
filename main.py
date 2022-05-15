import os
import shutil
from wsgiref import simple_server
from flask import Flask, render_template, request, url_for
from flask_cors import cross_origin, CORS
from Training.EEDataInjestionCompTrain import EEDataInjestionCompTrain
from Training.EEModelDevelopment import EETrainingPipeline
from Prediction.EEPredictionPipeline import EEPredictionPipeline
from Prediction.EEDataInjestionCompPred import EEDataInjestionCompPred

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def ee_home_page():
    img_url = url_for('static', filename='ineuron-logo.webp')
    return render_template('index.html', image_url=img_url)


@app.route("/train", methods=["POST"])
@cross_origin()
def ee_train_route():
    img_url = url_for('static', filename='ineuron-logo.webp')
    try:

        if request.form is not None:

            file_item = request.files["train_dataset"]
            if file_item.filename:
                file_name = "ENB2022_data.xlsx"

                if os.path.isdir("Uploaded_Files"):
                    shutil.rmtree("Uploaded_Files")
                    os.mkdir("Uploaded_Files")
                else:
                    os.mkdir("Uploaded_Files")

                with open(os.path.join("Uploaded_Files", file_name), 'wb') as f:
                    f.write(file_item.read())

                train_validation_obj = EEDataInjestionCompTrain(path="Uploaded_Files")
                train_validation_obj.ee_data_injestion_complete()

                if os.path.isdir("Models"):
                    shutil.rmtree("Models")
                    os.mkdir("Models")
                else:
                    os.mkdir("Models")

                training_pipeline = EETrainingPipeline()
                training_pipeline.ee_model_train()
            else:
                message = "No records Found\n TRY AGAIN"
                return render_template("predict.html", message=message, image_url=img_url)

    except ValueError as e:
        return render_template('train.html', message=f"ERROR: {str(e)}\n TRY AGAIN", image_url=img_url)

    except KeyError as e:
        return render_template('train.html', message=f"ERROR: {str(e)}\n TRY AGAIN", image_url=img_url)

    except Exception as e:
        return render_template('train.html', message=f"ERROR: {str(e)}\n TRY AGAIN", image_url=img_url)

    return render_template('train.html', message="Training Successful", image_url=img_url)


@app.route('/prediction', methods=["POST"])
@cross_origin()
def ee_prediction_route():
    img_url = url_for('static', filename='ineuron-logo.webp')
    try:

        if request.form is not None:

            file_item = request.files['dataset']
            if file_item.filename:
                file_name = "ENB2022_data.xlsx"

                if os.path.isdir("Uploaded_Files"):
                    print()
                    shutil.rmtree("Uploaded_Files")
                    os.mkdir("Uploaded_Files")
                else:
                    os.mkdir("Uploaded_Files")

                with open(os.path.join("Uploaded_Files", file_name), 'wb') as f:
                    f.write(file_item.read())

                pred_injestion = EEDataInjestionCompPred(path="Uploaded_Files")
                pred_injestion.ee_data_injestion_complete()

                pred_pipeline = EEPredictionPipeline()
                result = pred_pipeline.ee_predict()

                return render_template("predict.html", records=result, image_url=img_url)
            else:
                message = "Using Default Prediction Dataset"

                pred_injestion = EEDataInjestionCompPred(path="PredDatasets")
                pred_injestion.ee_data_injestion_complete()

                pred_pipeline = EEPredictionPipeline()
                result = pred_pipeline.ee_predict()

                return render_template("predict.html", message=message, records=result, image_url=img_url)

    except ValueError as e:
        message = f"Value Error: {str(e)}\n TRY AGAIN"
        return render_template("predict.html", message=message, image_url=img_url)
    except KeyError as e:
        message = f"KeyError: {str(e)}\n TRY AGAIN"
        return render_template("predict.html", message=message, image_url=img_url)
    except Exception as e:
        message = f"Error: {str(e)}\n TRY AGAIN"
        return render_template("predict.html", message=message, image_url=img_url)


@app.route("/logs", methods=["POST"])
@cross_origin()
def ee_get_logs():
    img_url = url_for('static', filename='ineuron-logo.webp')
    try:
        if request.form is not None:
            log_type = request.form['log_type']

            with open(os.path.join("EElogging/", log_type), "r") as f:
                logs = f.readlines()
            return render_template("logs.html", heading=log_type.split("/")[1], logs=logs, image_url=img_url)
        else:
            message = "No logs found"
            return render_template("logs.html", message=message, image_url=img_url)

    except Exception as e:
        message = f"Error: {str(e)}"
        return render_template("logs.html", heading=message, image_url=img_url)


port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
