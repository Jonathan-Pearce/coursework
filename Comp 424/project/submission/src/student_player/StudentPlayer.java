package student_player;

import boardgame.Move;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

/** A player file submitted by a student. */
public class StudentPlayer extends TablutPlayer {
	private int searchDepth = 3;

	/**
	 * You must modify this constructor to return your student number. This is important, because this is what the code that runs the competition uses
	 * to associate you with your agent. The constructor should do nothing else.
	 */
	public StudentPlayer() {
		super("260672004");
	}

	/**
	 * This is the primary method that you need to implement. The ``boardState`` object contains the current state of the game, which your agent must
	 * use to make decisions.
	 */
	public Move chooseMove(TablutBoardState boardState) {
		TablutMove move = null;
		Node root;

		//Opening move code
		//Fixed opening move for both sides
		if (boardState.getTurnNumber() == 0) {
			// opening moves
			if (player_id == 0) {
				//Begin barricade in bottom right corner
				move = new TablutMove(7, 4, 7, 6, 0);
			} else {
				//Set pick at top of board, gives king early opportunity to move out
				move = new TablutMove(4, 5, 1, 5, 1);
			}
		} else {
			//ALPHA BETA PRUNING code
			
			//Check if there is an immediate winning move
			//My player is capable of looking 3 moves ahead (2 of their own
			//and 1 of the opponents) so it can tell when its guaranteed a win, however it will not always
			//Take the winning move, it will wait sometimes until the opponent is 1 move away from
			//preventing the guaranteed win and at that point it will take the win
			//This code was added to prevent any issues of closing out games when the turn count is high
			//I need to make sure that if there is a win I take it immediately, otherwise we may reach
			//the last turn and settle for a draw when we have a win in hand
			root = new Node(boardState, 0, player_id, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY,
					player_id, 1);
			double score = root.alphaBeta();
			// If there is a winning moving lets take it
			if (score == 10000.0) {
				move = root.getBestMove();
			}
			
			//If there is no immediate winning move, then do full search
			//Do Minimax search with Alpha Beta Pruning to depth of 3
			//Find best move
			else {
				root = new Node(boardState, 0, player_id, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY,
						player_id, searchDepth);
				score = root.alphaBeta();
				move = root.getBestMove();
			}
		}
		// Return your move to be processed by the server.
		return move;
	}

}