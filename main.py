from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd
def load_model():
    encoder = joblib.load('encoder.joblib') 
    model_load = joblib.load('xgbmodel.joblib')
    return encoder,model_load
app = FastAPI()

#print(model_load)
class spesis_data(BaseModel):
    PRG: int
    PL: int 
    PR: int 
    SK: int 
    TS: int
    M11: float 
    BD2: float
    Age: int 
    Insurance: int
@app.get('/')

async def index():
    return("SEPSIS API: PREDICTION")
# def index():
#     return("This my First API")
@app.post('/predict')

def predict(spesis_data: spesis_data):
    data = {
        'PRG':spesis_data.PRG,
        'PL': spesis_data.PL,
        'PR': spesis_data.PR,
        'SK': spesis_data.SK,
        'TS': spesis_data.TS,
        'M11': spesis_data.M11,
        'BD2': spesis_data.BD2,
        'Age': spesis_data.Age,
        'Insurance': spesis_data.Insurance
    }
    df = pd.DataFrame(data,index=[0])

    # num_col =  [ 'PRG', 'PL', 'PR', 'SK', 'TS', 'M11', 'BD2', 'Age','Insurance']

    scaler,model = load_model()
     #
     # Scale numerical colums
    # scaled_col = scaler.transform(df[num_col])
    # df2 = pd.DataFrame(scaled_col)
    prediction = model.predict(df).tolist()
    if (prediction[0] == 1):
        result = "Positive Sepsis"
    else:
        result = "Negative Sepsis"
        return{"result":result}
    #return {'Prediction': prediction}
   


    # # data = pd.DataFrame([spesis_data.dist()]    )
    # predd = model_load.predict(data)

    # return {'Prediction':predd}


        

