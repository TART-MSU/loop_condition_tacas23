// package HyperQube;
import java.io.*;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map.Entry;
import java.util.*;


public class gen_model_a{

	// Bit-wise operations
	static int num_bits_info = 1;
	static int info_msb = num_bits_info-1;
	static int num_bits_state = 2;
	static int state_msb = num_bits_state-1;

	// Logical Operators 
	static String AND = " /\\ ";
	static String OR = " \\/ ";
	static String IMPLIES = " -> ";
	static String NOT = "~";
	static String EQUAL = " <-> ";
	static String IFF = " <-> ";
	static String SWITCH = "~";


	// variables 
	static String state = "state_";
	static String var_p = "p";
	// static String var_b = "b";

	static String[] all_variables = {"p"};

	// static TS ts;


	public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {

		// Transition System Creator ////
		// ts = new TS(all_variables);



		// constrcut transition relations
       	PrintWriter writer_R = new PrintWriter("model_a_R.bool", "UTF-8");
       	writer_R.write(generate_transitions());
	   	writer_R.close();

	   	// give initial values
	   	PrintWriter writer_I = new PrintWriter("model_a_I.bool", "UTF-8");
       	writer_I.write(generate_initialState());
	   	writer_I.close();

	   	// properties
	   	PrintWriter writer_P = new PrintWriter("test_P.bool", "UTF-8");
	   	writer_P.write(generate_property());
	   	writer_P.close();

	}

	///////////  P r o p e r t y   ///////////////
	private static String generate_property(){

		// For original AA formula ???
		// testcase( AA F(a_pi /\ Zb_pi') ) ---> EA G(~a_pi \/ ~b_pi')

		/// eventually p iff p
		return "F(" + "p_A" + OR + "~p_A)";	/// Dummy property
		// return "";


		/// property of checking simulation relation
		

	}


	////////    I n i t i a l    S t a t e  //////////

	private static String generate_initialState(){

		ArrayList<String> all = new ArrayList<>();
		all.add(initialState(0));
		all.add(NOT+var_p);

		return conjunction(all);
	}



	/////////////////  M o d e l    ////////////////

	private static String generate_transitions(){

		String goto_state0 = conjunct2(nextState(0), atom_assignFalse(var_p));
		String goto_state1 = conjunct2(nextState(1), atom_assignFalse(var_p));
		String goto_state2 = conjunct2(nextState(2), atom_assignTrue(var_p));


		ArrayList<String> tr = new ArrayList<>();
		tr.add(implication(currState(0), goto_state1));
		tr.add(implication(currState(1), disjunct2(goto_state0, goto_state2)));
		tr.add(implication(currState(2), goto_state2));
		return conjunction(tr);

	}









































	// -------- H e l p e r     M e t h o d s --------//



	////// A T O M I C  O P E R A T I O N S //////

	// "assign the negation" of the output, so the value switched
	private static String atom_switch(String var){
			return "(" + NOT+ var + EQUAL + var  + "')";
	}

	private static String atom_assignTrue(String var){
		return  conjunct2(implication(NOT+var, "("+NOT+var+ EQUAL + var +"')"), 
						  implication(var, "(" + var + EQUAL + var  +"')"));
	}

	private static String atom_assignFalse(String var){
		return  conjunct2(implication(var, "("+NOT+var+ EQUAL + var +"')"), 
						  implication(NOT+var, "(" + var + EQUAL + var  +"')"));
	}

	//switc to True and always be true
	private static String atom_toggleToTrue(String var){
		return  conjunct2(implication(NOT+var, "("+NOT+var+ EQUAL + var +"')"), 
						  implication(var, "(" + var + EQUAL + var  +"')"));
	}

	private static String atom_staySame(String var){
		return  "(" + var + EQUAL + var  +"')";
	}




	//////// L O G I C A L   O P E R A T I O N ///////

	// create a conjunction clause for a list of Strings
 	private static String conjunction(ArrayList<String> arr){
 		String temp = "(";
 		for (int i = 0 ; i < arr.size() ; i++){
 			temp += "(" + arr.get(i) + ")";
 			if (i != (arr.size()-1)) temp += "\n" + AND ; else temp += ")\n";
 		}
 		return temp;
 	}

