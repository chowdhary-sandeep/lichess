### Game to temporal-dictionary
import time
import pandas as pd
import glob
import numpy as np
import timeit
import pickle
import ast
from datetime import datetime
from collections import Counter
from scipy import stats

def simulate_game_only_activity_VI(game_,MOVES_,dict_board0,dict_piece_loc0,board_rows_,pieces_,board_cols_):
    
    array_activities=[]
#     dict_activities={'wP':[],'wR':[],'wB':[],'wN':[],'wQ':[],'wK':[],\
#                      'bP':[],'bR':[],'bB':[],'bN':[],'bQ':[],'bK':[]}
    
    
    dict_pieces_endgame=-1
    points_on_board_endgame=[-1,-1]
    endgame_reached=0
    move_on_which_endgame_reached=-1
    total_promotions_=0
    first_promotion_move=-1
    points_on_board=[39,39] # black and white
    dict_piece_values={'P':1,'N':3,'B':3,'R':5,'Q':9};
    color_=['b','w']
    dict_board=dict_board0.copy()
    dict_piece_loc=dict_piece_loc0.copy()
    Lifetimes_=[]
    # for it  in range(len(game_)-2):
    for it  in range(MOVES_):
        array_activities.append(-1)
        dict_board_Tminus1=dict_board.copy()
        move_=game_[it]
        is_odd_= int( (it+1) % 2 !=0);    is_white_move=is_odd_
#         print(move_)
            
    #     print(int(move_[0] in board_rows_)+ int(move_[0] in pieces_ )+  int(move_[0] == 'O'))
    #----------------------------------------------------------------------------------
    # pawn move
    #----------------------------------------------------------------------------------
        if move_[0] in board_rows_: # pawn move
            promotion_=0
#             print(move_,'Pawn Move')
        #----------------------------------------------------------------------------------
    
            #----------------------------------------------------------------------------------
            # pawn taken off or NOT?
            #----------------------------------------------------------------------------------        
            if 'x' in move_: # piece or pawn comes off-board
                
                takes_=1
                destination_=move_[2:4]
#                 if destination_[1]=='1' or destination_[1]=='8':
                if '=' in move_:
                    promotion_=1
                    new_piece_=move_[5]
                    
                                
                if is_white_move==1:
#                    
                    source_=move_[0]+str(ord((move_[3]))-48-1)
                    source_2=move_[0]+str(ord((move_[3]))-48-2)
                else:
                    source_=move_[0]+str(ord((move_[3]))-48+1)
                    source_2=move_[0]+str(ord((move_[3]))-48+2)

            

            else:
                takes_=0
                destination_=move_[0:2]
#                 if destination_[1]=='1' or destination_[1]=='8':
                if '=' in move_:
                    promotion_=1
                    new_piece_=move_[3]
#                     print(move_,'----------------PROMOTION-------------------to--',new_piece_)
                    
                    
                    
                if is_white_move==1:
                    
                    source_=move_[0]+str(ord((move_[1]))-48-1)
                    source_2=move_[0]+str(ord((move_[1]))-48-2)
                else:

                    source_=move_[0]+str(ord((move_[1]))-48+1)
                    source_2=move_[0]+str(ord((move_[1]))-48+2)
#             print(source_,source_2,destination_)
            if promotion_==1:
                new_piece_=color_[is_white_move]+new_piece_+'z'
                if total_promotions_==0:
                    first_promotion_move=it
                total_promotions_=total_promotions_+1
        
            #------------------------
            # MOVING THE PAWN
            #------------------------
            piece_to_move=dict_board[source_]
            if piece_to_move=='':
                piece_to_move=dict_board[source_2]
                
                source_=source_2
            if takes_==1:
                Lifetimes_.append([dict_board[destination_],it+1])
                if (not dict_board[destination_] =='') and (not dict_board[destination_][1] =='K'):
                    points_lost=dict_piece_values[dict_board[destination_][1]]
                    points_on_board[abs(1-is_white_move)]=points_on_board[abs(1-is_white_move)]-points_lost
                if (points_on_board[0]<13) and (points_on_board[1]<13) and (endgame_reached==0):
                    points_on_board_endgame=points_on_board.copy()
                    endgame_reached=1
                    move_on_which_endgame_reached=it
                    dict_pieces_endgame=dict_board.copy()

                    

                dict_piece_loc[dict_board[destination_]]=''                


            dict_piece_loc[piece_to_move]=destination_
            if not piece_to_move=='':
