package student_player;

import java.util.List;
import tablut.TablutBoardState;
import tablut.TablutMove;

public class Node {
	//Board
	TablutBoardState state;
	//Team making move at this depth
	int team;
	//Current depth
    int depth;
    //Depth we're building tree to
    int desiredDepth;
    //The best move in this section of search tree
    TablutMove bestMove;
    //Evaluation object
    Evaluation eval;
    //Constants for alpha-beta pruning
    double alpha;
    double beta;
    //Original team, i.e. team that started the search tree
    int orgTeam;
    
    //Constructor
    //Set up variables
    public Node(TablutBoardState state,int depth,int player,double alpha,double beta,int orgTeam,int searchDepth) {
    	this.state = state;
    	this.depth = depth;
    	this.team = player;
    	this.alpha = alpha;
    	this.beta = beta;
    	this.orgTeam = orgTeam;
    	this.desiredDepth = searchDepth;
    }
    
    //Minimax with alpha beta pruning
    public double alphaBeta(){
    	//Check whether board has a winner 
    	if(state.getWinner() == orgTeam){
        	return 10000;
        }else if(state.getWinner() == (orgTeam-1)*-1){
        	return -10000;
        }
    	//If we've reached the correct depth evaluate the board
    	if (depth == desiredDepth){
    		eval = new Evaluation(state);
    		return eval.boardScore(orgTeam);
    	}
    	//Otherwise, the game represented by this board is not finished and is not at the desired depth
    	//Therefore continue expanding search tree
    	
    	//Maximizing player
		if (depth % 2 == 0){
			double value = Double.NEGATIVE_INFINITY;
			//get every possible move
    		List<TablutMove> options = state.getAllLegalMoves();
    		//Iterate through moves
    		for (TablutMove move : options) {
    			//Clone board
    	        TablutBoardState childState = (TablutBoardState) state.clone();
    	        //Process particular move with parent boardState
    	        childState.processMove(move);
    	        double score = 0;
    	        //Create child Node in search tree
    	        Node childNode = new Node(childState,(depth+1),(team-1)*-1,alpha,beta,orgTeam,desiredDepth);
    	        score = childNode.alphaBeta(); //this gets the value of the board
    	        //If child is better than our best option, update best move
    	        if (score > value){
    	        	value = score;
    	        	bestMove = move;
    	        }
    	        //Update alpha if best score is higher
    	        if (value > alpha){
    	        	alpha = value;
    	        }
    	        //Check if we can stop exploring this branch of search tree
    	        //This is where we save time
    	        if (beta < alpha){
    	        	break;
    	        }		
    		}
    		return value;
		}
		//Minimzing Player
		else{
			double value = Double.POSITIVE_INFINITY;
			//get every possible move
    		List<TablutMove> options = state.getAllLegalMoves();
    		//Iterate through moves
    		for (TablutMove move : options) {
    			//Clone board
    	        TablutBoardState childState = (TablutBoardState) state.clone();
    	        //Process particular move with parent boardState
    	        childState.processMove(move);
    	        double score = 0;
    	        //Create child Node in search tree
   	        	Node childNode = new Node(childState,(depth+1),(team-1)*-1,alpha,beta,orgTeam,desiredDepth);
   	        	score = childNode.alphaBeta(); //this gets the value of the board
    	        //If child is better than our best option, update best move
    	        if (score < value){
    	        	value = score;
    	        	bestMove = move;
    	        }
    	        //Update beta if best score is lower
    	        if (value < beta){
    	        	beta = value;
    	        }
    	        //Check if we can stop exploring this branch of search tree
    	        //This is where we save time
    	        if (beta < alpha){
    	        	break;
    	        }
    		}
    		return value;
		}
    }
    
    //Return the move associated with the highest score
    public TablutMove getBestMove(){
    	return bestMove;
    }
    
}
