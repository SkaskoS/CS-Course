import java.io.*;
import java.util.*;

// DO NOT!! IMPORT JAVA.LANG
/////////////// NOT MY PROJECT WAS JUST TO HAVE A COPY OF THIS LAB, NOT MY WORK /////////////////////////////////////
public class Swamp
{
   static int[][] swamp; // NOW YOU DON'T HAVE PASS THE REF IN/OUT METHODS

    public static void main(String[] args) throws Exception
   {
       int[] dropInPt = new int[2]; // row and col will be on the 2nd line of input file;
       swamp = loadSwamp( args[0], dropInPt );
       int row=dropInPt[0], col = dropInPt[1];
       String path = ""; // with each step grows to => "[2,3][3,4][3,5][4,6]" etc
       dfs( row, col, path );
   } // END MAIN

   // --YOU-- WRITE THIS METHOD (LOOK AT PRINTSWAMP FOR CLUES)
    // ----------------------------------------------------------------
   private static int[][] loadSwamp( String infileName, int[] dropInPt ) throws Exception
   {
       File swampFile= new File(infileName);
       Scanner inputFile = new Scanner( swampFile );

       int dimension = inputFile.nextInt();
       dropInPt[0] = inputFile.nextInt();
       dropInPt[1] = inputFile.nextInt();
       int[][] swamp = new int[dimension][dimension];
       for( int r = 0; r <swamp.length; r++)
           for(int c = 0; c <swamp.length; c++)
               swamp[r][c] = inputFile.nextInt();
       inputFile.close();
       return swamp;
       // OPEN UP A SCANNER USING THE INCOMING FILENAME
       // THE FIRST NUMBER ON THE FIRST LINE WILL BE THE NUMBER OF ROWS & COLS
       // THE SECOND & THIRD NUMBER ON 1st LINE WILL BE THE DROP IN POINT X,Y
       // STORE SEOND NUMBER INTO dropInPt[0] THIRD # INTO dropInPt[1]
       // USING ROW, COL DEFINE A 2D ARRAY OF INT
       // USE A NESTED LOOP. OUTER LOOP ROWS, INNER LOOP COLS
       // READ IN THE GRID OF VALUES FROM THE INPUT FILE
       // CLOSE THE SCANNER
       // RETURN THE 2D ARRAY WITH VALUES LOADED INTO IT
       // JUST TO MAKE IT COMPILE
   }

   static void dfs( int r, int c, String path ) // dfs = DEPTH FIRST SEARCH
   {
       path += "[" + Integer.toString(r) + "," + Integer.toString(c) + "]"; //finish writing

       if (onEdge(r,c))
       {
           System.out.println(path);
           return;
       }
       if(swamp[r-1][c] == 1) // north
       {
           swamp[r][c]= -1;
           dfs(r-1, c, path);
           swamp[r][c] = 1;
       }
       if(swamp[r-1][c+1] == 1) // northeast
       {
           swamp[r][c]= -1;
           dfs(r-1, c+1, path);
           swamp[r][c] = 1;
       }
       if(swamp[r][c+1] == 1) // east
       {
           swamp[r][c]= -1;
           dfs(r, c+1, path);
           swamp[r][c] = 1;
       }
       if(swamp[r+1][c+1] == 1) // southeast
       {
           swamp[r][c]= -1;
           dfs(r+1, c+1, path);
           swamp[r][c] = 1;
       }
       if(swamp[r+1][c] == 1) // south
       {
           swamp[r][c]= -1;
           dfs(r+1, c, path);
           swamp[r][c] = 1;
       }
       if(swamp[r+1][c-1] == 1) // southwest
       {
           swamp[r][c]= -1;
           dfs(r+1, c-1, path);
           swamp[r][c] = 1;
       }
       if(swamp[r][c-1] == 1) // west
       {
           swamp[r][c]= -1;
           dfs(r, c-1, path);
           swamp[r][c] = 1;
       }
       if(swamp[r-1][c-1] == 1) // northwest
       {
           swamp[r][c]= -1;
           dfs(r-1, c-1, path);
           swamp[r][c] = 1;
       }

   }
   static boolean onEdge(int r, int c)
   {
       return ( r==0 || r == swamp.length - 1 || c==0 || c == swamp[r].length - 1 );
   }
}