#                 dict_activities[piece_to_move[0:2]].append(it+1)
                array_activities[it]=piece_to_move[0:2]
            dict_board[source_]='';                           
            dict_board[destination_]=piece_to_move
            if points_on_board[0]<13 and points_on_board[1]<13:
                dict_pieces_endgame=dict_board
            if promotion_==1:
                dict_board[destination_]=new_piece_
                dict_piece_loc[piece_to_move]=''
                dict_piece_loc[new_piece_]=destination_
            
#             print('piece',piece_to_move,source_,destination_)

            # takes_=0: c3 pawn on same file moved 1 or 2 spaces,
            # takes_=1: cxd3, pawn on file c takes piece on d3 
            #(en passant? Not tractable, 
            # you will have to check if place is empty then if there was a pawn on d4 and no promoted piece on d3)



     
            
            
            
            
            

    #----------------------------------------------------------------------------------
    # piece move
    #----------------------------------------------------------------------------------

        elif move_[0] in pieces_:   # piece move
#             print(move_,'Piece Move')

            piece_=move_[0]
            #----------------------------------------------------------------------------------
            # piece taken off or NOT?
            #----------------------------------------------------------------------------------        
            if 'x' in move_: # piece or pawn comes off-board                
                takes_=1
            else:
                takes_=0


            #----------------------------------------------------------------------------------
            # Knights, Bishops and Rooks need to treated different than Queens and Kings
            #----------------------------------------------------------------------------------        

            if piece_ in ['N','B','R']:


            #----------------------------------------------------------------------------------
            # all moves, takes, check, checkmate, forget eval
            # Nc3, Nxc3, Nac3, Naxc3, N2c3, N2xc3,  Na2c3, Na2xc3, Nc3+, Nc3#, Nxc3, Nac3, Naxc3, N2c3, N2xc3,  Na2c3, Na2xc3, 
            #----------------------------------------------------------------------------------       

            #----------------------------------------------------------------------------------
            # takes_=0: Nc3, Nac3, N2c3, Na2c3
            # takes_=1: Nxc3, Naxc3, N2xc3, Na2xc3

                move_type_=-1
                if (move_[1+takes_] in board_rows_ and move_[2+takes_] in board_cols_ and (len(move_)==3+takes_)):
                    move_type_=1
                    destination_=move_[1+takes_:3+takes_]
                elif (move_[1+takes_] in board_rows_ and move_[2+takes_] in board_cols_ and (len(move_)==4+takes_)):
                    if move_[3+takes_]=='+' or move_[3+takes_]=='#' :
                        move_type_=1    
                        destination_=move_[1+takes_:3+takes_]
                elif (move_[1] in board_rows_ and move_[2+takes_] in board_rows_):
                    move_type_=2
                    destination_=move_[2+takes_:4+takes_]
                elif (move_[1] in board_cols_ and move_[2+takes_] in board_rows_):
                    move_type_=3
                    destination_=move_[2+takes_:4+takes_]
                elif (move_[1] in board_rows_ and move_[2] in board_cols_ and move_[2+takes_] in board_rows_):
                    move_type_=4
                    destination_=move_[3+takes_:5+takes_]

            #----------------------------------------------------------------------------------
            # source location of piece (only for dupliate pieces)
            #----------------------------------------------------------------------------------
            
                loc1=dict_piece_loc[color_[is_white_move]+piece_+'1'];
                loc2=dict_piece_loc[color_[is_white_move]+piece_+'2'];
