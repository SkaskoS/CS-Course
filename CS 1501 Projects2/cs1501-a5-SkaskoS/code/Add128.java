import java.util.*;


public class Add128 implements SymCipher
{

	private byte[] key;
	
	public Add128() {
		Random rand = new Random();
		key = new byte[128];
		rand.nextBytes(key);
}

	public Add128(byte[] key) {
		this.key = key;
	}
	public byte[] getKey() {
		return key;
	}

	public byte[] encode(String encodedString) {
		byte[] result = encodedString.getBytes();
		byte[] output = new byte[result.length];
	

	for(int i = 0; i < result.length; i++) {
		result[i] = (byte)(result[i] + key[i % key.length]); //add key to i

	}


	return output;
}

public String decode(byte[] bytes) {
	
	byte[] newResult = new byte[bytes.length];


	for(int i = 0; i < newResult.length; i++) {
		newResult[i] = (byte)(newResult[i] - key[i % key.length]); //subtract  key from i

	}


	String newReturn = new String(newResult);
	return newReturn;


	}


	//Test driver to see if it works 
	public static void main(String[] args) {
		String str = "Computer Science 1501";  
		byte[] byteArray = str.getBytes();  
		System.out.println("Orginal byteArray" + byteArray);

		for(byte b : byteArray) {  
		System.out.println(b);  

		}	

		
	}

}