 	// create a disjunction clause for a list of Strings
 	private static String disjunction(ArrayList<String> arr){
 		String temp = "(";
 		for (int i = 0 ; i < arr.size() ; i++){
 			temp += "(" + arr.get(i) + ")";
 			if (i != (arr.size()-1)) temp += "\n" + OR ; else temp += ")\n";
 		}
 		return temp;
 	}

 	// implication
 	private static String implication(String a, String b){

 		return "((" + a + ")" + IMPLIES + "(" + b + "))";
 	}

 	// simple conjunct two Strings together
 	private static String conjunct2(String a, String b){

 		return "((" + a + ")" + AND + "(" + b + "))";
 	}

 	private static String conjunct3(String a, String b, String c){

 		return "(" + a + AND + b + AND + c + ")";
 	}

 	private static String disjunct2(String a, String b){

 		return "(" + a + OR + b + ")";
 	}

 	private static String disjunct3(String a, String b, String c){

 		return "(" + a + OR + b + OR + c + ")";
 	}

 	private static String conjunct4(String a, String b, String c, String d){

 		return "(" + a + AND + b + AND + c + AND + d + ")";
 	}

 	private static String iff(String a, String b){

 		return "((" + a + ")" + EQUAL + "(" + b + "))";
 	}



 	////// S T A T E   T R A N S I T I O N ///////

 	// assign initial state
	private static String initialState(int num){
		String bin = String.format( "%0"+ num_bits_state +"d" , Integer.parseInt(Integer.toBinaryString(num)));
		int msb = num_bits_state-1;

		String result = "(";
		for (int j = 0 ; j <= msb ; j++ ){
			if (bin.charAt(j) == '0')
				result += NOT;

			result += state + (msb-j);
			if (j != msb)  { result += AND ; }
			else  { result += ")"; }
		}
		return result;
	}

	// if current state is s_num
	private static String currState(int num){
		String bin = String.format( "%0"+ num_bits_state +"d" , Integer.parseInt(Integer.toBinaryString(num)));
		int msb = num_bits_state-1;

		String result = "(";
		for (int j = 0 ; j <= msb ; j++ ){
			if (bin.charAt(j) == '0') 
				result += NOT;

			result += state + (msb-j);
			if (j != msb)  
				{ result += AND ; }
			else  
				{ result += ")"; }
		}
		return result;
	}


	// assign next outgoing state
	private static String nextState(int num){
		String bin = String.format( "%0"+ num_bits_state +"d" , Integer.parseInt(Integer.toBinaryString(num)));
		int msb = num_bits_state-1;

		String result = "(";
		for (int j = 0 ; j <= msb ; j++ ){
			if (bin.charAt(j) == '0') 
				result += NOT;

			result += state + (msb-j) + "'";
			if (j != msb)  
				{ result += AND ; }
			else  
				{ result += ")"; }
		}
		return result;
	}


	/////////////////  v a r i a b l e     p a s s i n g  /////////////////
	// pass all variables listed in variables
	private static String passAll(){

		ArrayList<String> all = new ArrayList<>();
		for (int i = 0 ; i < all_variables.length ; i++ ){
				all.add(passValue(all_variables[i], 1)); 
		}
		return conjunction(all);
	}

	private static String passAllExceptFor(String str){
		ArrayList<String> all = new ArrayList<>();
		for (int i = 0 ; i < all_variables.length ; i++ ){
			if (!all_variables[i].equals(str)){

				all.add(passValue(all_variables[i], 1));
				
			}
		}
		return conjunction(all);
	}

	private static String passAllExceptFor2(String str1, String str2){
		ArrayList<String> all = new ArrayList<>();
		for (int i = 0 ; i < all_variables.length ; i++ ){
			if (!all_variables[i].equals(str1) && !all_variables[i].equals(str2)){

				all.add(passValue(all_variables[i], 1));
				
			}
		}
		return conjunction(all);
	}


