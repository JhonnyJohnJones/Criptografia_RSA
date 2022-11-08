import random
import base64


#função para criptografar
def encript(msg, pubkey):  
    emsg = []
    for l in msg:
        el = ord(l) ** pubkey[0] % pubkey[1] 
        emsg.append(el)
    emsg = ''.join(map(lambda n: chr(n), emsg))
    emsg = emsg.encode()
    emsg = base64.b64encode(emsg)
    emsg = emsg.decode()
    return emsg

#função geradora de chave de descriptografia
def dkeyGen(e, totiente, *, primom=3):  
    for c in range(primom, totiente):
        if ((c*e-1) / totiente) == ((c*e-1) // totiente):
            d = c
            if d != e:
                return d
            return d+totiente

#função de descriptografar
def decript(emsg, privkey):  
    dmsg = []
    for l in emsg:
        dl = ord(l) ** privkey[0] % privkey[1]
        dmsg.append(chr(dl))

    return dmsg

#função para formatar o input de primos e mandar para o gerador
def geraPrimo(lchar):   
    primos = []
    for w in lchar:
        soma = sum([ord(c) for c in w])
        print(f'soma1: {soma}')
        while True:
            if soma < 200:
                soma **= soma
            print(f'somap: {soma}')
            print(f'len: {len(str(soma))}')
            if len(str(soma)) // 4 >= 1:
                soma = (soma // (10**((len(str(soma))-3))))
            if soma > 200:
                break
        print(f'soma2: {soma}')
        soma += (soma % 2)-1
        print(f'soma3: {soma}')

        primos.append(geradorPrimos(soma))

    return sorted(primos)

#função q gera primos
def geradorPrimos(soma):    
    primeiros_primos = []
    for c in range(soma, 3, -2):
        if len(primeiros_primos) >= 20: 
            break 
        simprimo = True
        for n in range(3, c-1, 2):
            if c%n == 0:
                simprimo = False
                break
        if simprimo:
            primeiros_primos.append(c)
    print(primeiros_primos)
    return(primeiros_primos[random.randrange(0, len(primeiros_primos))])

#função que gera o e
def geraKeyPubli(mult, totiente):   
    possiveis = []
    for c in range(mult, 3, -2):
        if len(possiveis) >= 5:
            break
        sim = True
        if mult % c !=0:
            if totiente > c and totiente % c != 0:
                for n in range (3, c, 2):
                    if c%n == 0:
                        sim = False
                        break
            else:
                continue
        else:
            continue
        if sim:
            possiveis.append(c)
    return possiveis[random.randrange(0, len(possiveis))]

#função para verificar se o usuário colocou uma opção válida
def escolhaTipo():  
    while True:
        e_ou_d = input('Criptografar ou Descriptografar (C ou D): ').strip().upper()
        if e_ou_d == 'C' or e_ou_d == 'D':
            return e_ou_d
        print('Coloque apenas "C" ou "D"')
    

#função para descodificar a base64
def inpMsgCript(*, new=True):
    global emsg
    if new:
        emsg = input('Coloque a mensagem criptografada: ').strip()
    try:
        emsg = emsg.encode()
        emsg  = base64.b64decode(emsg)
        emsg = emsg.decode()
    except:
        print('\033[31mColoque uma mensagem criptografada válida (em b64)\033[m')
    return emsg


emsg = ''
while True:
    e_ou_d = escolhaTipo()
    if e_ou_d == 'C':
        v = True
        msg = input('Mensagem para criptografar: ')
        print(f'####################################################')
        cprimo1 = input('Digite letras para gerar o primeiro primo: ')
        cprimo2 = input('Digite letras para gerar o segundo primo: ')
        while v:
            try:
                primo1, primo2 = geraPrimo([cprimo1, cprimo2])
                mult = primo1*primo2
                totiente = (primo1 - 1) * (primo2 - 1)
                print(f'####################################################')
                print(mult)
                print(totiente)
                e = geraKeyPubli(mult, totiente)
                print(e)
                emsg = encript(msg, [e,mult])
                v = False
            except:
                print('\033[31mErro encontrado, mudando a chave\033[m')
        print(emsg)
        with open('./dados.txt', 'w') as arq: #primos + public_key + msg_cript
            arq.write(f'{str(primo1)}\n')
            arq.write(f'{str(primo2)}\n')
            arq.write(f'{str(e)}\n')
            arq.write(emsg)
        print('\033[32mOs dados dessa criptográfia foram salvos!\033[m')

    else:
        try:
            arq = open('./dados.txt', 'r')
            arq.close()
        except: 
            emsg = inpMsgCript()
            e = int(input('Coloque a chave "e": ').strip())
            primo1 = int(input('Coloque a chave "e": ').strip())
            primo2 = int(input('Coloque a chave "e": ').strip())
        msm = input('Deseja descriptografar a mensagem criptografada salva (sim ou não)? ').strip().upper()
        if msm not in 'SIM':
            emsg = inpMsgCript()
            e = int(input('Coloque a chave "e": ').strip())
            primo1 = int(input('Coloque o primeiro primo: ').strip())
            primo2 = int(input('Coloque o segundo primo: ').strip())
        else:
            with open('./dados.txt', 'r') as arq:
                primo1 = int(arq.readline())
                primo2 = int(arq.readline())
                e = int(arq.readline())
                emsg = arq.readline()
            emsg = inpMsgCript(new=False)
        mult = primo1 * primo2
        totiente = (primo1 - 1) * (primo2 - 1)
        dkey = dkeyGen(e, totiente, primom=primo1)
        print(f'####################################################')
        dmsg = decript(emsg, [dkey, mult])
        print(''.join(l for l in dmsg))


    resp = input('Deseja continuar (sim ou não)? ').strip().upper()
    if resp not in "SIM" or resp == '':
        break