#                 print(loc1,loc2)

                possible_=[]
                for loc_ in [loc1,loc2]:
                    
                    if not loc_ =='': #'Piece is onboard and should be considered'
                        dx=abs(ord(destination_[0])-ord(loc_[0]))
                        dy=abs(ord(destination_[1])-ord(loc_[1]))

                        if piece_=='N':
                            if ((dx==1 and dy==2) or (dx==2 and dy==1)) and (not loc_ ==''):
                                possible_.append(1)
                            else:
                                possible_.append(0)


                        elif piece_=='B':
                            if (dx==dy) and (not loc_ ==''):
                                possible_.append(1)
                            else:
                                possible_.append(0)

                        elif piece_=='R':
    #                         print('loc=',loc_,', dest=',destination_)
                            something_in_between=0;
                            if not loc_=='':
                                if loc_[0]==destination_[0]:
                                    l1=ord(loc_[1]);l2=ord(destination_[1])
                                    if abs(l1-l2)==1:
                                        something_in_between=0;
                                    else:
                                        t_file_=loc_[0]
                                        if l1<l2:
                                            for i_ in range(l2-l1-1):
                                                t_rank_=chr(l1+i_+1)
                                                t_pos_=t_file_+t_rank_
                                                if not dict_board[t_pos_]=='':
                                                    something_in_between=1
                                        else:
                                            for i_ in range(l1-l2-1):
                                                t_rank_=chr(l2+i_+1)
                                                t_pos_=t_file_+t_rank_
                                                if not dict_board[t_pos_]=='':
                                                    something_in_between=1            

                                elif loc_[1]==destination_[1]:
                                    l1=ord(loc_[0]);l2=ord(destination_[0])
                                    if abs(l1-l2)==1:
                                        something_in_between=0;
                                    else:
                                        t_rank_=loc_[1]
                                        if l1<l2:
                                            for i_ in range(l2-l1-1):
                                                t_file_=chr(l1+i_+1)
                                                t_pos_=t_file_+t_rank_

                                                if not dict_board[t_pos_]=='':
                                                    something_in_between=1        
                                        else:
                                            for i_ in range(l1-l2-1):
                                                t_file_=chr(l2+i_+1)
                                                t_pos_=t_file_+t_rank_
                                                if not dict_board[t_pos_]=='':
                                                    something_in_between=1
                            if (dx==0 or dy==0) and (not loc_ =='') and something_in_between==0:
                                possible_.append(1)

                            else:
                                possible_.append(0)         
                    else:
                        possible_.append(0)         
                        
                if move_type_==1:
                    if possible_[0]==1:
                        source_=loc1
                    else:
                        source_=loc2
                    

                elif move_type_==2:
                    if move_[1] in loc1:
                        source_=loc1
                    else:
                        source_=loc2

                elif move_type_==3:
                    if move_[1] in loc1:
                        source_=loc1
                    else:
                        source_=loc2

                elif move_type_==4:
                    if move_[1:3] == loc1:
                        source_=loc1
                    else:
                        source_=loc2
            
            
#                 if  piece_=='R':
#                     print('possible' ,possible_,', dest=',destination_,'source=',loc1,loc2,source_)
#                     print('something_in_bet',something_in_between,'possible_',possible_)

#                     print('movetype' ,move_type_,takes_)
       

                         


                
                
                
                

        #----------------------------------------------------------------------------------                
        # else: # Queen move/ King move
        #----------------------------------------------------------------------------------
            else:
                source_=dict_piece_loc[color_[is_white_move]+piece_]
            #----------------------------------------------------------------------------------
            # takes_=0: Qc3, Qac3, Q2c3, Qa2c3
            # takes_=1: Qxc3, Qaxc3, N2xc3, Na2xc3

                move_type_=-1
                if (move_[1+takes_] in board_rows_ and move_[2+takes_] in board_cols_ and (len(move_)==3+takes_)):
                    move_type_=1
                    destination_=move_[1+takes_:3+takes_]
                elif (move_[1+takes_] in board_rows_ and move_[2+takes_] in board_cols_ and (len(move_)==4+takes_)):
                    if move_[3+takes_]=='+' or move_[3+takes_]=='#':
                        move_type_=1    
                        destination_=move_[1+takes_:3+takes_]
                elif (move_[1] in board_rows_ and move_[2+takes_] in board_rows_):
                    move_type_=2
                    destination_=move_[2+takes_:4+takes_]
                elif (move_[1] in board_cols_ and move_[2+takes_] in board_rows_):
                    move_type_=3
                    destination_=move_[2+takes_:4+takes_]
                elif (move_[1] in board_rows_ and move_[2] in board_cols_ and move_[2+takes_] in board_rows_):
                    move_type_=4
                    destination_=move_[3+takes_:5+takes_]       

                possible_=[]

                if not source_=='':       
                    dx=abs(ord(destination_[0])-ord(source_[0]))
                    dy=abs(ord(destination_[1])-ord(source_[1]))

                    if piece_=='Q':
                        if (dx==dy) or (dx==0 or dy==0):
                            possible_.append(1)
                    elif piece_=='K':
                        possible_.append(1)

   



        
    
    
    
    
    
        #----------------------------------------------------------------------------------
        # MOVING THE PIECE
        #----------------------------------------------------------------------------------                        
