import argparse
import datetime
import json
import random

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "num_call_logs",
    nargs="?",
    default=10000,
    type=int,
    help="Número de arquivos de registro de chamadas a serem gerados",
)
args = parser.parse_args()
config = vars(args)

NUM_CALL_LOG_FILES = config["num_call_logs"]

greetings = [
    "Olá, como posso ajudar você hoje?",
    "Oi, com o que posso te ajudar hoje?",
    "Saudações, como posso te ajudar?",
    "Oi, seja bem-vindo(a) ao suporte, como posso te ajudar hoje?",
    "Olá, no que posso te ajudar?",
]

devices = [
    "televisão",
    "laptop",
    "roteador",
    "celular",
    "relógio inteligente",
    "tablet",
    "dispositivo de streaming",
]

problems = [
    "O(a) {0} não liga. O(a) {0} não responde a nenhum botão ou comando. A luz de energia do(a) {0} não acende.",
    "O(a) {0} não está conectando à internet. O(a) {0} não consegue se conectar a uma rede Wi-Fi. O(a) {0} não consegue se conectar à internet quando conectado(a) a uma rede cabeada.",
    "Não consigo baixar nenhum aplicativo no meu {0}. Só consigo acessar o aplicativo de mensagens no meu {0}. Não consigo acessar outros aplicativos.",
    "Não consegui conectar à minha conta do meu {0}. Não consigo fazer login na minha conta no meu {0}. Não consigo acessar minha conta no {0}. Não sei o que fazer para consertar minha conta.",
    "A bateria do meu {0} dura apenas 30 minutos. A bateria descarrega rapidamente após ser totalmente carregada. A bateria do {0} não dura mais tanto quanto antes.",
]

problem_detail = [
    "O/A {0} diz que há um erro com a atualização mais recente. O/A {0} está travado(a) na atualização anterior. A atualização não está funcionando corretamente no/a {0}.",
    "Isso está acontecendo há 4 dias, quando deixei o/a {0} cair. É possível que a queda tenha causado algum dano ao/à {0}.",
    "O/A {0} não responde quando tento redefini-lo(a) para os padrões de fábrica. Mudei as configurações de energia há alguns dias e o/a {0} nãoestá funcionando corretamente desde então.",
    "Tentei usar o assistente de solução de problemas no/a {0}, mas não ajudou. Havia um aviso para verificar se o/a {0} tem espaço de armazenamento suficiente e se é compatível com o software que estou tentando usar.",
    "O problema com o/a {0} ainda está acontecendo desde a última vez que liguei. Tentei reiniciar o/a {0} 3 vezes e o problema ainda está acontecendo. Ele/a está reportando um erro de memória aproximadamente uma vez por hora."
]

statuses = [
    "Erro: Falha na atualização. A atualização não está disponível para sua versão principal atual. Verifique se há atualizações novamente mais tarde.",
    "Todos os sistemas normais. Seu dispositivo está conectado à internet e funcionando normalmente. Não há problemas a serem relatados.",
    "Aviso: Sem armazenamento disponível. O disco rígido do seu computador está cheio. Exclua alguns arquivos e tente novamente. Você também pode tentar liberar espaço movendo alguns arquivos para um dispositivo de armazenamento externo.",
    "Erro: Sua conta não está autorizada a acessar este recurso. Entre em contato com o administrador para obter assistência.",
    "Aviso: Sem conexão com a internet. Sua conexão com a internet está bloqueada por um firewall. Entre em contato com o administrador para desbloqueá-la."
]

