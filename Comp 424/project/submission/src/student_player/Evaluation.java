package student_player;

import coordinates.Coord;
import coordinates.Coordinates;
import tablut.TablutBoardState;
import tablut.TablutBoardState.Piece;

public class Evaluation {
	//Board variable
	TablutBoardState boardState;	
	//Constants for evaluation
	//Two distinct sets to support asymmetric strategy
	double[] swedeConstants = { 10, 2, 7, 6, 3, 3 };
	double[] muscoviteConstants = {7, 10, 5, 5, 2, 2 };

	//Constructor
	public Evaluation(TablutBoardState boardState) {
		this.boardState = boardState;
	}

	//Calculates and returns board score
	public double boardScore(int team) {
		double constants[];		
		double[] evalScores;
		
		//If Swedes, use Swede constants and collect Swede feature scores
		if(team == 1){
			evalScores = collectTermsSwedes();
			constants = swedeConstants;
		}
		//Else, Use Muscovite data
		else{
			evalScores = collectTermsMuscovites();
			constants = muscoviteConstants;
		}
		//product of constants and feature scores
		double finalScore = 0;
		for (int i = 0; i < constants.length; i++) {
			finalScore += (evalScores[i] * constants[i]);
		}
		return finalScore;

	}
	
	//Build array of feature scores
	public double[] collectTermsSwedes() {
		double[] scores = new double[6];
		scores[0] = kingCornerDistance();
		scores[1] = kingOptions();
		scores[2] = numSwedes();
		scores[3] = numMuscovites();
		scores[4] = rowCol(1);
		scores[5] = rowCol(0);
		return scores;
	}
	
	//Flip sign of features for computing Muscovite board score
	public double[] collectTermsMuscovites(){
		double[] scores = collectTermsSwedes();
		for (int i = 0; i < scores.length; i++){
			scores[i] *= -1;
		}
		return scores;
	}

	// Get number of swedes on board
	//Swedes want to Maximize
	public double numSwedes() {
		return (boardState.getNumberPlayerPieces(1) / 9.0);

	}

	// Get number of muscovites on board
	//Swedes want to Minimize
	public double numMuscovites() {
		return (-boardState.getNumberPlayerPieces(0) / 16.0);
	}

	// Get distance of king to closest corner
	//Swedes want to Minimize
	public double kingCornerDistance() {
		Coord kingPos = boardState.getKingPosition();
		return (-Coordinates.distanceToClosestCorner(kingPos) / 8.0);
	}

	// Get number of possible moves for king
	//Swedes want to Maximize
	public double kingOptions() {
		Coord kingPos = boardState.getKingPosition();
		return boardState.getLegalMovesForPosition(kingPos).size() / 16.0;
	}

	// Calculates how well the sides pieces are spread out across each row and column
	// For every row/column occupied the score counts 1
	// This feature help support effective piece placement
	// Important for opening/closing rows to help/stop the king from moving effectively 
	public double rowCol(int side) {
		//rows
		boolean[] row = new boolean[9];
		//columns
		boolean[] col = new boolean[9];
		//Look through board
		for (int i = 0; i < 9; i++) {
			for (int j = 0; j < 9; j++) {
				//Whereever there is a piece mark that row and column and occupied
				Piece piece = boardState.getPieceAt(i, j);
				if (side == 1 && piece.toString().equals("WHITE") || piece.toString().equals("KING")) {
					row[i] = true;
					col[j] = true;
				} else if (side == 0 && piece.toString().equals("BLACK")) {
					row[i] = true;
					col[j] = true;
				}
			}
		}
		//Count how many rows and columns are occupied
		int score = 0;
		for (int i = 0; i < 9; i++) {
			if (row[i] == true) {
				score++;
			}
			if (col[i] == true) {
				score++;
			}
		}
		//Swedes want to Maximize for their own pieces
		if(side == 1){
			return (score/18.0);
		}
		//Swedes want to Minimize for Muscovite pieces
		else{
			return -(score / 18.0);
		}
	}

	//Calculates how many pieces are surrounding the king
	//Did not use variable in final code
	public double kingPressure() {
		int xKing = boardState.getKingPosition().x;
		int yKing = boardState.getKingPosition().y;
		int pressure = 0;
		//Check Left
		if (xKing > 0) {
			Piece piece = boardState.getPieceAt(xKing - 1, yKing);
			if (piece.toString().equals("BLACK")) {
				pressure++;
			}
		}
		//Check Right
		if (xKing < 8) {
			Piece piece = boardState.getPieceAt(xKing + 1, yKing);
			if (piece.toString().equals("BLACK")) {
				pressure++;
			}
		}
		//Check above
		if (yKing > 0) {
			Piece piece = boardState.getPieceAt(xKing, yKing - 1);
			if (piece.toString().equals("BLACK")) {
				pressure++;
			}
		}
		//Check below
		if (yKing < 8) {
			Piece piece = boardState.getPieceAt(xKing, yKing + 1);
			if (piece.toString().equals("BLACK")) {
				pressure++;
			}
		}
		return -(pressure / 4.0);
	}
}
