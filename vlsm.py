def spec_ip_addr_checker(address):
    spec_addr_list = {"127.0.0.1":"localhost"}
    for addr in spec_addr_list:
        if addr == address: return spec_addr_list.get(addr)
def class_checker(split_int_addr):
    if split_int_addr[0] <= 127: return "A"
    elif 128 <= split_int_addr[0] <= 191: return "B"
    elif 192 <= split_int_addr[0] <= 223: return "C"
    elif 224 <= split_int_addr[0] <= 239: return "D - Muticast"
    elif 240 <= split_int_addr[0] <= 255: return "E - Experimental purpose"
def private_class_checker(split_int_addr):
    if 10 <= split_int_addr[0] <= 11: return "A"
    elif split_int_addr[0] == 172 and 16 <= split_int_addr[1] <= 32: return "B"
    elif split_int_addr[0] == 192 and 168 <= split_int_addr[1] <= 169: return "C"

def ip_addr_validation():
    while True:
        address = raw_input("Input IP address in dot-decimal notation:\n") or "192.168.10.44"
        splitted_address = address.split(".")
        #Check if there are other chars that required
        try:
            split_int_addr = map(int, splitted_address)
        except ValueError:
                print "Required input type is dot-decimal notation"
                break
        #Look for not proper values in ip address.
        errors = []
        if len(split_int_addr) == 4:
            for  octet in split_int_addr:
                if  0 > octet or octet > 255:
                    errors.append(octet)
        else:
            print "Wrong number of octets(got {})".format(len(split_int_addr))
            break
        if errors:
            for i in errors: print "{} is not proper octet value (should be 1-255)".format(i)
            break
        #Check for the specific IP addresses
        address_class = private_class_checker(split_int_addr)
        spec_ip = spec_ip_addr_checker(address)
        if spec_ip == None: spec_ip = ""
        if address_class == None:
            is_private = False
            address_class = class_checker(split_int_addr)
        else:
            is_private = True
        return split_int_addr, address_class, spec_ip, is_private



def mask_validation(address_class):
    while True:
        possible_masks = (0, 128, 192, 224, 240, 248, 252, 255)
        mask = raw_input("Input mask in dot-decimal notation:\n") or "255.255.255.248"
        native_masks = {'A': ("255.0.0.0", 8),'B': ("255.255.0.0", 16),'C': ("255.255.255.0", 24)}
        #Check if there are other chars that required
        splitted_mask = mask.split(".")
        try:
            split_int_mask = map(int, splitted_mask)
        except ValueError:
                print "Required input type is dot-decimal notation"
                break

        if len(split_int_mask) != 4:
            print "Wrong number of octets(got {})".format(len(split_int_mask))
            break
        if address_class == "A" and (split_int_mask[0] != 255 or split_int_mask[1] not in possible_masks or split_int_mask[2] not in possible_masks) or split_int_mask[3] not in possible_masks:
            print "This is wrong mask for A class network."
            break
        if address_class == "B" and (split_int_mask[0] != 255 or split_int_mask[1] != 255 or split_int_mask[2] not in possible_masks or split_int_mask[3] not in possible_masks):
            print "This is wrong mask for B class network."
            break
        if address_class == "C" and (split_int_mask[0] != 255 or split_int_mask[1] != 255 or split_int_mask[2] != 255 or split_int_mask[3] not in possible_masks):
            print "This is wrong mask for C class network."
            break
        return split_int_mask

def to_bin(dot_decimal):
    binary = []
    for octet in dot_decimal:
        new_octet = bin(octet).replace("0b", "")
        binary.append((8 - len(new_octet)) * "0"+ new_octet)
    return  binary


def bin_and(addr, mask):
    addr_and_mask = []
    for y, octet in enumerate(addr):
        new_octet = ""
        for x, octet in enumerate(addr[y]):
            new_octet = new_octet + str(int(addr[y][x]) * int(mask[y][x]))
        addr_and_mask.append(new_octet)
    return addr_and_mask

def hosts_places(addr_and_mask):
    num_of_zeros = 32 - "".join(addr_and_mask).rfind("1") - 1
    return num_of_zeros


while True:
    split_int_addr, address_class, spec_ip, is_private = ip_addr_validation()
    print "Class " + address_class + " address."
    if spec_ip != "": print "This is special purpose " + spec_ip + "address."
    if is_private == True: print "Private adresses space."
    split_int_mask = mask_validation(address_class)
    bin_mask =  to_bin(split_int_mask)
    bin_addr =  to_bin(split_int_addr)
    # print bin_mask, bin_addr
    # print bin_and(bin_mask, bin_addr)
    print "There are " + str((2**(hosts_places(bin_and(bin_mask, bin_addr))))-2) + " legal hosts."
