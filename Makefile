

install: vspypatcher.py
	mkdir -p /opt/vspypatcher
	cp vspypatcher.py /opt/vspypatcher/
	chmod +x /opt/vspypatcher/vspypatcher.py
	ln -sf /opt/vspypatcher/vspypatcher.py /usr/local/bin/vspypatcher

requirements: requirements.txt
	python2 -m pip install -r requirements.txt
