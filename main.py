import random

#manipulacao de arquivos---------------------------------------------------

def carregar_dados():
    
    nome_arquivo = "usuarios.txt"
    # Dicionário padrão caso o arquivo não exista ou ocorra erro
    usuarios = {"admin": {"senha": "123", "vitorias": 3, "pontos": 5000}}
    # dado generico
   
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            dicionario_temporario = {}
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                # quebra o texto usando o ponto e virgula como separador
                partes = linha.split(";")
                if len(partes) == 4:
                    usuario = partes[0]
                    senha = partes[1]
                    vitorias = int(partes[2])
                    pontos = int(partes[3])
                    
                    dicionario_temporario[usuario] = {
                        "senha": senha,
                        "vitorias": vitorias,
                        "pontos": pontos
                    }
            # Se a leitura ocorreu com sucesso e contem dados, retorna o dicionário lido
            if dicionario_temporario:
                return dicionario_temporario
    except:
        
        pass
    
    
    return usuarios

def salvar_dados(dados):
    # grava os dados das variaveis no arquivo txt quando precisa
    try:
        with open("usuarios.txt", "w", encoding="utf-8") as arquivo:
            for usuario, info in dados.items():
                # junta tudo virando texto puro separado por ponto e virgula
                linha = f"{usuario};{info['senha']};{info['vitorias']};{info['pontos']}\n"
                arquivo.write(linha)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

#logicas do jogo--------------------------------------------------------

def criar_tabuleiro():
    #cria um matriz(tabuleiro) capaz de ser interagido e mutavel
    return [["🟦" for _ in range(10)] for _ in range(10)]
#utilizacao de "bloco de agua" como inicial

def exibir_tabuleiro(tabuleiro):
    #um tabuleiro que usuario eh capaz de visualizar e atualizar informacoes
    print("\n    1  2  3  4  5  6  7  8  9  10")#coluna
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']#linha
    for linha in range(10):
        print(f"{letras[linha]} ", end=" ")
        
        for coluna in range(10):
            print(tabuleiro[linha][coluna], end=' ')
        print()

def converter_coordenada(coordenada):
    #converte letras em coordenadas de numeros
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    try:
        letra = coordenada[0].upper()
        #maisculo ou minusculo equivalentes
        coluna = int(coordenada[1:]) - 1
        if letra in letras and 0 <= coluna < 10:
            linha = letras.index(letra)
            return linha, coluna
    except:
        pass
    return None, None

def validar_posicionamento(tabuleiro, linha, coluna, tamanho, orientacao):
    #verifica se o barco cabe nos limites e não sobrepoe outro
    for i in range(tamanho):
        nova_linha = linha + (i if orientacao == 'V' else 0)
        nova_coluna = coluna + (i if orientacao == 'H' else 0)
        
        #restringir dentro do tabuleiro 10x10
        if nova_linha >= 10 or nova_coluna >= 10:
            return False
        # evitar sobreposicao
        if tabuleiro[nova_linha][nova_coluna] == "🚢":
            return False
            
    return True

def posicionar_barco(tabuleiro, linha, coluna, tamanho, orientacao):
    #modificar a agua para um navio
    for i in range(tamanho):
        nova_linha = linha + (i if orientacao == 'V' else 0)
        nova_coluna = coluna + (i if orientacao == 'H' else 0)
        tabuleiro[nova_linha][nova_coluna] = "🚢"

def posicionar_bot(tabuleiro_bot, frota):
    #usar funcao random pra colocar barcos para bot
    for barco in frota:
        while True:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
            orientacao = random.choice(['H', 'V'])
            
            if validar_posicionamento(tabuleiro_bot, linha, coluna, barco['tamanho'], orientacao):
                posicionar_barco(tabuleiro_bot, linha, coluna, barco['tamanho'], orientacao)
                break

def dar_tiro(tabuleiro_alvo, linha, coluna):
    #atualiza estado de cada bloco no jogo
    if tabuleiro_alvo[linha][coluna] == "🚢":
        print("💥 FOGO! Um barco foi atingido!")
        tabuleiro_alvo[linha][coluna] = "💥"
        #vira o fogo, para indicar que acertou
        return True
    else:
        print("💦 ÁGUA! Nenhum barco por aqui.")
        tabuleiro_alvo[linha][coluna] = "💦"
        #se nao, mostra agua sem nada
        return False

