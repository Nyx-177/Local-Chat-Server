class log:
    def info(text):
        print(f'[{colorama.Fore.GREEN}INFO{colorama.Fore.RESET}] {text}')
    
    def warn(text):
        print(f'[{colorama.Fore.YELLOW}WARNING{colorama.Fore.RESET}] {text}')
    
    def error(text):
        print(f'[{colorama.Fore.RED}ERROR{colorama.Fore.RESET}] {text}')