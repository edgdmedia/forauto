from uvicorn import run

from fortauto.settings import DEBUG

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   run("fortauto:app", reload=True, workers=4, debug=DEBUG)