solutions = [
    "Você já tentou desligar e ligar o/a {0} novamente? O/A {0} deve estar conectado(a) à internet para contatar nossos servidores. Se não estiver, verifique sua conexão com a internet e certifique-se de que seu/sua {0} está conectado(a).",
    "Você pode atualizar seu/sua {0} para a versão de firmware mais recente? Você pode verificar se o firmware do seu/sua {0} está atualizado acessando as configurações do/da {0} e procurando uma opção de atualização de firmware. Se houver uma atualização disponível, instale-a.",
    "Verifique se seu/sua {0} é capaz de acessar o conteúdo de streaming. Você pode verificar se seu/sua {0} é capaz de acessar o conteúdo de streaming tentando assistir a um programa ou filme em um serviço de streaming. Se você não conseguir assistir nada, verifique sua conexão com a internet e certifique-se de que seu/sua {0} está conectado(a) à rede correta.",
    "Verifique se seu/sua {0} está recebendo sinal. Você pode verificar se seu/sua {0} está recebendo sinal usando um medidor de intensidade de sinal. Se a intensidade do sinal for baixa, talvez seja necessário mover seu/sua {0} para mais perto do roteador.",
    "Você já tentou redefinir o/a {0} para as configurações de fábrica? Você pode verificar se as configurações do seu/sua {0} estão corretas acessando as configurações do/da {0} e procurando uma opção de configurações padrão. Se houver uma opção de configurações padrão, redefina seu/sua {0} para as configurações padrão.",
]

check_solved = [
    "Claro, isso resolve tudo por hoje?",
    "Sem problemas, há algo mais com que eu possa ajudar?",
    "Com certeza, isso resolveu o problema para você?",
    "Parece bom, há algum outro problema com o qual eu possa ajudar?",
    "Ótimo, isso corrigiu o problema?",
]

problem_solved = [
    "Sim, meu problema está resolvido agora. Verifiquei as configurações do meu {0} e me certifiquei de que tudo está configurado corretamente.",
    "Não, ainda estou com o mesmo problema. Vou tentar entrar em contato com o fabricante do {0} para obter ajuda.",
    "Sim, tudo está funcionando bem agora. Tentei usar uma conexão diferente para ver se o problema é com o {0} ou com o provedor de internet.",
    "Sim, o {0} parece estar funcionando agora. Verifiquei as conexões e me certifiquei de que tudo está conectado corretamente.",
    "Não, estou com um problema diferente agora com o {0}. Tentei usar um site ou aplicativo diferente para ver se o problema é com o próprio site ou aplicativo.",
]


def generate_log():
    # Select a device that the user is having trouble with
    device = random.choice(devices)

    # Generate timestamps within the last 30 days in microseconds of epoch time
    dt = datetime.datetime.today() - random.random() * datetime.timedelta(days=30)
    timestamp = int(round(dt.timestamp()) * 1e6)
    response_delay = int(random.randint(10, 30) * 1e6)

    # Generate JSON object of conversation
    call_log = {
        "entries": [
            {
                "start_timestamp_usec": timestamp + response_delay * 0,
                "text": random.choice(greetings),
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 1,
                "text": "Hi, I'm having an issue with my " + device,
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 2,
                "text": "Sorry to hear. Can you tell me what the problem is?",
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 3,
                "text": random.choice(problems).format(device),
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 4,
                "text": "Can you give me more details about the problem with your {0}?".format(device),
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 5,
                "text": random.choice(problem_detail).format(device),
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 6,
                "text": "And what is the status shown in the settings on the {0}?".format(device),
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 7,
                "text": random.choice(statuses),
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 8,
                "text": "Can you tell me your account number?",
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 9,
                "text": "Sure, it's " + str(random.randint(100000000, 999999999)),
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 10,
                "text": random.choice(solutions).format(device),
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 11,
                "text": "I see, thanks for the information, I will give that a try.",
                "role": "CUSTOMER",
                "user_id": 1,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 12,
                "text": random.choice(check_solved),
                "role": "AGENT",
                "user_id": 2,
            },
            {
                "start_timestamp_usec": timestamp + response_delay * 13,
                "text": random.choice(problem_solved).format(device),
                "role": "CUSTOMER",
                "user_id": 1,
            },
        ]
    }

    json_object = json.dumps(call_log, indent=4)
    return json_object


for i in range(NUM_CALL_LOG_FILES):
    filename = "output/chat_" + str(i) + ".json"
    with open(filename, "w") as outfile:
        output = generate_log()
        outfile.write(output)
