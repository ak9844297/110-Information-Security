import sys
import numpy as np



#數字正向左
def caesar(ciphertxt, key):
    output = ""
    try:
        ikey = int(key) % 26
    except Exception as e:
        raise SystemExit("key 無法使用 請確認是否為int") from e
    ciphertxt = ciphertxt.replace(" ", "").upper()
    for i in ciphertxt:
        if i.isalpha():
            num = ord(i)
            num = num - ikey
            if num > ord('Z'):
                    num = num - 26
            elif num < ord('A'):
                    num = num + 26

            output = output + chr(num)
        else:
            output = output + i
    output=output.lower()
    print(output)


def playfair(ciphertxt, key):
    #移除空格檢查密文
    ciphertxt = ciphertxt.replace(" ", "").upper()
    for x in ciphertxt:
        if not x.isalpha():
            raise SystemExit("請檢察輸入是否都為字母")
    #key table
    for x in key:
        if not x.isalpha():
            raise SystemExit("請檢察key是否都為字母")
    A_Z = ''.join(chr(x) for x in range(65, 91))
    tmp = key.replace(" ", "").upper()+A_Z
    keytable = ''
    for x in tmp:
        if not x in keytable and x.isalpha():
            keytable = keytable+x
    #沒有J
    keytable = keytable.replace("J", "")

    output = ""
    for pre in range(0, len(ciphertxt), 2):
        #前一個字母和後一個字母
        preindex = keytable.index(ciphertxt[pre])
        postindex = keytable.index(ciphertxt[pre+1])
        preRow, preCol = int(preIndex/5), preIndex % 5
        postRow, postCol = int(postIndex/5), postIndex % 5

        # 橫列相同往左移
        if postRow == preRow:

            if preCol == 0:
                preCol = 4
            else:
                preCol = preCol - 1
            if postCol == 0:
                postCol = 4
            else:
                postCol = postCol - 1

        # 直行相同往上移
        elif postCol == preCol:
            if preRow == 0:
                preRow = 4
            else:
                preRow = preRow - 1
            if postRow == 0:
                postRow = 4
            else:
                postRow = postRow - 1
        # 四角形
        else:
            tmp = preCol
            preCol = postCol
            postCol = tmp

        output = output + keytable[preRow*5 + preCol]
        output = output + keytable[postRow*5 + postCol]
    output=output.lower()
    print(output)


def vernam(ciphertxt, key):
    #autokey 
    ciphertxt = ciphertxt.replace(" ", "").upper()
    if len(key) < len(ciphertxt):
        autokey = key + ciphertxt[0:len(ciphertxt)-len(key)]

    output = ""
    for i in range(0, len(ciphertxt)):
        # xor 
        tmp = ((ord(autokey[i])-ord('A')) ^
               (ord(ciphertxt[i])-ord('A'))) + ord('A')
        output = output + chr(tmp)
    output=output.lower()
    print(output)


def railfence(ciphertxt, key):
    ciphertxt = ciphertxt.replace(" ", "").upper()
    if key.isdigit():
        key = int(key)
    else:
        raise SystemExit("key 無法使用 請確認是否為int")
 
    # create the matrix to cipher
    #rail[key][text]
    rail = [['\n' for i in range(len(ciphertxt))]
                  for j in range(key)]
  
    dir_down = None
    row, col = 0, 0
     
    # mark the places with '*'
    for i in range(len(ciphertxt)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
         
        
        rail[row][col] = '*'
        col += 1
         
        # 下一列
        if dir_down:
            row += 1
        else:
            row -= 1           
    # fill the rail matrix
    index = 0
    for i in range(key):
        for j in range(len(ciphertxt)):
            if ((rail[i][j] == '*') and
               (index < len(ciphertxt))):
                rail[i][j] = ciphertxt[index]
                index += 1
         
    result = []
    row, col = 0, 0
    for i in range(len(ciphertxt)):
         
        # 方向
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False          
        # 確認位置
        if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1          

        if dir_down:
            row += 1
        else:
            row -= 1
    output="".join(result)
    output=output.lower()
    print(output)


def row(ciphertxt, key):
    key=key.replace(" ","")
    # preprocess
    ciphertxt = ciphertxt.replace(" ", "").upper()
    chrNum = int(len(ciphertxt)/len(key))
    rem = (len(ciphertxt) % len(key))
    # print(chrNum)

    splitTxt = {}
    splitCount = 0
    sort_key = ''.join(sorted(key))
    for i in range(0, len(key)):
        # 餘數以下的key多一個字母
        if key.index(sort_key[i]) < rem :
            moreNum = 1
        else:
            moreNum = 0
        splitTxt[sort_key[i]] = ciphertxt[splitCount:splitCount+chrNum+moreNum]
        splitCount = splitCount + chrNum+moreNum
    print(splitTxt)

    output = ''
 
    for num in range(0, chrNum+1):
        for i in key:
            tmp = splitTxt[i]
            if num < len(tmp):
                output = output + tmp[num]
    #一個一個元素放入
    output=output.lower()
    print(output)



try:

    print("嘗試解密...")
    mindex = sys.argv[1:].index('-m')
    iindex = sys.argv[1:].index('-i')
    kindex = sys.argv[1:].index('-k')
    
except Exception as e:
    raise SystemExit(f"Usage: {sys.argv[0]} -m method -i ciphertxt -k key, 請檢察指令...") from e
#有可能 text 有空格
method = sys.argv[mindex+2]
ciphertxt = ' '.join(sys.argv[iindex+2:kindex+1])
key = ' '.join(sys.argv[kindex+2:])


if method != 'caesar' and method != 'playfair' and method != 'vernam' and method != 'railfence' and method != 'row':
    raise SystemExit("無此算法 不可使用...")

globals()[method](ciphertxt, key)
