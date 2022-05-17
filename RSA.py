import random
import base64
import sys
#key generate
# p q = prime(large)
# n=p*q phi_n=(p-1)*(q-1)
# e=public_key d=private_key
#key size=1024 bit=512
def key_gen(bit_count):
    p = generate_pnum(int(bit_count/2))
    q = generate_pnum(int(bit_count/2))
    n = p * q
    phi_n = (p-1)*(q-1)
    public_key = random.randint(2,phi_n)
    if public_key % 2 == 0:
        public_key += 1
    while not is_coprime(public_key,phi_n):
        public_key = random.randint(2,phi_n)
    private_key = mod_inverse(public_key,phi_n)

    print("p = {}".format(p))
    print("q = {}".format(q))
    print("n = {}".format(n))
    print("phi = {}".format(phi_n))
    print("e = {}".format(public_key))
    print("d = {}".format(private_key))
    return

#create a large prime num
def generate_pnum(bits):
    pnum = random.randint( 2**(bits-1)+1, 2**bits-1 )
    if(pnum%2==0):
        pnum +=1
    
    while(miller_rabin(pnum,20) == False):
        pnum +=2
    
    return pnum
#miller rabin演算法
#快速判斷是否為質數
def miller_rabin(check_num ,times):   
    if check_num == 2 or check_num == 3:
        return True    
    if check_num == 1 or check_num < 0 or check_num % 2 == 0:
        return False
    r = 0
    s = check_num-1
    while(s%2==0):
        r += 1
        s //=2
    for i in range(times):
        a = random.randrange(2,check_num-1)
        x = pow(a,s,check_num)
        if(x==1 or x == check_num-1):
            continue
        for j in range(r-1):
            x = pow(x,2,check_num)
            if(x==check_num-1):
                break
        else:
            return False
    return True
#輾轉相除
def gcd(a,b):
    if b <= 1 or b >= a:
        return -1

    while b != 0:
        a, b = b, a % b
    return a

#a b 是否互質(gcd==1)
def is_coprime(a, b):
    if a >= b:
        return gcd(a, b) == 1
    else:
        return gcd(b, a) == 1

def mod_inverse(a, m):
    #python 3.8 up 直接 pow(x,-1,y)
    if sys.version_info[0] > 3:
        return pow(a,-1,m)
    elif sys.version_info[0] == 3 and sys.version_info[1] >= 8:
        return pow(a,-1,m)
    else: 
    #phi =m public_key=a
     d_old = 0; r_old = m
     d_new = 1; r_new = a
     while r_new > 0:
        x = r_old // r_new
        (d_old, d_new) = (d_new, d_old - x * d_new)
        (r_old, r_new) = (r_new, r_old - x * r_new)
     return d_old % m if r_old == 1 else None

#採用sqare and multiply algorithm加速
def square_multiply(base, exponent, mod_num): 
    bins = bin(exponent)
    result = 1
    for index in range(0,len(bins)):
        result = (result * result) % mod_num
        if bins[index] == '1':
            result = (result * base) % mod_num
    return result
#insert plain_text n public_key
#RSA加密後的數字透過base64 decode顯示
def encrypt(plain_text,n,public_key):
    plain_num = str_to_num(plain_text)
    #文字轉數字後處理
    cipher_num = square_multiply(plain_num,public_key,n)
    cipher_base64 = base64.b64encode(str(cipher_num).encode('ascii'))
    cipher_text = cipher_base64.decode('ascii')
    return cipher_text




#decrypt insert cipher_text n d
#解密出數字後，將數字轉回原始訊息
def decrypt(cipher_text,n,private_key):
    cipher_num = int(base64.b64decode(cipher_text).decode('ascii'))
    plain_num = square_multiply(cipher_num,private_key,n)
    print(plain_num)
    plain_text = num_to_str(plain_num)
    return plain_text


#CRT speed up! cipher_text & input p q d
def CRT_dec(cipher_text,p,q,d):
    cipher_num = int(base64.b64decode(cipher_text).decode('ascii'))
    dp = d % (p-1)
    dq = d % (q-1)
    q_inv = mod_inverse(q,p)
    m1 = square_multiply(cipher_num,dp,p)
    m2 = square_multiply(cipher_num,dq,q)
    h = q_inv * (m1-m2) % p
    result = m2 + h * q
    print(result)
    plain_text = num_to_str(result)
    return plain_text


#python內建encode函式
def str_to_num(input):
    m_bytes = input.encode('utf-8')
    m_num = int.from_bytes(m_bytes, 'little')
    return m_num

#python內建decode函式
def num_to_str(input):
    m_bytes = input.to_bytes((input.bit_length() + 7) // 8, 'little')
    m_str = m_bytes.decode('utf-8')
    return m_str




# use argv argc to control input
def main():
    argc = len(sys.argv)
    try:
        if argc < 2:
            raise IndexError
        if sys.argv[1] == '-i':
            key_gen(1024)
        elif sys.argv[1] == '-e':
            if argc != 5:
                raise IndexError
            cipher_text = encrypt(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
            print(cipher_text)
        elif sys.argv[1] == '-d':
            if argc != 5:
                raise IndexError            
            plain_text = decrypt(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
            print(plain_text)
        elif sys.argv[1] == '-CRT':
            if argc != 6:
                raise IndexError
            plain_text = CRT_dec(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
            print(plain_text)
    except IndexError:
        print('argv error!')
    return

if __name__ == "__main__":
    main()