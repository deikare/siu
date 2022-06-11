# Autor: Mariusz Kamola
# encoding: utf8
import os
import argparse
import numpy as np
from tensorflow.keras.models import load_model
from turtlesim.msg import Pose

parser = argparse.ArgumentParser()
parser.add_argument('--multi',action="store_true",help='flaga testowania wieloagentowego (domyślnie: jednoagentowe)')
parser.set_defaults(multi=False)
parser.add_argument('--realtime',action="store_true",help='flaga sterowania prędkościowego (domyślnie: ruch skokowy)')
parser.set_defaults(realtime=False)
parser.add_argument('--detect_collision',action="store_true",help='flaga wykrywania kolizji (domyślnie: nieaktywne)')
parser.set_defaults(detect_collision=False)
parser.add_argument('--n_agents',type=int,default=1,help='maks. liczba agentów (domyślnie: 1)')
parser.add_argument('--routes',type=str,default='routes.csv',help='nazwa pliku scenariusza (domyślnie: routes.csv)')
parser.add_argument('--n_steps',type=int,default=5_000,help='liczba kroków do wykonania przez agenta (domyślnie: 5 tys.)')
parser.add_argument('--goal_eps',type=float,default=2.5,help='odl. od celu oznaczająca jego osiągięcie (domyślnie: 2,5 m)')
parser.add_argument('--res_file',type=str,default='results.csv',help='nazwa pliku, do którego dopisać wyniki (domyślnie: results.csv)')
parser.add_argument('model_names',nargs=argparse.REMAINDER)

args = parser.parse_args()

if args.multi:
    from turtlesim_env_multi import provide_env
    from dqn_multi import DqnMulti as Dqn
else:
    from turtlesim_env_single import provide_env
    from dqn_single import DqnSingle as Dqn

# uruchamia krążenie żółwia po planszy wg 1. scenariusza,
# zliczając średnią liczbę udanych obiegów na 1 uruchomienie
# mierzoną liczbą osiągniętych celów pośrednich

env=provide_env()
env.setup(args.routes,agent_cnt=args.n_agents)          # wczytanie tras i zarezerwowanie 1 agenta
env.PI_BY=3                                             # pocz. odchyłka od azymutu na cel losowo w przedziale +-pi/3
env.DETECT_COLLISION=args.detect_collision
dqn=Dqn(env,'test')                                     # utworzenie klasy uczącej (tam są metody wyliczania sterowania)

for s in args.model_names:                              # ocena dla każdego modelu - argumentu wywołania
    model_name = os.path.splitext(os.path.split(s)[-1])[0]
    print(f'model {model_name}')
    dqn.model=load_model(s)                             # załadowanie/podmiana modelu
    env.MAX_STEPS=args.n_steps+1
    agents=env.reset()
    max_test_steps=args.n_steps
    if args.multi:                                      # jeśli wieloagentowo, przemnóż limit kroków przez liczbę agentów
        max_test_steps*=len(agents)
    step=0                                              # licznik wszystkich kroków symulacji
    section_ids={t:a.sec_id for t,a in agents.items()}  # pocz. indeksy segmentów (celu) tras poszczególnych agentów
    lap=0                                               # łączna liczba cykli dla wszystkich agentów
    to_restart=set()                                    # nazwy aktywnych agentów do reaktywacji
    ride=len(agents)                                    # licznik łącznej liczby przejazdów
    current_states = {tname: agent.map for tname, agent in agents.items()}
    last_states = {}
    for tname,map in current_states.items():            # duplikat bieżącego stanu jako stan poprzedni
        last_states[tname] = [i.copy() for i in map]
    while step<max_test_steps:                          # jednoczesny krok symulacji wszystkich agentów
        ride+=len(to_restart)
        agents=env.reset(to_restart,sections=['random' for i in to_restart])  # odnowienie agentów po awarii
        for tname in to_restart:                        # inicjalizacja sytuacji reaktywowanych żółwi
            section_ids[tname]=agents[tname].sec_id     # pierwszy cel po restarcie żółwia
            current_states[tname]=agents[tname].map     # początkowy obraz sytuacyjny
            last_states[tname] = [i.copy() for i in agents[tname].map]
        # wybór decyzji i zamiana decyzji na wartości sterowań
        controls={t:np.argmax(dqn.decision(dqn.model, last_states[t], current_states[t])) for t in agents}
        actions={tname: dqn.ctl2act(control) for tname, control in controls.items()}
        # odpowiedź środ. 1-agentowego to trzeba włożyć w słownik, żeby zachować dalszą zgodność kodu
        scene=env.step(actions,realtime=args.realtime) if args.multi else {list(agents.keys())[0]:env.step(actions,realtime=args.realtime)}
        to_restart=set()                                # komu zafundować restart
        step+=len(agents)                               # zliczanie wszystkich kroków agentów
        for tname,(new_state,reward,done) in scene.items():         # przestawienie zółwi na kolejne cele
            if done:                                    # awaria agenta -> restart
                to_restart.add(tname)
                print(f'{tname} X')
                continue
            last_states[tname] = current_states[tname]  # przejście do nowego stanu
            current_states[tname] = new_state           # z zapamiętaniem poprzedniego
            route=env.routes[agents[tname].route]       # trasa tego żółwia
            rlen=len(route)                             # liczba celów pośr. na trasie żółwia
            fds = np.zeros(rlen)                        # odległości od wszystkich celów, szukamy najbliższego
            for goal_id in range(rlen):
                if (goal_id+1)%rlen==section_ids[tname]:            # pomiń ostatnio osiągnięty cel
                    fds[goal_id]=np.inf
                else:                                   # odl. do celu
                    fds[goal_id]=np.sqrt((route[goal_id][5]-env.agents[tname].pose.x)**2+(route[goal_id][6]-env.agents[tname].pose.y)**2)
            if np.min(fds)<args.goal_eps:               # osiągnięto jakiś cel
                if np.argmin(fds)!=section_ids[tname]:  # cel niewłaściwy
                    to_restart.add(tname)
                    print(f'{tname} -> X {np.argmin(fds)}')
                else:                                   # cel właściwy
                    section_ids[tname]=(section_ids[tname]+1)%rlen
                    env.agents[tname].goal_loc=Pose(x=route[section_ids[tname]][5],y=route[section_ids[tname]][6])
                    lap+=1.0/rlen                       # każdy osiągnięty cel zwiększa ułamkowo licznik okrążeń
                    print(f'{tname} -> V {section_ids[tname]}')
    print(f'{lap} okrazen, {ride} prob, {lap/ride:.2f} okrazen na 1 probe')
    with open(args.res_file,'a') as f:
        f.write(f'{lap} {ride} {lap/ride:.2f} {model_name}\n')