def sortear_inicio():
    #sortear quem comeca
    quem_comeca = random.randint(1, 2)
    if quem_comeca == 1:
        print("\n🎲 Sorteio realizado: Você começa!")
        return "jogador"
    else:
        print("\n🎲 Sorteio realizado: O inimigo começa!")
        return "inimigo"

# cadastrar usuario-------------------------------------------------------

def cadastrar_usuario(usuarios):
    """Solicita credenciais e adiciona ao dicionário, salvando em arquivo"""
    print("\n--- TELA DE CADASTRO ---")
    usuario = input("Escolha um nome de usuário: ").strip().lower()
    if not usuario:
        print("❌ O nome de usuário não pode ser vazio!")
        return usuarios
    if usuario in usuarios:
        print("❌ Este nome de usuário já está em uso!")
        return usuarios
        
    senha = input("Digite uma senha: ")
    if not senha:
        print("❌ A senha não pode ser vazia!")
        return usuarios
        
    usuarios[usuario] = {"senha": senha, "vitorias": 0, "pontos": 0}
    salvar_dados(usuarios)
    print(f"✅ Usuário '{usuario}' cadastrado com sucesso!")
    return usuarios

def fazer_login(usuarios):
    """Valida o login e retorna o usuário ativo para o escopo do menu"""
    print("\n--- TELA DE LOGIN ---")
    usuario = input("Usuário: ").strip().lower()
    senha = input("Senha: ")
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"✅ Bem-vindo, {usuario}!")
        return usuario
    else:
        print("❌ Usuário ou senha incorretos.")
        return None

def visualizar_recordes(usuarios):
    # cria o ranking ordenando a pontuacao do maior pro menor
    print("\n" + "="*15 + " RANKING UNIVERSAL " + "="*15)
    if not usuarios:
        print("Nenhum jogador cadastrado ainda.")
        return
    
    # ordena usando lambda pra ler a pontuacao dentro do dicionario de dados
    ranking = sorted(usuarios.items(), key=lambda x: x[1].get("pontos", 0), reverse=True)
    
    print(f"{'Posicao':<7} | {'Jogador':<15} | {'Pontos':<10} | {'Vitórias':<8}")
    print("-" * 48)
    for i, (jogador, dados) in enumerate(ranking, start=1):
        print(f"#{i:<5} | {jogador:<15} | {dados.get('pontos', 0):<10} | {dados.get('vitorias', 0):<8}")
    print("=" * 48)
    input("\nPressione Enter para voltar ao menu...")


