
import uvicorn

if __name__ == '__main__':
    print(f'uvicorn run...')
    #config = uvicorn.Config('fake_webserver:app', port=5000, log_level='info')
    config = uvicorn.Config('fake_webserver:app', host='0.0.0.0', port=5555, log_level='info')
    server = uvicorn.Server(config)
    server.run()

