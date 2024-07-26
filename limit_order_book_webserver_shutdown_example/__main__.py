
import uvicorn

if __name__ == '__main__':
    print(f'uvicorn run...')
    config = uvicorn.Config('limit_order_book_webserver_shutdown_example:app', host='0.0.0.0', port=5555, log_level='debug', proxy_headers=True)
    server = uvicorn.Server(config)
    server.run()