	///// B i t - W I S E   O P E R A T I O N /////

	// // passValue, with given width of bits 
	private static String passValue(String var, int num_bits){

		String temp = "(";
		if (num_bits == 1){
			temp += var + EQUAL + var + "'" + ")";
		}
		else {
			for (int y = (num_bits-1) ; y >= 0 ;y --){
				temp += "(" + var + y + EQUAL + var + y +"')";
				if (y != 0)  temp += AND ; else temp += ")";
			}
		}
		return temp;
	}
	
	// for initial state to use
	// private static String initialAssignVarAsValue(String proc, String var, int value){
	// 	String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(value)));
	// 	int msb = num_bits_pc-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += proc + var + (msb-j);

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;
	// }

	// if variable is in the value vlaue
	// private static String inputVarAsValue(String var, int value){
	// 	String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(value)));
	// 	int msb = num_bits_info-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += var + (msb-j);

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;
	// }

	// // A := A or B (bitwise or)
	// private static String outputAlice_as_bitwiseve_AorB(String varA, String varB){

	// 	String result = "(";
	// 	for (int i = info_msb ; i >= 0 ; i--){
	// 		result += "((" + varA + i + OR + varB + i + ")" + EQUAL + varA + i +"' )";
	// 		if (i != 0 ) result += AND;
	// 	}
	// 	result += ")";

	// 	return result;
	// }

	// // A := A and comp(B) (bitwise and)
	// private static String outputAlice_as_bitwiseve_AandCompB(String varA, String varB){

	// 	String result = "(";
	// 	for (int i = info_msb ; i >= 0 ; i--){
	// 		result += "((" + varA + i + AND + NOT + varB + i + ")" + EQUAL + varA + i +"' )";
	// 		if (i != 0 ) result += AND;
	// 	}
	// 	result += ")";

	// 	return result;
	// }

	// // A := A and (B) (bitwise and)
	// private static String outputAlice_as_bitwiseve_AandB(String varA, String varB){

	// 	String result = "(";
	// 	for (int i = info_msb ; i >= 0 ; i--){
	// 		result += "((" + varA + i + AND + varB + i + ")" + EQUAL + varA + i +"' )";
	// 		if (i != 0 ) result += AND;
	// 	}
	// 	result += ")";

	// 	return result;
	// }

	// check bit-wise equal for two NODE
	// private static String equal(String var1, String var2){
	// 	String temp = "(";
	// 	for (int y = (num_bits_info-1) ; y >= 0 ;y --){
	// 		temp += "(" + var1 + y + EQUAL + var2 + y +")";
	// 		if (y != 0)  temp += AND ; else temp += ")";
	// 	}
	// 	return temp;
	// }

	// // for initial state to use
	// private static String initialAssignVarAsNode(String proc, String var, int nodeID){

	// 	String bin = String.format( "%0"+ num_bits_info +"d" , Integer.parseInt(Integer.toBinaryString(nodeID)));
	// 	int msb = num_bits_info-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += proc + var + (msb-j);

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;
	// }


	// // assign "all zeros" to each bit to it's value
	// private static String assignEmpty(String proc, String var, int num_bits){
	// 	String result = "(";
	// 	int msb = num_bits-1;
	// 	for (int i = msb ; i >= 0 ; i--){
	// 		result += NOT + proc + var + i;
	// 		if (i != 0 ) result += AND;
	// 	}
	// 	return result + ")\n";
	// }



	// private static String outputVarAsValue(String var, int value){
	// 	String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(value)));
	// 	int msb = num_bits_info-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += var + (msb-j) + "'";

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;
	// }



	// // process name can be empty, that will indicates that it's a shared variable
	// private static String assignVarAasVarB(String procA, String varA, String procB, String varB){
	// 	String temp = "(";
	// 	for (int y = (num_bits_node-1) ; y >= 0 ;y --){
	// 		temp += "(" + procB + varB + y + EQUAL + procA + varA + y +"')";
	// 		if (y != 0)  temp += AND ; else temp += ")";
	// 	}
	// 	return temp;
	// }

