package main

import (
	"reflect"
	"testing"
)

func TestGetLatest(t *testing.T) {
	var input string = "|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15"
	expected := []string{"11", "12", "13", "14", "15"}

	result := GetLatest(input, 5)

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("got %q, wanted %q", result, expected)
	}
}

func TestGetLatestShort(t *testing.T) {
	var input string = "|1|2|3|4|5"
	expected := []string{"", "1", "2", "3", "4", "5"}

	result := GetLatest(input, 10)

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("got %q, wanted %q", result, expected)
	}
}
