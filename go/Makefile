
go:
	go run minion.go --list

debug:
	# https://github.com/trstringer/cli-debugging-cheatsheets/blob/master/go.md
	dlv debug -- --list

install_go:
	choco install golang

setup:
	go get -u github.com/derekparker/delve/cmd/dlv

libs:
	go get github.com/docopt/docopt-go

build:
	go build minion.go

