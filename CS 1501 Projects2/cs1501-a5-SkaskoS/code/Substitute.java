import java.util.*;


public class Substitute implements SymCipher
{

	private byte[] key;
	
	public Substitute() {

		key = new byte[256];

		for(int i = 0; i < key.length; i++) {
			key[i] = (byte)i;
		}
		for(int i = 0; i < key.length; i++) { 

		Random ran = new Random();
		int random = ran.nextInt(256);

		//reverse 
		byte tmp = key[i];
		key[i] = key[random];
		key[random] = tmp;
	}
}

	public Substitute(byte[] key) {
		this.key = key;
	}
	public byte[] getKey() {
		return key;
	}

	public byte[] encode(String encodedString) {
		byte[] result = encodedString.getBytes();
		byte[] output = new byte[result.length];
	

	for(int i = 0; i < result.length; i++) {
		result[i] = (key[((int) result[i] & 0xff)]);
	}

	return output;
}

public String decode(byte[] bytes) {
	byte[] newResult = new byte[bytes.length];
	byte[] newResult1 = new byte[key.length];

	for(int i = 0; i < newResult.length; i++) {

		newResult[i] = (newResult1[((int) newResult[i] & 0xff)]);

	}
	String newReturn = new String(newResult); //convert back to String
	return newReturn;

	}
		public static void main(String[] args) {
		String str = "Computer Science 1501";  
		byte[] byteArray = str.getBytes();  
		System.out.println("Orginal byteArray" + byteArray);

		for(byte b : byteArray) {  
		System.out.println(b);  

		}	
		
	}
}