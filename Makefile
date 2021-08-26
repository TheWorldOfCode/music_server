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
		-v $(shell pwd)/config:/config \
		--user $(shell id -u):$(shell id -g) \
		$(image):$(version)

dev: 
	docker run --rm -it \
		-p 5000:5000 \
		-p 6601:6600 \
		-p 8001:8000 \
		-w /web \
		-v $(shell pwd)/data:/data \
		-v $(shell pwd)/config:/config \
		-v $(shell pwd)/web:/app \
		--user $(shell id -u):$(shell id -g) \
		$(image):$(version)


stop:
	docker stop $(shell cat container_id)
