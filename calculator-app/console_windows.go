package main

import "syscall"

// Включает UTF-8 в консоли Windows, чтобы русский текст отображался правильно.
func setupConsole() {
	k := syscall.NewLazyDLL("kernel32.dll")
	k.NewProc("SetConsoleOutputCP").Call(65001)
	k.NewProc("SetConsoleCP").Call(65001)
}
