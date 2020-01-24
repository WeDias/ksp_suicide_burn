# ------------------------------------------------------------- #
#                                       KSP_SUICIDEBURN         #
#                                       Github:@WeDias          #
#                                    Licença: MIT License       #
#                                Copyright © 2020 Wesley Dias   #
# ------------------------------------------------------------- #

import krpc
from time import sleep

print('=' * 170)
print('''

888    d8P   .d8888b.  8888888b.        .d8888b.  888     888 8888888 .d8888b. 8888888 8888888b.  8888888888      888888b.   888     888 8888888b.  888b    888 
888   d8P   d88P  Y88b 888   Y88b      d88P  Y88b 888     888   888  d88P  Y88b  888   888  "Y88b 888             888  "88b  888     888 888   Y88b 8888b   888 
888  d8P    Y88b.      888    888      Y88b.      888     888   888  888    888  888   888    888 888             888  .88P  888     888 888    888 88888b  888 
888d88K      "Y888b.   888   d88P       "Y888b.   888     888   888  888         888   888    888 8888888         8888888K.  888     888 888   d88P 888Y88b 888 
8888888b        "Y88b. 8888888P"           "Y88b. 888     888   888  888         888   888    888 888             888  "Y88b 888     888 8888888P"  888 Y88b888 
888  Y88b         "888 888                   "888 888     888   888  888    888  888   888    888 888             888    888 888     888 888 T88b   888  Y88888 
888   Y88b  Y88b  d88P 888             Y88b  d88P Y88b. .d88P   888  Y88b  d88P  888   888  .d88P 888             888   d88P Y88b. .d88P 888  T88b  888   Y8888 
888    Y88b  "Y8888P"  888              "Y8888P"   "Y88888P"  8888888 "Y8888P" 8888888 8888888P"  8888888888      8888888P"   "Y88888P"  888   T88b 888    Y888 
                                                                                                                                                                BY: WEDIAS
''')
print('=' * 170)

# Conecxao com o foguete
conn = krpc.connect()
vessel = conn.space_center.active_vessel

# Definindo as constantes
constante_gravitacional = 6.674184 * 10 ** -11
massa_planeta = vessel.orbit.body.mass
raio_planeta = vessel.orbit.body.equatorial_radius
nome_astro = vessel.orbit.body.name
tem_atmosfera = vessel.orbit.body.has_atmosphere
tamanho_atmosfera = 0
if tem_atmosfera:
    tamanho_atmosfera = vessel.orbit.body.atmosphere_depth

try:
    vessel.control.sas = True
    vessel.control.rcs = True
    sleep(0.1)
    vessel.control.sas_mode = vessel.control.sas_mode.retrograde
    print('NAVE COM SAS_RETROGRADE, PILOTO AUTOMATICO ATIVADO')
    print('SAS = [ONLINE]\nRCS = [ONLINE]')

    # Contagem regressiva de 10s
    for c in range(10, 0, - 1):
        print(f'\rCONTAGEM REGRESSIVA: {c}', end='')
        sleep(1)
    print('\rPILOTO AUTIOMATICO = [ONLINE]')

except:
    print('NAVE SEM SAS_RETROGRADE, PILOTO SEMI-AUTOMATICO ATIVADO. PILOTO MANTENHA A NAVE NO RETROGRADE')
    print('PILOTO AUTOMATICO = [OFFLINE]')

print('\rSUICIDEBURN = [ONLINE]')

# Instrucoes de pouso | Computador de bordo
gear = caindo = False
while True:
    # Dados de telemetria
    altura_mar = vessel.flight().mean_altitude
    altura_chao = vessel.flight().surface_altitude
    periastro = vessel.orbit.periapsis_altitude
    vel_superficie = vessel.flight(vessel.orbit.body.reference_frame).speed
    retrograde = vessel.flight().retrograde
    aceleracao_gravidade = constante_gravitacional * massa_planeta / (raio_planeta + altura_mar) ** 2
    twr = vessel.available_thrust / (vessel.mass * aceleracao_gravidade)
    aceleracao = twr * aceleracao_gravidade
    tempo_ate_chao = altura_chao / vel_superficie
    tempo_de_queima = vel_superficie / aceleracao
    situacao = vessel.situation.name
    print(f'\rACELERACAO:{aceleracao:.2f}M/S^2 | ALTURA:{altura_chao:.2f}M | VELOCIDADE:{vel_superficie:.2f}M/S | TEMPOATECHAO:{int(tempo_ate_chao)}S | TEMPODEQUEIMA:{int(tempo_de_queima)}S | SITU:{situacao.upper()}', end='')

    # Ativacao de paraquedas
    if tem_atmosfera and altura_mar <= (tamanho_atmosfera / 4):
        vessel.control.parachutes = True

    # Pernas de pouso e luzes
    if tempo_ate_chao <= 3 and not gear:
        vessel.control.gear = True
        vessel.control.lights = True

    # Separacao de estagio
    if vessel.available_thrust == 0 and vessel.control.current_stage != 0:
        print(f'\rSEPARAÇÃO DE ESTÁGIO')
        vessel.control.activate_next_stage()

    # controle da pontencia dos motores
    if not caindo and situacao in ['orbiting', 'sub_orbital', 'flying']:
        if tem_atmosfera:
            vessel.control.brakes = True
            if periastro >= (tamanho_atmosfera - 10000):
                vessel.control.throttle = 1
            else:
                vessel.control.throttle = 0
        else:
            if periastro <= 0:
                sleep(1)
                vessel.control.throttle = 0
                caindo = True
            else:
                vessel.control.throttle = 1

    elif tempo_ate_chao <= tempo_de_queima + 0.5:
        if tem_atmosfera:
            if tempo_ate_chao <= tempo_de_queima + 0.5 and altura_mar <= (tamanho_atmosfera / 4):
                vessel.control.throttle = 1
            else:
                vessel.control.throttle = 0
        else:
            vessel.control.throttle = 1

    # Pouso com sucesso !
    else:
        vessel.control.throttle = 0
        if vessel.situation.name in ['landed', 'splashed']:
            vessel.auto_pilot.engage()
            vessel.auto_pilot.target_pitch_and_heading(90, 90)
            print(f'\nA NAVE "{vessel.name.upper()}" POUSOU COM SUCESSO EM {nome_astro.upper()}')
            input('PRESSIONE ENTER PARA VOLTAR')
            vessel.auto_pilot.disengage()
            vessel.control.sas = True
            if vessel.recoverable:
                input('PRESSIONE ENTER PARA VOLTAR E RECUPERAR A NAVE')
                vessel.recover()
            break
