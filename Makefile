image=music_server
version=0.0.1

requirements.txt: build
	@echo "updated image"

build:
	docker build -t $(image):$(version) .

run:
	docker run --rm -it \
		-p 5000:5000 \
		-v $(shell pwd)/data:/data \
		$(image):$(version)

dev: 
	docker run --rm -it \
		-p 5000:5000 \
		-w /web \
		-v $(shell pwd)/music:/app/static/music \
		-v $(shell pwd)/web:/web \
		$(image):$(version)


stop:
	docker stop $(shell cat container_id)
