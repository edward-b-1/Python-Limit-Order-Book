
import uvicorn

if __name__ == '__main__':
    print(f'uvicorn run...')
    config = uvicorn.Config('limit_order_book_webserver:app', port=5000, log_level='info')
    server = uvicorn.Server(config)
    server.run()

