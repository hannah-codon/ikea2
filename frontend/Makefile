include .env
export $(shell sed -n 's/=.*//p' .env)
SHELL := /bin/bash
VERSION := $(shell jq -r .version package.json)

run: 
	npm run dev -- --port ${PORT}

preview:
	npm run build && node api.js

install-dependencies: 
	source .env && export CCL_NPM_TOKEN && npm install