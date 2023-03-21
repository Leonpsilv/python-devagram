from uvicorn import run

if __name__ == '__main__':
    run('Main:app', port=5000, reload=True)
