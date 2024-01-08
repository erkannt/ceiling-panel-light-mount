.PHONY = dev

current_dir = $(shell pwd)

dev:
	docker run -p 8080:5000 -v $(current_dir)/:/data cadquery/cadquery-server run
