from opcua import Client,ua
from Send_Email import send_email
def conect_server(adress):

    client = Client(adress)

    try:
        client.connect()
        root = client.get_root_node()
        print(f'Conexão com servidor OPC UA. Realizada com sucesso')
        #print(f'Número do Root: {root}')
    except:
        #print('Não Foi possivel conectar ao servidor OPC')
        client.disconnect()
    return client


def get_opc_data(server, nodes):
    """
    Lê os valores dos nós especificados em um servidor OPC UA.

    Parâmetros:
    server (Client): Cliente conectado ao servidor OPC UA.
    nodes (list): Lista de identificadores dos nós a serem lidos.

    Retorna:
    dict: Dicionário com os valores lidos.
    """
    data = {}
    for node in nodes:
        try:
            data[node] = read_input_value(node, server)
        except Exception as e:
            #print(f'Erro ao ler o nó {node}: {e}')
            data[node] = 0  # ou um valor padrão, por exemplo, 0
    return data


def read_input_value(node_id, client):
    """
    Lê o valor de um nó específico no servidor OPC UA.

    Parâmetros:
    node_id (str): Identificador do nó.
    client (Client): Cliente OPC UA.

    Retorna:
    result (float): Valor do nó arredondado para duas casas decimais.
    """
    client_node = client.get_node(node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    #print(f"Servidor OPC UA nó :{ str(client_node)}. Valor lido:{str(client_node_value)}.")
    result_float = float(client_node_value)
    result = round(result_float,2)/10
    print(result)

    tentativas = 0

    if result == 40.1:
        for i in range(4):
            subject = "Alerta: Alta temperatura no painel"
            body = (f"O valor de temperatura no painel da máquina: {node_id} excedeu o limite: {result}. "
            f"Favor direcionar um mantenedor para avaliar")
            to_address = "jaironascij2@gmail.com"
            send_email(subject, body, to_address)
            tentativas = i+1
            if tentativas == 2:
                break

    return result

'''def write_value_bool(node_id,client,value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))'''





