import java.util.*;


public class Permute implements SymCipher
{

	private byte[] key;
	private byte[] location;

	public Permute() {

		key = new byte[256];

		for(int i = 0; i < key.length; i++) { //cipher text array
			
			key[i] = (byte)i;
		}

		for(int i = 0, j = 0; i < key.length; i++, j++) { 

		if(j == key.length) {
			j=0;
		}


			
			Random ran = new Random();
			int random = ran.nextInt(256); ///random that takes 256 bits array


			/*
			byte values and will serve as a map from locations in the plain 
			text array to their destination location in the cipher text array

			Also: need an inverse mapping array for this cipher, which can be easily derived from 
			      the substitution array
			*/

			//reverse 
			byte tmp = key[i];
			key[i] = key[random];
			key[random] = tmp;
		}
	}



	public Permute(byte[] key) {
		
		this.key = key;
	}
	public byte[] getKey() {
		
		return key;
	}

	public byte[] encode(String encodedString) { //have to convert to an array of bytes
		
		byte[] result = encodedString.getBytes(); //convert String to bits
		byte[] output = new byte[result.length];
	

		for(int i = 0; i < result.length; i++) { //iterate through bytes 

			//If the plain text array is smaller than 256 bytes or if its size is not a multiple of 256

			//array of elements into Bytes 
			result[i] = (byte)(result[i] + key[i % key.length]);   //Check Here: determine the destination location in the cipher text array. Must return null
		}

			return output;
	}

	public String decode(byte[] bytes) {
	
		byte[] newResult = new byte[bytes.length];
		byte[] newResult1 = new byte[key.length];



		for(int i = 0; i < newResult.length; i++) { 

			//If the cipher text array is smaller than 256 bytes or if its size is not a multiple 
			//of 256, the `decode()` method should return `null`.

			newResult[i] = (byte)(newResult[i] - key[i % key.length]); //reverse the array + Check Here

		}
	

	 String newReturn = new String( plaintext ) ;
    plaintextString = plaintextString.toLowerCase();
    plaintext = plaintextString.toCharArray() ;

    char i =0 ;
    for (int index=0; index<plaintext.length; index++)
    {
        i = plaintext[index] ;
        if ( i == ' ')                      //The space character 
        {                                   //doesn't get encrypted
            plaintext[index] = ' ' ;
        }
        for (int index2=0; index2<alphabet.length; index2++)
        {
            if ( i == alphabet[index2])    //Alphabet array already generated
            {
                encrypt[index]= cipher[index2] ;                                    
            }
        }


    }
				return newReturn; //should return null
	}

	//Test driver to see if it works to encode + Check: How to run Decode method?
		public static void main(String[] args) {
		String str = "Computer Science 1501";  
		String str2 = "15";
		byte[] byteArray = str.getBytes();  
		System.out.println("Orginal byteArray: " + byteArray);

		for(byte b : byteArray) {  
		System.out.print(" " +b); 


			}	

		Byte actualByte = Byte.decode(str2);
				System.out.println();

		System.out.println("Decode: " + actualByte);
		}
		
	}

