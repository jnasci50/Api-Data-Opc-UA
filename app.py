from flask import Flask, render_template
from opc_data_request import conect_server, get_opc_data, read_input_value

# Declaração de variáveis globais

# Lista dos servidores para conectar

ADRESS_SERVER_A=['opc.tcp://CRTM13A0101:4840',
                 'opc.tcp://CRTM13A0102:4840',
                 'opc.tcp://CRTM13A0201:4840',
                 'opc.tcp://CRTM13A0202:4840',
                 'opc.tcp://CRTM13A0301:4840',
                 'opc.tcp://CRTM13A0302:4840',
                 'opc.tcp://CRTM13A0401:4840',
                 'opc.tcp://CRTM13A0402:4840',
                 'opc.tcp://CRTM13A0501:4840',
                 'opc.tcp://CRTM13A0502:4840',
                 'opc.tcp://CRTM13A0601:4840',
                 'opc.tcp://CRTM13A0602:4840',
                 'opc.tcp://CRTM13A0701:4840',
                 'opc.tcp://CRTM13A0702:4840',
                 'opc.tcp://CRTM13A0801:4840',
                 'opc.tcp://CRTM13A0802:4840']
                 #Fila B
ADRESS_SERVER_B=['opc.tcp://CRTM13B0101:4840',
                 'opc.tcp://CRTM13B0102:4840',
                 'opc.tcp://CRTM13A0201:4840',
                 'opc.tcp://CRTM13B0202:4840',
                 'opc.tcp://CRTM13B0301:4840',
                 'opc.tcp://CRTM13B0302:4840',
                 'opc.tcp://CRTM13B0401:4840',
                 'opc.tcp://CRTM13B0402:4840',
                 'opc.tcp://CRTM13B0501:4840',
                 'opc.tcp://CRTM13B0502:4840',
                 'opc.tcp://CRTM13B0601:4840',
                 'opc.tcp://CRTM13B0602:4840',
                 'opc.tcp://CRTM13B0701:4840',
                 'opc.tcp://CRTM13B0702:4840',
                 'opc.tcp://CRTM13B0801:4840',
                 'opc.tcp://CRTM13B0802:4840']
                 #fILA C
ADRESS_SERVER_C =['opc.tcp://CRTM13C0101:4840',
                 'opc.tcp://CRTM13C0102:4840',
                 'opc.tcp://CRTM13C0201:4840',
                 'opc.tcp://CRTM13C0202:4840',
                 'opc.tcp://CRTM13C0301:4840',
                 'opc.tcp://CRTM13C0302:4840',
                 'opc.tcp://CRTM13C0401:4840',
                 'opc.tcp://CRTM13C0402:4840',
                 'opc.tcp://CRTM13C0501:4840',
                 'opc.tcp://CRTM13C0502:4840',
                 'opc.tcp://CRTM13C0601:4840',
                 'opc.tcp://CRTM13C0602:4840',
                 'opc.tcp://CRTM13C0701:4840',
                 'opc.tcp://CRTM13C0702:4840',
                 'opc.tcp://CRTM13C0801:4840',
                 'opc.tcp://CRTM13C0802:4840']
                 #FILA D
ADRESS_SERVER_D =['opc.tcp://CRTM13D0601:4840',
                 'opc.tcp://CRTM13D0602:4840',
                 'opc.tcp://CRTM13D0701:4840',
                 'opc.tcp://CRTM13D0702:4840',
                 'opc.tcp://CRTM13D0801:4840',
                 'opc.tcp://CRTM13D0802:4840']

# Lista de variáveis para consultar
NODE_READ_VALUE = ['ns=4;s=.CC_IW_Temperature_Sensor','ns=4;s=.CC_IW_AirCondition_Cabinet_Actual_Temperatur']

# Dicionário para armazenar as conexões dos servidores
connected_servers_A = {}
connected_servers_B = {}
connected_servers_C = {}
connected_servers_D = {}

app = Flask(__name__)