	// // create a increment bit-wise transition for var, from 0 - max 
	// private static String increment(String var, int max){
	// 	int num_bits = (int) Math.ceil(Math.log((max+1)) / Math.log(2.0));
	// 	int msb = num_bits-1;
	// 	String result = "(";
	// 	for (int i = 0 ; i < max ; i++){

	// 		String  left_bin = String.format( "%0"+ num_bits +"d" , Integer.parseInt(Integer.toBinaryString(i)));
	// 		String  right_bin = String.format( "%0"+ num_bits +"d"  , Integer.parseInt(Integer.toBinaryString(i+1)));

	// 		String left = "(";
	// 		String right = "(";
	// 		for (int j = 0 ; j <= msb ; j++ ){
	// 			if (left_bin.charAt(j) == '0')
	// 				left += NOT;
	// 			if (right_bin.charAt(j) == '0')
	// 				right += NOT;

	// 			left += var + (msb-j);
	// 			right += var + (msb-j) + "'";

	// 			if (j != msb)  { left += AND ; right += AND; }
	// 			else  { left += ")";  right += ")"; }
	// 		}
	// 		result += "(" + left + IMPLIES + right + ")";
	// 		if (i != (max-1)) result += "\n" + AND ; else result += ")";
	// 	}
	// 	return result;
	// }


	////// P R O G R A M    C O U N T E R /////

	// assign next execution of a process, with given line number
	// private static String assignNextExecution(String proc, int lineve_number){

	// 	String var = RUN;
	// 	String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(lineve_number)));


	// 	//sSystem.out.println("AT LINE 25 -------> "+ String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(24))) );

	// 	int msb = num_bits_pc-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += proc + var + (msb-j) + "'";

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;

	// }


	// assign RUN of a process to a certain line numbers
	// private static String currentRunningLine(String proc, int lineve_number){
	// 	String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(lineve_number)));
	// 	int msb = num_bits_pc-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += proc + RUN + (msb-j);

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;
	// }

	// list out all possible run of code for this process, zero = not running
	// private static ArrayList<String> allRuns(String proc){

	// 	String var = RUN;
	// 	ArrayList<String> result = new ArrayList<String>();
	// 	int msb = num_bits_pc-1;

	// 	for (int i = 0 ; i <= MAX_PC ; i++){

	// 		String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(i)));

	// 		String temp = "(";
	// 		for (int j = 0 ; j <= msb ; j++ ){
	// 			if (bin.charAt(j) == '0')
	// 				temp += NOT;
	// 			temp += proc + var + (msb-j);

	// 			if (j != msb)  { temp += AND ; }
	// 			else  { temp +=")"; }
	// 		}
	// 		result.add(temp);
	// 	}
	// 	return result;
	// }


 	///// M  I  S  C /////


 	// DON"T DO THIS!!!!
	// private static String assignVarAsNode(String proc, String var, int nodeID){

	// 	String bin = String.format( "%0"+ num_bits_node +"d" , Integer.parseInt(Integer.toBinaryString(nodeID)));
	// 	int msb = num_bits_node-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		if (bin.charAt(j) == '0')
	// 			result += NOT;
	// 			result += proc + var + (msb-j) + "'";

	// 			if (j != msb)  { result += AND ; }
	// 			else  { result += ")"; }
	// 	}
	// 	return result;

	// }

	// private static String whateverRunningLine(String proc){
	// 	//String bin = String.format( "%0"+ num_bits_pc +"d" , Integer.parseInt(Integer.toBinaryString(lineve_number)));
	// 	int msb = num_bits_pc-1;

	// 	String result = "(";
	// 	for (int j = 0 ; j <= msb ; j++ ){
	// 		//if (bin.charAt(j) == '0')
	// 			//result += NOT;
	// 			result += proc + RUN + (msb-j);

	// 			if (j != msb)  { result += OR ; }
	// 			else  { result += OR + currentRunningLine(proc, 0) +  ")"; }
	// 	}
	// 	return result;
	// }

}






