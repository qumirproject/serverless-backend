import src.lambda_function
import json

with open("./event.json") as file:
    evjs = json.load(file)


rtobj = src.lambda_function.lambda_handler(evjs, None)

print(json.dumps(rtobj,indent=4))