# funcao principal---------------------------------------------------------------------
def jogar_partida(usuarios, jogador_atual):
    #gerencia toda a rodada da partida
    barcos_jogador = 17
    barcos_bot = 17
    #indica quantas partes de barco cada um possui, ao zerar perde e finaliza execucao
    proximos_alvos = []
    pontos_partida = 10000
    #pontuacao inicial

    if jogador_atual:
        print(f"\n--- INICIANDO JOGO (Logado como: {jogador_atual}) ---")
    else:
        print("\n--- INICIANDO JOGO (Modo Convidado - Pontos não serão salvos) ---")

    meu_tabuleiro = criar_tabuleiro()
    tabuleiro_bot = criar_tabuleiro()
    #chamou a funcao para gerar tableiro 10x10
    
    visao_do_jogador = criar_tabuleiro()

    frota = [
        {"nome": "Porta-avioes", "tamanho": 5},
        {"nome": "Navio de guerra", "tamanho": 4},
        {"nome": "Contratorpedeiro 1", "tamanho": 3},
        {"nome": "Contratorpedeiro 2", "tamanho": 3},
        {"nome": "Submarino", "tamanho": 2}
    ]
    # foram diferentes argumentos passados para funcao posicionar barcos, diferenca de nome e tamanho

    posicionar_bot(tabuleiro_bot, frota)
    print(" O Bot ja posicionou a frota dele secretamente!")

    # Fase de posicionamento do usuario
    for barco in frota:
        while True:
            exibir_tabuleiro(meu_tabuleiro)
            print(f"\nPosicione seu **{barco['nome']}** (Tamanho: {barco['tamanho']})")
            
            coordenada = input("Digite a coordenada inicial (Ex: A5) ou 'sair': ").strip()
            if coordenada.lower() == 'sair':
                print("Voltando ao menu principal...")
                return usuarios
                
            linha, coluna = converter_coordenada(coordenada)
            #chamando a funcao para converter letra em numero de lista
            
            if linha is None or coluna is None:
                #verificacao de se existe coordenadas
                print("❌ Coordenada inválida! Use o formato LetraNumero (ex: B3).")
                continue
            
            orientacao = 'H'
            if barco['tamanho'] > 1:
                #checar a necessidade de posicionar em horizontal ou vertical(acaba que todos foram)
                orientacao = input("Orientação - (H)orizontal ou (V)ertical? ").strip().upper()
                
                if orientacao not in ['H', 'V']:
                    #averigue se usuario colocou opcao valida
                    print("❌ Orientação inválida! Escolha H ou V.")
                    continue
            
            if validar_posicionamento(meu_tabuleiro, linha, coluna, barco['tamanho'], orientacao):
                posicionar_barco(meu_tabuleiro, linha, coluna, barco['tamanho'], orientacao)
                print(f"✅ {barco['nome']} posicionado com sucesso!")
                break 
            else:
                print("❌ Não é possível posicionar o barco aqui. Ele bate em outro ou sai do mapa!")
    
    turno = sortear_inicio()
    # sorteando
    input("\nPressione Enter para começar a batalha...")

    partida_rolando = True
    # sempre comecara o jogo
    while partida_rolando:
        
        # round do player
        if turno == "jogador":
            print("\n================ MEU TABULEIRO DE ATAQUE ================")
            exibir_tabuleiro(visao_do_jogador)
            print("\n================ MEU TABULEIRO DE DEFESA ================")
            exibir_tabuleiro(meu_tabuleiro)
            print(f" Seus pontos atuais nesta rodada: {pontos_partida}")
            print(f"\n SUA VEZ! (O inimigo ainda tem {barcos_bot} partes de barcos)")
            
            coordenada_tiro = input("Digite a coordenada do seu tiro (Ex: B4): ").strip()
            l_tiro, c_tiro = converter_coordenada(coordenada_tiro)
            
            if l_tiro is None or c_tiro is None:
                print("❌ Coordenada inválida! Turno mantido para tentar novamente.")
                continue
                
            if visao_do_jogador[l_tiro][c_tiro] in ["💥", "💦"]:
                print("⚠️ Você já atirou aí antes! Escolha outra coordenada.")
                continue

            pontos_partida -= 100
            #ou seja, a cada rodada (tiro), jogador comeca a perder ponto
            acertou = dar_tiro(tabuleiro_bot, l_tiro, c_tiro)
            
            if acertou:
                barcos_bot -= 1
                visao_do_jogador[l_tiro][c_tiro] = "💥"
                print("🔥 Você acertou! Jogue mais uma vez!")
            else:
                visao_do_jogador[l_tiro][c_tiro] = "💦"
                turno = "inimigo" 
                input("\nVocê errou... Pressione Enter para passar a vez ao bot...")
                
            if barcos_bot == 0:
                # verificacao para terminar o jogo
                print("\n🏆 FIM DE JOGO! Você afundou todos os barcos do bot!")
                bonus_sobreviventes = barcos_jogador * 200
                pontos_finais = pontos_partida + bonus_sobreviventes
                
                print(f"Pontos de precisão restantes: {pontos_partida}")
                print(f"Bônus de barcos sobreviventes ({barcos_jogador} partes x 200): +{bonus_sobreviventes}")
                # total de pontos eh dado pela (10000-rodadas*100)+(200*parte de barco do jogador intacto)
                print(f"🏅 Total acumulado nesta partida: {pontos_finais}")
                
                if jogador_atual:
                    usuarios[jogador_atual]["vitorias"] += 1
                    usuarios[jogador_atual]["pontos"] += pontos_finais
                    salvar_dados(usuarios) # Grava pontualmente a vitória obtida
                    print(f"⭐ Registro salvo no perfil de {jogador_atual}!")
                
                partida_rolando = False
            
        # round do bot
        elif turno == "inimigo":
            print("\n VEZ DO INIMIGO! O bot está calculando o alvo...")
            
            l_bot, c_bot = None, None
            
            while proximos_alvos:
                possivel_l, possivel_c = proximos_alvos.pop(0)
                if meu_tabuleiro[possivel_l][possivel_c] not in ["💥", "💦"]:
                    # nao atirar nas posicoes que ja foram atingidos
                    l_bot, c_bot = possivel_l, possivel_c
                    break
                
            
            if l_bot is None or c_bot is None:
                while True:
                    l_bot = random.randint(0, 9)
                    c_bot = random.randint(0, 9)
                    if meu_tabuleiro[l_bot][c_bot] not in ["💥", "💦"]:
                        break
                        #sai do loop ate achar uma posicao valida
            
            letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            print(f" O bot disparou em: {letras[l_bot]}{c_bot + 1}")
            
            acertou = dar_tiro(meu_tabuleiro, l_bot, c_bot)
            
            if acertou:
                barcos_jogador -= 1
                print("💥 O bot acertou e ganhou uma jogada extra!")
                
                vizinhos = [
                    (l_bot - 1, c_bot), (l_bot + 1, c_bot),
                    (l_bot, c_bot - 1), (l_bot, c_bot + 1)
                ]
                # essa eh uma pequena mecanismo apos de bot ter acertado, que forca ele a atirar na vertical e horizontal daquela regiao atingida, uma vez que todos os barcos tem 2 ou mais partes e sao posicionadas em H e V
                for vl, vc in vizinhos:
                    if 0 <= vl < 10 and 0 <= vc < 10:
                        if meu_tabuleiro[vl][vc] not in ["💥", "💦"]:
                            proximos_alvos.append((vl, vc))
                input("Pressione Enter para ver o próximo movimento do bot...")
            else:
                turno = "jogador"
                # a rodada volta da ser da vez do usuario
                input("\nO bot errou! Pressione Enter para pegar o controle do jogo...")
                
            if barcos_jogador == 0:
                print("\n💀 DERROTA! O bot destruiu sua frota inteira.")
                pontos_finais = max(0, pontos_partida)
                print(f"🏅 Você opteve {pontos_finais} pontos nesta partida.")
                if jogador_atual:
                    usuarios[jogador_atual]["pontos"] += pontos_finais
                    salvar_dados(usuarios)
                    print(f"🛡️ Pontos computados na conta de {jogador_atual}.")
                partida_rolando = False

    print("\nPartida encerrada. Voltando ao menu principal automaticamente...")
    input("Pressione Enter...")
    return usuarios

