package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func calculate(a float64, op string, b float64) (float64, error) {
	switch op {
	case "+":
		return a + b, nil
	case "-":
		return a - b, nil
	case "*":
		return a * b, nil
	case "/":
		if b == 0 {
			return 0, errors.New("на ноль делить нельзя")
		}
		return a / b, nil
	}
	return 0, fmt.Errorf("неизвестная операция: %s", op)
}

func ask(r *bufio.Reader, prompt string) (string, bool) {
	fmt.Print(prompt)
	line, err := r.ReadString('\n')
	if err != nil && line == "" {
		return "", false
	}
	return strings.TrimSpace(line), true
}

func parseNumber(s string) (float64, error) {
	return strconv.ParseFloat(strings.ReplaceAll(s, ",", "."), 64)
}

func main() {
	setupConsole()
	r := bufio.NewReader(os.Stdin)
	fmt.Println("Калькулятор. Операции: + - * /")
	fmt.Println("Для выхода введите q")
	for {
		first, ok := ask(r, "\nПервое число: ")
		if !ok || strings.EqualFold(first, "q") {
			return
		}
		op, ok := ask(r, "Операция (+ - * /): ")
		if !ok {
			return
		}
		second, ok := ask(r, "Второе число: ")
		if !ok {
			return
		}
		a, err1 := parseNumber(first)
		b, err2 := parseNumber(second)
		if err1 != nil || err2 != nil {
			fmt.Println("Ошибка: нужно ввести число")
			continue
		}
		res, err := calculate(a, op, b)
		if err != nil {
			fmt.Println("Ошибка:", err)
			continue
		}
		fmt.Println("Результат:", strconv.FormatFloat(res, 'f', -1, 64))
	}
}
