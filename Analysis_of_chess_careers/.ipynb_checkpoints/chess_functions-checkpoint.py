import numpy as np
import time

def get_ELO_bins(game_type_,X):
    
    sorted_X=sorted(X)

    #     a=sorted_X[int(np.floor(.01*len(sorted_X)))]
    #     b=sorted_X[int(np.floor(.99*len(sorted_X)))]
    a=0;b=len(sorted_X)-1
    bins_=np.floor(np.linspace(a,b,5))
    sorted_X=np.array(sorted_X)
    bins_=np.floor(sorted_X[bins_.astype('int')]).astype('int')
#     bins_[len(bins_)-1]=sorted_X[len(sorted_X)-1]


    return bins_

# calling function



def importPGNData(filepath):
    """This function returns the data read as a string"""
    with open(filepath) as f:
        return f.readlines()
def getEdgePoints(data):
    """This function returns the start and end indices for each game in the PGN"""
    ends=[]
    starts=[]
    for n,l in enumerate(data):
        if l.startswith("[Event"):
            if n!=0:
                ends.append(n - 1)
            starts.append(n)
        elif (n==len(data)-1):
            ends.append(n)

    return (starts,ends)

path_dicts='/mnt/sdb1/sandeep/dicts_chess/'

def get_suboptimality(player_op_wins_suboptimal,player_op_counts_suboptimal,player_elo_FILTER_suboptimal,store_career_indices):
    t_ic = time.time();

    career_in_focus=len(store_career_indices)
    player_op_w_suboptimal={'1':{'op1':[],'op2':[]},'2':{'op1':[],'op2':[]},'3':{'op1':[],'op2':[]}}
    player_op_c_suboptimal={'1':{'op1':[],'op2':[]},'2':{'op1':[],'op2':[]},'3':{'op1':[],'op2':[]}}
    player_op_frac_times_played_suboptimal={'1':{'op1':[],'op2':[]},'2':{'op1':[],'op2':[]},'3':{'op1':[],'op2':[]}}

    for it in range(career_in_focus-1):

        for game_type_ in [1,2,3]:         
            g_type_=str(game_type_)

            openings_=player_op_counts_suboptimal[g_type_][it]

            if openings_==-1:
                player_op_w_suboptimal[g_type_]['op'+str(1)].append(-1)
                player_op_w_suboptimal[g_type_]['op'+str(2)].append(-1)
                player_op_c_suboptimal[g_type_]['op'+str(1)].append(-1)
                player_op_c_suboptimal[g_type_]['op'+str(2)].append(-1)
                player_op_frac_times_played_suboptimal[g_type_]['op'+str(1)].append(-1)
                player_op_frac_times_played_suboptimal[g_type_]['op'+str(2)].append(-1)
            else:

                openings_keys=[x[0] for x in openings_]
                openings_count=[x[1] for x in openings_]
                if len(openings_keys)>=2:
                    for op__ in range(0,2):

                        player_total_games=openings_count[op__]


                        if op__ in player_op_wins_suboptimal[g_type_][it].keys():
                            player_wins=player_op_wins_suboptimal[g_type_][it][openings_keys[op__]]
                        else:
                            player_wins=-1


                        player_op_w_suboptimal[g_type_]['op'+str(op__+1)].append(player_wins)
                        player_op_c_suboptimal[g_type_]['op'+str(op__+1)].append(player_total_games)
                        player_op_frac_times_played_suboptimal[g_type_]['op'+str(op__+1)].append(player_total_games/sum(openings_count))



                else:
                    player_op_w_suboptimal[g_type_]['op'+str(1)].append(-1)
                    player_op_w_suboptimal[g_type_]['op'+str(2)].append(-1)
                    player_op_c_suboptimal[g_type_]['op'+str(1)].append(-1)
                    player_op_c_suboptimal[g_type_]['op'+str(2)].append(-1)
                    player_op_frac_times_played_suboptimal[g_type_]['op'+str(1)].append(-1)
                    player_op_frac_times_played_suboptimal[g_type_]['op'+str(2)].append(-1)

        if it % 50000 == 0:
            t_oc = time.time();
            print('career number=''--'+str(it/(len(store_career_indices)-1))+'--i.e.-'+str(it)+'/'+str(len(store_career_indices)-1)+'----time (s)-'+str(round(t_oc-t_ic,2))+'',end='\r')
            with open("/mnt/sdb1/sandeep/0. Careers in chess/a_entropy_calc.txt", "a") as file_object:
                file_object.write('--'+str(it/(len(store_career_indices)-1))+'--i.e.-'+str(it)+'/'+str(len(store_career_indices)-1)+'----time (s)-'+str(round(t_oc-t_ic,2))+'\n')


    ###### making np arrays from lists
    for game_type_ in [1,2,3]:         
        g_type_=str(game_type_)
        player_op_w_suboptimal[g_type_]['op'+str(1)]=np.array(player_op_w_suboptimal[g_type_]['op'+str(1)])
        player_op_w_suboptimal[g_type_]['op'+str(2)]=np.array(player_op_w_suboptimal[g_type_]['op'+str(2)])
        player_op_c_suboptimal[g_type_]['op'+str(1)]=np.array(player_op_c_suboptimal[g_type_]['op'+str(1)])
        player_op_c_suboptimal[g_type_]['op'+str(2)]=np.array(player_op_c_suboptimal[g_type_]['op'+str(2)])
        player_op_frac_times_played_suboptimal[g_type_]['op'+str(1)]=np.array(player_op_frac_times_played_suboptimal[g_type_]['op'+str(1)])
        player_op_frac_times_played_suboptimal[g_type_]['op'+str(2)]=np.array(player_op_frac_times_played_suboptimal[g_type_]['op'+str(2)])


    return player_op_w_suboptimal,player_op_c_suboptimal,player_op_frac_times_played_suboptimal



