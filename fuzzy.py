import itertools
import numpy as np

kelembaban_param = ["cukup lembab", "lembab","sangat lembab"]
dk_kelembaban = [1, 250, 450, 650, 980, 1024]

temp_param = ["sangat dingin","dingin","hangat","panas"]
dk_temp = [-10, -5, 10, 15, 22, 25, 30, 40]

inp_kelembaban = 360
inp_temperatur   = 20

# Mencari nilai tengah dari interval bawah dan atas
def findCenter(nilai):
    c = []
    count = 0
    center = 0
    idx = 1
    while idx <= len(nilai)-1:
        if count == 2:        
            center = center / 2
            c.append(center)
            count = 0
            center = 0                       
        else:
            center += nilai[idx]                         
            count += 1
            idx += 1                
    return c

c_kelembaban = findCenter(dk_kelembaban)
c_temp = findCenter(dk_temp)

# Fuzzification
def fuzzification(center, dk, input, param):
    idx = 0
    dic = {}    
    for i in range(len(center)):
        batas_kiri = 0
        batas_kanan = 0    
        fuzzi_1 = 0
        fuzzi_2 = 0    
        for j in range(2):
            idx+=1                
        batas_kiri = dk[idx-1]
        batas_kanan = dk[idx]

        if input < batas_kiri:            
            kiri = (idx/2)-1            
            dic.update({param[int(kiri)]: 1})           
            return dic
            break

        if input >= batas_kanan and input <= dk[idx+1]:                                            
            kiri = (idx/2)                            
            dic.update({param[int(kiri)]: 1})
            return dic
            break     
        
        if input > batas_kiri and input > batas_kanan:
            continue
        else:
            fuzzi_1 = (batas_kanan - input) / (batas_kanan - batas_kiri)        
            fuzzi_2 = (input - batas_kiri) / (batas_kanan - batas_kiri)                  
            
            kanan = idx/2
            kiri = (idx/2)-1            

            if input > center[i]:
                dic.update({param[int(kanan)]: fuzzi_2})
                dic.update({param[int(kiri)]: fuzzi_1})
            else:
                dic.update({param[int(kanan)]: fuzzi_1})
                dic.update({param[int(kiri)]: fuzzi_2})
            return dic
            break  
                    
def getKeyVal(mydict):
    key = []
    val = []
    for k,v in mydict.items():
        key.append(k)
        val.append(v)
    return key,val

#Rules
def rules(inp1, inp2):
    out = ""
    if inp1 == "cukup lembab" and inp2 == "sangat dingin":
        out = "cukup lama"
    elif inp1 == "cukup lembab" and inp2 == "dingin":
        out = "cukup lama"
    elif inp1 == "cukup lembab" and inp2 == "hangat":
        out = "lama"
    elif inp1 == "cukup lembab" and inp2 == "panas":
        out = "lama"
    elif inp1 == "lembab" and inp2 == "sangat dingin":
        out = "sebentar"
    elif inp1 == "lembab" and inp2 == "dingin":
        out = "sebentar"
    elif inp1 == "lembab" and inp2 == "hangat":
        out = "sebentar"
    elif inp1 == "lembab" and inp2 == "panas":
        out = "cukup lama"
    elif inp1 == "sangat lembab" and inp2 == "sangat dingin":
        out = "sebentar"
    elif inp1 == "sangat lembab" and inp2 == "dingin":
        out = "sebentar"
    elif inp1 == "sangat lembab" and inp2 == "hangat":
        out = "sebentar"
    elif inp1 == "sangat lembab" and inp2 == "panas":
        out = "sebentar"
    
    return out

dic_kelembaban = fuzzification(c_kelembaban, dk_kelembaban, inp_kelembaban, kelembaban_param) 
dic_temp = fuzzification(c_temp, dk_temp, inp_temperatur, temp_param)

kelembabankey, kelembabanval = getKeyVal(dic_kelembaban)
tempkey, tempval = getKeyVal(dic_temp)

key = []
for x in itertools.product(kelembabankey, tempkey):
    key.append(rules(x[0],x[1]))

val = []
for x in itertools.product(kelembabanval, tempval):
    val.append(np.min(x))

print(key)
max_data = {}
for i in range(len(key)):
    for j in range(len(val)):
        if key[i] == key[j]:
            if max_data.get(key[i]) != None and val[i] > max_data.get(key[i]):
                max_data.update({key[i]: val[i]})
            else:
                max_data.update({key[i]: val[i]})

# Defuzzifikasi
defuzzy = []
y = []
for k,v in max_data.items():
    y.append(v)
    if k == "sebentar":
        tmp = (25 - (v*15))
        # print(25, "-",v,"*15 = ", tmp)
        defuzzy.append(tmp)
    elif k == "cukup lama":
        tmp = (10 + (v*15))
        # print(10, "+",v,"*15=", tmp)
        defuzzy.append(tmp)
    elif k == "lama":
        tmp = (30 + (v*20))
        # print(30, "+",v,"*20=", tmp)
        defuzzy.append(tmp)

sum_nilai = 0
sum_y = 0
for i in range(len(defuzzy)):
    sum_nilai += (defuzzy[i]*y[i])
    sum_y += y[i]

print("=============== FUZIFIKASI ===============")
print(dic_kelembaban)
print(dic_temp)
print("==========================================\n")

print("============= DEFUZZIFIKASI ============")
defuzifikasi = sum_nilai/sum_y
print("Durasi Penyiraman rumput dengan kelembaban",inp_kelembaban,"pH & suhu", inp_temperatur,"celcius adalah",defuzifikasi,"menit")
print("========================================\n")