#             print('possible' ,possible_,', dest=',destination_,'source=',loc1,loc2,source_)
#             print('movetype' ,move_type_,takes_)

            if sum(possible_)>0:   

                if not source_=='':
                    piece_to_move=dict_board[source_]
                    if not piece_to_move=='':
#                         dict_activities[piece_to_move[0:2]].append(it+1)
                        array_activities[it]=piece_to_move[0:2]

                    if takes_==1:
                        Lifetimes_.append([dict_board[destination_],it+1])
                        if (not dict_board[destination_] =='') and (not dict_board[destination_][1] =='K'):
                            points_lost=dict_piece_values[dict_board[destination_][1]]
                            points_on_board[abs(1-is_white_move)]=points_on_board[abs(1-is_white_move)]-points_lost
                        dict_piece_loc[dict_board[destination_]]=''
                        if (points_on_board[0]<13) and (points_on_board[1]<13) and (endgame_reached==0):
                            points_on_board_endgame=points_on_board.copy()
                            endgame_reached=1
                            move_on_which_endgame_reached=it
                            dict_pieces_endgame=dict_board.copy()
                            
                    if not piece_to_move =='':
                        dict_piece_loc[piece_to_move]=destination_
                        dict_board[source_]='';                           
                        dict_board[destination_]=piece_to_move

                        if points_on_board[0]<13 and points_on_board[1]<13:
                            dict_pieces_endgame=dict_board
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
    #----------------------------------------------------------------------------------
    # castling move
    #----------------------------------------------------------------------------------

        elif move_[0] == 'O':      # castles: just change the position of rook and king depending on if its long or short 
#             print(move_,'Castling Move')
            
            piece_to_move1=color_[is_white_move]+'K';
            piece_to_move2=color_[is_white_move]+'R';
            
#             dict_activities[piece_to_move1[0:2]].append(it+1)
            array_activities[it]=piece_to_move1[0:2]
            
#             dict_activities[piece_to_move2[0:2]].append(it+1)

            if  move_=='O-O' and is_white_move==1:
                dict_piece_loc[dict_board['e1']]='g1';            dict_piece_loc[dict_board['h1']]='f1';
                dict_board['g1']=dict_board['e1'];                dict_board['f1']=dict_board['h1'];
                dict_board['e1']='';                              dict_board['h1']='';            
            elif  move_=='O-O-O' and is_white_move==1:
                dict_piece_loc[dict_board['e1']]='c1';            dict_piece_loc[dict_board['a1']]='d1';
                dict_board['c1']=dict_board['e1'];                dict_board['d1']=dict_board['a1'];
                dict_board['e1']='';                              dict_board['a1']='';            
            if  move_=='O-O' and is_white_move==0:
                dict_piece_loc[dict_board['e8']]='g8';            dict_piece_loc[dict_board['h8']]='f8';
                dict_board['g8']=dict_board['e8'];                dict_board['f8']=dict_board['h8'];
                dict_board['e8']='';                              dict_board['h8']='';            
            elif  move_=='O-O-O' and is_white_move==0:
                dict_piece_loc[dict_board['e8']]='c8';            dict_piece_loc[dict_board['a8']]='d8';
                dict_board['c8']=dict_board['e8'];                dict_board['d8']=dict_board['a8'];
                dict_board['e8']='';                              dict_board['h8']='';     
#     dict_activities=[{x:np.array(dict_activities[x])} for x in dict_activities.keys()]
    array_activities=np.array(array_activities)

    return array_activities

# returns dict_board: pieces on the board, with pieces and lifetimes