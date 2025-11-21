import random
import time

class SimuladorTransporte:
    def __init__(self):
        self.pacotes = []
        self.pacotes_recebidos = []
        self.historico_execucoes = []  # >>> ADIÇÃO DO RELATÓRIO FINAL
        
    def criar_pacotes(self, mensagem, tamanho_pacote=4):
        print(f"\nCriando pacotes da mensagem: '{mensagem}'")
        self.pacotes = []
        
        for i in range(0, len(mensagem), tamanho_pacote):
            pacote = {
                'numero': len(self.pacotes),
                'dados': mensagem[i:i+tamanho_pacote],
                'ack': False
            }
            self.pacotes.append(pacote)
            
        print(f"Criados {len(self.pacotes)} pacotes:")
        for pacote in self.pacotes:
            print(f"   Pacote {pacote['numero']}: '{pacote['dados']}'")
        
        return self.pacotes
    
    def _gerar_taxas_aleatorias(self, protocolo):
        if protocolo == "stop_and_wait":
            return {
                'perda_pacote': random.uniform(0.1, 0.4),
                'perda_ack': random.uniform(0.1, 0.3),
                'atraso': random.uniform(0.5, 2.0)
            }
        elif protocolo == "go_back_n":
            return {
                'perda_pacote': random.uniform(0.15, 0.35),
                'perda_ack': random.uniform(0.1, 0.25),
                'tamanho_janela': random.randint(2, 5)
            }
        else:
            return {
                'perda_pacote': random.uniform(0.2, 0.6),
                'corrupcao': random.uniform(0.05, 0.2),
                'duplicacao': random.uniform(0.05, 0.15)
            }
    
    def _simular_problema_rede(self, taxa, tipo_problema):
        return random.random() < taxa
    
    def stop_and_wait(self, mensagem):
        print("\nINICIANDO STOP-AND-WAIT")
        print("=" * 40)
        
        taxas = self._gerar_taxas_aleatorias("stop_and_wait")
        print(f"Taxas desta execução:")
        print(f"   Perda de pacotes: {taxas['perda_pacote']:.1%}")
        print(f"   Perda de ACKs: {taxas['perda_ack']:.1%}")
        print(f"   Atraso de timeout: {taxas['atraso']:.1f}s")
        
        pacotes = self.criar_pacotes(mensagem)
        self.pacotes_recebidos = []
        tentativas = 0
        
        for i, pacote in enumerate(pacotes):
            enviado_com_sucesso = False
            tentativas_pacote = 0
            
            while not enviado_com_sucesso and tentativas_pacote < 5:
                tentativas += 1
                tentativas_pacote += 1
                
                print(f"\nTentativa {tentativas_pacote}: Enviando pacote {i}: '{pacote['dados']}'")
                
                if self._simular_problema_rede(taxas['perda_pacote'], 'perda_pacote'):
                    print("Pacote perdido. Aguardando timeout...")
                    time.sleep(taxas['atraso'])
                    continue
                
                print(f"Pacote {i} recebido: '{pacote['dados']}'")
                
                if self._simular_problema_rede(taxas['perda_ack'], 'perda_ack'):
                    print("ACK perdido. Aguardando timeout...")
                    time.sleep(taxas['atraso'])
                    continue
                
                print(f"ACK {i} confirmado")
                self.pacotes_recebidos.append(pacote['dados'])
                enviado_com_sucesso = True
            
            if not enviado_com_sucesso:
                print(f"Pacote {i} abandonado após 5 tentativas")
        
        self._mostrar_resultado(mensagem, tentativas)
        self._registrar_execucao("Stop-and-Wait", mensagem)  
    
    def go_back_n(self, mensagem):
        print("\nINICIANDO GO-BACK-N")
        print("=" * 40)
        
        taxas = self._gerar_taxas_aleatorias("go_back_n")
        tamanho_janela = taxas['tamanho_janela']
        
        print(f"Taxas desta execução:")
        print(f"   Perda de pacotes: {taxas['perda_pacote']:.1%}")
        print(f"   Perda de ACKs: {taxas['perda_ack']:.1%}")
        print(f"   Tamanho da janela: {tamanho_janela}")
        
        pacotes = self.criar_pacotes(mensagem)
        self.pacotes_recebidos = []
        proximo_a_enviar = 0
        base = 0
        total_transmissoes = 0
        
        while base < len(pacotes):
            print(f"\nJanela atual: pacotes {base} a {base + tamanho_janela - 1}")
            
            while proximo_a_enviar < base + tamanho_janela and proximo_a_enviar < len(pacotes):
                pacote = pacotes[proximo_a_enviar]
                
                if self._simular_problema_rede(taxas['perda_pacote'], 'perda_pacote'):
                    print(f"Pacote {proximo_a_enviar} perdido no envio")
                else:
                    print(f"Enviando pacote {proximo_a_enviar}: '{pacote['dados']}'")
                    total_transmissoes += 1
                
                proximo_a_enviar += 1
            
            print("Processando confirmações...")
            time.sleep(1)
            
            ack_recebido = base
            while ack_recebido < proximo_a_enviar and ack_recebido < len(pacotes):
                if self._simular_problema_rede(taxas['perda_ack'], 'perda_ack'):
                    print(f"ACK {ack_recebido} perdido. Voltando ao pacote {base}")
                    proximo_a_enviar = base
                    break
                else:
                    print(f"ACK {ack_recebido} recebido")
                    if ack_recebido not in [p['numero'] for p in pacotes if p['dados'] in self.pacotes_recebidos]:
                        self.pacotes_recebidos.append(pacotes[ack_recebido]['dados'])
                    ack_recebido += 1
            
            base = ack_recebido
        
        self._mostrar_resultado(mensagem, total_transmissoes)
        self._registrar_execucao("Go-Back-N", mensagem)  
    
    def udp_simples(self, mensagem):
        print("\nINICIANDO UDP")
        print("=" * 40)
        
        taxas = self._gerar_taxas_aleatorias("udp")
        
        print(f"Taxas desta execução:")
        print(f"   Perda de pacotes: {taxas['perda_pacote']:.1%}")
        print(f"   Corrupção: {taxas['corrupcao']:.1%}")
        print(f"   Duplicação: {taxas['duplicacao']:.1%}")
        
        pacotes = self.criar_pacotes(mensagem)
        self.pacotes_recebidos = []
        problemas_ocorridos = []
        
        for i, pacote in enumerate(pacotes):
            print(f"\nEnviando pacote {i}: '{pacote['dados']}'")
            
            if self._simular_problema_rede(taxas['perda_pacote'], 'perda_pacote'):
                print("Pacote perdido")
                problemas_ocorridos.append(f"Pacote {i} perdido")
            
            elif self._simular_problema_rede(taxas['corrupcao'], 'corrupcao'):
                print("Pacote corrompido")
                problemas_ocorridos.append(f"Pacote {i} corrompido")
                if random.random() < 0.3:
                    dados_corrompidos = pacote['dados'][:-1] + '?'
                    self.pacotes_recebidos.append(dados_corrompidos)
                    print(f"Pacote {i} chegou corrompido: '{dados_corrompidos}'")
            
            elif self._simular_problema_rede(taxas['duplicacao'], 'duplicacao'):
                print("Pacote duplicado")
                self.pacotes_recebidos.append(pacote['dados'])
                self.pacotes_recebidos.append(pacote['dados'])
                problemas_ocorridos.append(f"Pacote {i} duplicado")
            
            else:
                print(f"Pacote {i} chegou: '{pacote['dados']}'")
                self.pacotes_recebidos.append(pacote['dados'])
        
        self._mostrar_resultado(mensagem, len(pacotes), problemas_ocorridos)
        self._registrar_execucao("UDP", mensagem)  # >>> ADIÇÃO DO RELATÓRIO FINAL
    
    def _mostrar_resultado(self, mensagem_original, metricas_extra=None, problemas=None):
        print(f"\n{'='*60}")
        print("RESULTADO DA TRANSFERÊNCIA:")
        print(f"Mensagem original: '{mensagem_original}'")
        
        mensagem_recebida = ''.join(self.pacotes_recebidos)
        print(f"Mensagem recebida:  '{mensagem_recebida}'")
        
        if mensagem_original == mensagem_recebida:
            print("Transferência bem-sucedida")
        else:
            print("Transferência com falhas")
        
        print(f"Pacotes enviados: {len(mensagem_original)}")
        print(f"Pacotes recebidos: {len(mensagem_recebida)}")
        
        if metricas_extra:
            if isinstance(metricas_extra, int):
                print(f"Total de transmissões: {metricas_extra}")
        
        if problemas:
            print(f"Problemas ocorridos: {len(problemas)}")
            for problema in problemas[:3]:
                print(f"   • {problema}")
            if len(problemas) > 3:
                print(f"   • ... e mais {len(problemas) - 3} problemas")
        
        eficiencia = len(mensagem_original) / max(metricas_extra, 1) if isinstance(metricas_extra, int) else 1
        print(f"Eficiência: {eficiencia:.1%}")
        print(f"{'='*60}")

   
    def _registrar_execucao(self, protocolo, mensagem):
        self.historico_execucoes.append({
            "protocolo": protocolo,
            "tamanho_mensagem": len(mensagem),
            "conteudo_inicial": mensagem[:40] + ("..." if len(mensagem) > 40 else "")
        })

    # >>> ADIÇÃO DO RELATÓRIO FINAL
    def gerar_relatorio_final(self):
        print("\n\n" + "="*70)
        print("RELATÓRIO FINAL DA EXECUÇÃO")
        print("="*70)

        for i, execucao in enumerate(self.historico_execucoes, 1):
            print(f"\nExecução {i}:")
            print(f"   Protocolo: {execucao['protocolo']}")
            print(f"   Tamanho da mensagem: {execucao['tamanho_mensagem']} caracteres")
            print(f"   Início da mensagem: {execucao['conteudo_inicial']}")

        print("\n" + "="*70)
        print("FIM DO RELATÓRIO FINAL")
        print("="*70)



def main():
    simulador = SimuladorTransporte()
    
    while True:
        print("\n" + "="*50)
        print("SIMULADOR CAMADA DE TRANSPORTE")
        print("TAXAS ALEATÓRIAS A CADA EXECUÇÃO")
        print("="*50)
        print("1. Stop-and-Wait")
        print("2. Go-Back-N")
        print("3. UDP")
        print("4. Sair")
        
        opcao = input("\nEscolha o protocolo (1-4): ")
        
        if opcao == '4':
            print("Gerando relatório final...")
            simulador.gerar_relatorio_final()  
            print("Saindo...")
            break
            
        mensagem = input("Digite a mensagem para enviar: ")
        
        if not mensagem.strip():
            mensagem = "MensagemTesteParaSimulacao123"
            print(f"Usando mensagem padrão: '{mensagem}'")
        
        if opcao == '1':
            simulador.stop_and_wait(mensagem)
        elif opcao == '2':
            simulador.go_back_n(mensagem)
        elif opcao == '3':
            simulador.udp_simples(mensagem)
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
