class log:
    def info(text):
        import colorama
        print(f'[{colorama.Fore.GREEN}INFO{colorama.Fore.RESET}] {text}')
    
    def warn(text):
        import colorama
        print(f'[{colorama.Fore.YELLOW}WARNING{colorama.Fore.RESET}] {text}')
    
    def error(text):
        import colorama
        print(f'[{colorama.Fore.RED}ERROR{colorama.Fore.RESET}] {text}')