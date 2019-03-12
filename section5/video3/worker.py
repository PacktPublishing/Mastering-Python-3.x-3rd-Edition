def main():
    while True:
        num = int(input())
        print(num ** 2, flush = True)
        if num < 0:
            return

if __name__ == '__main__':
    main()
