.PHONY: kill build down

# include .env
export 
# DOCKER_PROJECT = ${PROJECT_NAME}
DOCKER_PROJECT = 'Collectibles Corner'

build:
	docker compose down && docker compose up --build

down:
	docker compose down

populate:
	curl -v http://localhost:5000/initdb && curl -v http://localhost:5000/init_mock_data/demo

remove_images:
	docker rmi $(shell docker images -a -q)

remove_volumes:
	docker volume rm $(shell docker volume ls -q)

kill:
	docker compose kill
