import src.lambda_function
import json

with open("./event.json") as file:
    evjs = json.load(file)


src.lambda_function.lambda_handler(evjs, None)