@app.route("/")
def home():
    # Tenta conectar a cada servidor OPC UA na lista de endereços
    for address in ADRESS_SERVER_A:
        try:
            connected_servers_A[address] = conect_server(address)
        except Exception as e:
            print(f'Não foi possível conectar ao servidor OPC UA em {address}: Tipo do Erro: {e}')

    print(f'Dicionario Servidores OPC:{connected_servers_A}')
    print(f'Tipo dados dicionario servidor opc:{type(connected_servers_A)}')
    data_a = {}

    for i, address in enumerate(ADRESS_SERVER_A):
        try:
            if address in connected_servers_A:
                # Pega os dados do servidor e armazena ambos os valores em NODE_READ_VALUE
                opc_data_A = get_opc_data(connected_servers_A[address], NODE_READ_VALUE[:])
                data_a[f'machine{i + 1}_A_data'] = {
                    NODE_READ_VALUE[0]: opc_data_A.get(NODE_READ_VALUE[0], 0),
                    NODE_READ_VALUE[1]: opc_data_A.get(NODE_READ_VALUE[1], 0)
                }
            else:
                data_a[f'machine{i + 1}_A_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

        except Exception as e:
            print(f'Erro ao obter dados do servidor {address}: {e}')
            data_a[f'machine{i + 1}_A_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

    print(data_a)

    return render_template('index.html',
                           KM1A_Temperatura=data_a.get('machine1_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU1A_Temperatura=data_a.get('machine2_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM2A_temperatura=data_a.get('machine3_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU2A_Temperatura=data_a.get('machine4_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM3A_Temperatura=data_a.get('machine5_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU3A_Temperatura=data_a.get('machine6_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM4A_Temperatura=data_a.get('machine7_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU4A_Temperatura=data_a.get('machine8_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM5A_Temperatura=data_a.get('machine9_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU5A_Temperatura=data_a.get('machine10_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM6A_Temperatura=data_a.get('machine11_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU6A_Temperatura=data_a.get('machine12_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM7A_Temperatura=data_a.get('machine13_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU7A_Temperatura=data_a.get('machine14_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM8A_Temperatura=data_a.get('machine15_A_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU8A_Temperatura=data_a.get('machine16_A_data', {}).get(NODE_READ_VALUE[1], 0),
                           )
@app.route("/FILA_B")
def FilaB():
   # Tenta conectar a cada servidor OPC UA na lista de endereços
    for address in ADRESS_SERVER_B:
        try:
            connected_servers_B[address] = conect_server(address)
        except Exception as e:
            print(f'Não foi possível conectar ao servidor OPC UA em {address}: Tipo do Erro: {e}')

    print(f'Dicionario Servidores OPC:{connected_servers_B}')
    data_b = {}

    for i, address in enumerate(ADRESS_SERVER_B):
        try:
            if address in connected_servers_B:
                # Pega os dados do servidor e armazena ambos os valores em NODE_READ_VALUE
                opc_data = get_opc_data(connected_servers_B[address], NODE_READ_VALUE[:])
                data_b[f'machine{i+1}_B_data'] = {
                    NODE_READ_VALUE[0]: opc_data.get(NODE_READ_VALUE[0], 0),
                    NODE_READ_VALUE[1]: opc_data.get(NODE_READ_VALUE[1], 0)
                }
            else:
                data_b[f'machine{i+1}_B_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

        except Exception as e:
            print(f'Erro ao obter dados do servidor {address}: {e}')
            data_b[f'machine{i+1}_B_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

    print(data_b)

    return render_template('FILA_B.html',
                           KM1B_Temperatura=data_b.get('machine1_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU1B_Temperatura=data_b.get('machine2_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM2B_temperatura=data_b.get('machine3_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU2B_Temperatura=data_b.get('machine4_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM3B_Temperatura=data_b.get('machine5_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU3B_Temperatura=data_b.get('machine6_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM4B_Temperatura=data_b.get('machine7_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU4B_Temperatura=data_b.get('machine8_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM5B_Temperatura=data_b.get('machine9_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU5B_Temperatura=data_b.get('machine10_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM6B_Temperatura=data_b.get('machine11_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU6B_Temperatura=data_b.get('machine12_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM7B_Temperatura=data_b.get('machine13_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU7B_Temperatura=data_b.get('machine14_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM8B_Temperatura=data_b.get('machine15_B_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU8B_Temperatura=data_b.get('machine16_B_data', {}).get(NODE_READ_VALUE[1], 0),
                           )

@app.route("/FILA_C")
def FilaC():
    # Tenta conectar a cada servidor OPC UA na lista de endereços
    for address in ADRESS_SERVER_C:
        try:
            connected_servers_C[address] = conect_server(address)
        except Exception as e:
            print(f'Não foi possível conectar ao servidor OPC UA em {address}: Tipo do Erro: {e}')

    print(f'Dicionario Servidores OPC:{connected_servers_C}')
    data_c = {}

    for i, address in enumerate(ADRESS_SERVER_C):
        try:
            if address in connected_servers_C:
                # Pega os dados do servidor e armazena ambos os valores em NODE_READ_VALUE
                opc_data = get_opc_data(connected_servers_C[address], NODE_READ_VALUE[:])
                data_c[f'machine{i+1}_C_data'] = {
                    NODE_READ_VALUE[0]: opc_data.get(NODE_READ_VALUE[0], 0),
                    NODE_READ_VALUE[1]: opc_data.get(NODE_READ_VALUE[1], 0)
                }
            else:
                data_c[f'machine{i+1}_C_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

        except Exception as e:
            print(f'Erro ao obter dados do servidor {address}: {e}')
            data_c[f'machine{i+1}_C_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

    print(data_c)

    return render_template('FILA_C.html',
                           KM1C_Temperatura=data_c.get('machine1_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU1C_Temperatura=data_c.get('machine2_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM2C_temperatura=data_c.get('machine3_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU2C_Temperatura=data_c.get('machine4_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM3C_Temperatura=data_c.get('machine5_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU3C_Temperatura=data_c.get('machine6_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM4C_Temperatura=data_c.get('machine7_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU4C_Temperatura=data_c.get('machine8_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM5C_Temperatura=data_c.get('machine9_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU5C_Temperatura=data_c.get('machine10_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM6C_Temperatura=data_c.get('machine11_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU6C_Temperatura=data_c.get('machine12_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM7C_Temperatura=data_c.get('machine13_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU7C_Temperatura=data_c.get('machine14_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM8C_Temperatura=data_c.get('machine15_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU8C_Temperatura=data_c.get('machine16_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           )
@app.route("/FILA_D")
def FilaD():
    
    # Tenta conectar a cada servidor OPC UA na lista de endereços
    for address in ADRESS_SERVER_D:
        try:
            connected_servers_D[address] = conect_server(address)
        except Exception as e:
            print(f'Não foi possível conectar ao servidor OPC UA em {address}: Tipo do Erro: {e}')

    print(f'Dicionario Servidores OPC:{connected_servers_D}')
    data_d = {}

    for i, address in enumerate(ADRESS_SERVER_D):
        try:
            if address in connected_servers_D:
                # Pega os dados do servidor e armazena ambos os valores em NODE_READ_VALUE
                opc_data = get_opc_data(connected_servers_D[address], NODE_READ_VALUE[:])
                data_d[f'machine{i+1}_D_data'] = {
                    NODE_READ_VALUE[0]: opc_data.get(NODE_READ_VALUE[0], 0),
                    NODE_READ_VALUE[1]: opc_data.get(NODE_READ_VALUE[1], 0)
                }
            else:
                data_d[f'machine{i+1}_D_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

        except Exception as e:
            print(f'Erro ao obter dados do servidor {address}: {e}')
            data_d[f'machine{i+1}_D_data'] = {NODE_READ_VALUE[0]: 0, NODE_READ_VALUE[1]: 0}

    print(data_d)

    return render_template('FILA_D.html',
                           #KM1C_Temperatura=data_c.get('machine1_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           #PU1C_Temperatura=data_c.get('machine2_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           #KM2C_temperatura=data_c.get('machine3_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           #PU2C_Temperatura=data_c.get('machine4_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           #KM3C_Temperatura=data_c.get('machine5_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           #PU3C_Temperatura=data_c.get('machine6_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           #KM4C_Temperatura=data_c.get('machine7_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           #PU4C_Temperatura=data_c.get('machine8_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           #KM5C_Temperatura=data_c.get('machine9_C_data', {}).get(NODE_READ_VALUE[0], 0),
                           #PU5C_Temperatura=data_c.get('machine10_C_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM6D_Temperatura=data_d.get('machine1_D_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU6D_Temperatura=data_d.get('machine2_D_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM7D_Temperatura=data_d.get('machine3_D_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU7D_Temperatura=data_d.get('machine4_D_data', {}).get(NODE_READ_VALUE[1], 0),
                           KM8D_Temperatura=data_d.get('machine5_D_data', {}).get(NODE_READ_VALUE[0], 0),
                           PU8D_Temperatura=data_d.get('machine6_D_data', {}).get(NODE_READ_VALUE[1], 0),
                           )

if __name__ == '__main__':
    app.run(debug=False)