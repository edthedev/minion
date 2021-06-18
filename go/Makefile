
# https://github.com/trstringer/cli-debugging-cheatsheets/blob/master/go.md
#
build:
	go build minion.go

go:
	go run minion.go --list

todo:
	go run minion.go -todo

todoFile: 
	go run .\minion.go -todo -file test.md

debug:
	dlv debug -- --list

install_go:
	choco install golang

setup:
	go get -u github.com/derekparker/delve/cmd/dlv

libs:
	go get github.com/docopt/docopt-go