#menu principal-----------------------------------------------------------

def executar_sistema():
    # funcao que guarda o estado principal do jogo e inicia as coisas
    # puxa os dados salvos no texto plano
    usuarios_cadastrados = carregar_dados()
    jogador_atual = None
    
    while True:
        status = f"(Logado como: {jogador_atual})" if jogador_atual else "(Modo Convidado)"
        print(f'\n--- MENU PRINCIPAL {status} ---')
        print('1 - Jogar')
        print('2 - Cadastrar Novo Usuário')
        print('3 - Entrar na Conta (Login)')
        print('4 - Sair da Conta (Logout)')
        print('5 - Visualizar Ranking Universal')
        print('6 - Sair do Jogo')
        
        try:
            opcao = int(input('Escolha uma opcao: '))
            if opcao == 1:
                usuarios_cadastrados = jogar_partida(usuarios_cadastrados, jogador_atual)  
            elif opcao == 2:
                usuarios_cadastrados = cadastrar_usuario(usuarios_cadastrados)
            elif opcao == 3:
                jogador_atual = fazer_login(usuarios_cadastrados)
            elif opcao == 4:
                if jogador_atual:
                    print(f"👋 Conta '{jogador_atual}' desconectada.")
                    jogador_atual = None
                else:
                    print("⚠️ Ninguém está logado no momento.")
            elif opcao == 5:
                visualizar_recordes(usuarios_cadastrados)
            elif opcao == 6:
                print("Até mais!")
                break
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Por favor, digite um número válido.")

# execucao 
if __name__ == "__main__":
    executar_sistema()