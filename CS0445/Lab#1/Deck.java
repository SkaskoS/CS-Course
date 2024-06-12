/*
	Deck class
*/

import java.util.*;
import java.io.*;

public class Deck
{
	private int[] deck; 
	private final int MAX_DECK_SIZE = 20;
	public Deck( int numCards )
	{	if ( numCards%2 != 0 || numCards > MAX_DECK_SIZE ) 
		{
			System.out.format("\nINVALID DECK SIZE: (" + numCards + "). Must be an small even number <= %d\n", MAX_DECK_SIZE);
			System.exit(0);
		}
		// YOU DO THIS => init deck to be exactly numCards long
		
			deck = new int[numCards]; 
			
			for(int i = 0; i < numCards; i++) //start at 0 and go through one increment at a time
			{
			
			
		// YOU DO THIS => fill deck with with 0 1 2 3 ... numCards-1 in order
				deck[i] = i; //i represents all numbers and deck corresponds to the construtor in making the deck

		 
				
	
			}
	}
	 
	public String toString() 
	{
		String deckStr = "";
		for ( int i=0 ; i < deck.length ; ++i )
			deckStr += deck[i] + " ";
		return deckStr;
	}

	// ONLY WORKS ON DECK WITH EVEN NUMBER OF CARDS
	// MODIFIES THE MEMBER ARRAY DECK
	public void inShuffle()
	{
		

    int orginal = deck.length / 2;
    int[] top = new int[orginal];
    int[] bottom = new int[orginal];

    for (int i = 0; i < orginal; i++) //Fills top + bottom array from the deck 
	{
      top[i] = deck[i]; //first few numbers
	  bottom[i] = deck[orginal + i]; //first numbers of split deck
	}
	for(int i = 0; i < orginal; i++) //Shuffles top + bottom of deck
	{
		
		deck[i*2] = bottom[i]; //deck = first index for first loop 
		deck[i*2+1] = top[i];
		//deck /2   01234567 {0,1,2,3}     {0,1,2,3}
		//4567 0123 4 0 
	}
	  
	}
	

	// ONLY WORKS ON DECK WITH EVEN NUMBER OF CARDS
	// MODIFIES THE MEMBER ARRAY DECK
	public void outShuffle()
	{
		
	
    int orginal = deck.length / 2;
    int[] top = new int[orginal];
    int[] bottom = new int[orginal];

    for (int i = 0; i < orginal; i++) //Fills top + bottom array from the deck 
	{
      top[i] = deck[i]; //first few numbers
	  bottom[i] = deck[orginal + i]; //first numbers of split deck
	}
	for(int i = 0; i < orginal; i++) //Shuffles top + bottom of deck
	{
		
		deck[i*2] = top[i]; //deck = first index for first loop 
		deck[i*2+1] = bottom[i];
		//deck /2   01234567 {0,1,2,3}     {0,1,2,3}
		//4567 0123 4 0 
	}
	  
		
		
	}
	// RETURNS TRUE IF DECK IN ORIGINAL SORTED:  0 1 2 3 ...
	public boolean inSortedOrder()
	{
		
	
	for(int i = 0; i < deck.length; i++)
	{
	if(deck[i] != i)
	
		
		return false;
	}
	return true;
	}
	
	
	
	
	
}
	

		
  	// END DECK CLASS
