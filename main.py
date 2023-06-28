from website import create_app
#flask --app main.py --debug run --port 8888
#python main.py --debug run --host=192.168.1.XXX --port=8888
#flask --app main.py --debug run --host=192.168.238.67 --port=8888
#python -m flask --app main.py --debug run --host=192.168.5.84 --port=8888
# SELECT name FROM sqlite_master WHERE type='table';
app = create_app()


if __name__=='__main__':
	app.run(debug=True,host='192.168.5.84',port=8888)