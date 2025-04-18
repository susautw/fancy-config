all: chdir
	python setup.py sdist bdist_wheel

chdir:
	cd $(WORKING_DIR)

clean:
	rm -rf ./build
	rm -rf ./dist

upload_test: clean all
	twine upload --repository testpypi dist/*.whl

upload: clean all
	twine upload dist/*.whl

test:
	PYTHONPATH=src pytest tests 