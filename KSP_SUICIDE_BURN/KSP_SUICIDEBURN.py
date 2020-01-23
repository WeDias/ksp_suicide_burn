#-------------------------------------------------------------#
#                                      KSP SUICIDEBURN        #
#                                      Github:@WeDias         #
#                                   Licença: MIT License      #
#                               Copyright © 2020 Wesley Dias  #
#-------------------------------------------------------------#

import krpc

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
                                                                                                                                                                BY: WeDias
''')
print('=' * 170)

# Conecxao com o foguete
conn = krpc.connect()
vessel = conn.space_center.active_vessel

constante_gravitacional = 6.674184 * 10 ** -11
massa_planeta = vessel.orbit.body.mass
raio_planeta = vessel.orbit.body.equatorial_radius


try:
    vessel.control.sas_mode = vessel.control.sas_mode.retrograde
    print('Nave Com SAS_Retrograde, controle automatico ativado')
except:
    print('Nave sem SAS_Retrograde, controle manualmente a nave até o retrograde, e o software faz o resto')

print('SUICIDEBURN = ON')

gear = False
vessel.control.brakes = True
while True:
    altura_mar = vessel.flight().mean_altitude
    altura_chao = vessel.flight().surface_altitude
    vel_superficie = vessel.flight(vessel.orbit.body.reference_frame).speed
    retrograde = vessel.flight().retrograde
    aceleracao_gravidade = constante_gravitacional * massa_planeta / (raio_planeta + altura_mar) ** 2
    twr = vessel.available_thrust / (vessel.mass * aceleracao_gravidade)
    aceleracao = twr * aceleracao_gravidade
    tempo_ate_chao = altura_chao / vel_superficie
    tempo_de_queima = vel_superficie / aceleracao
    print(f'\rAceleracao:{aceleracao:.2f}m/s^2 Altura:{altura_chao:.2f}m | Velocidade:{vel_superficie:.2f}m/s | TempoAteChao:{int(tempo_ate_chao)}s | TempoDeQueima:{int(tempo_de_queima)}s', end='')

    if tempo_ate_chao <= 3 and not gear:
        vessel.control.gear = True
        vessel.control.lights = True

    if vessel.available_thrust == 0:
        print(f'\rSEPARAÇÃO DE ESTÁGIO')
        vessel.control.activate_next_stage()

    if tempo_ate_chao <= tempo_de_queima + 0.5:
        vessel.control.throttle = 1

    else:
        vessel.control.throttle = 0
        if vessel.situation.name in ['landed', 'splashed']:
            print('\nPousei')
            break
